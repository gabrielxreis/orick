"""Arte do Rick em camadas para o Canva: plano JSON -> PPTX no tamanho exato da peça (1 px = 1 px).

O Canva importa PPTX como design editável (import-design-from-url do conector oficial, ou arrastando o arquivo):
cada texto vira caixa de texto editável (fonte, cor, tamanho, trechos coloridos), cada imagem e forma vira um
elemento separado, cada página do carrossel vira uma página do design.

  python3 montar_pptx.py plano.json [--saida arte.pptx]

Plano (caminhos de imagem relativos à pasta do plano):
{
  "titulo": "Carrossel X - Tema",
  "tamanho": [1080, 1350],
  "paginas": [
    {"camadas": [
      {"tipo": "imagem", "arquivo": "fundo_p1.png", "x": 0, "y": 0, "w": 1080, "h": 1350, "nome": "Fundo (IA)"},
      {"tipo": "forma", "forma": "retangulo|arredondado|elipse", "x": 80, "y": 900, "w": 920, "h": 300,
       "cor": "#000000", "opacidade": 0.55, "raio": 32, "borda": {"cor": "#FFFFFF", "px": 2}, "nome": "Caixa"},
      {"tipo": "texto", "texto": "TÍTULO EM\\nDUAS LINHAS", "x": 80, "y": 940, "w": 920, "h": 240,
       "fonte": "Anton", "tamanho": 96, "cor": "#FFFFFF", "negrito": false, "italico": false,
       "alinhar": "esquerda|centro|direita|justificado", "vertical": "topo|meio|base",
       "entrelinha": 1.0, "espacamento": 0, "caixa_alta": false, "sombra": false,
       "faixas": [{"trecho": "DUAS", "cor": "#F88F22", "fonte": "Anton", "negrito": true}], "nome": "Título"}
    ]}
  ]
}
Medidas em px da peça. "tamanho" do texto em px (altura do corpo, como no Photoshop); "espacamento" em px entre letras.
Camadas na ordem do plano = de baixo para cima. "nome" vira o nome da camada no Canva.
"""
import argparse, copy, json, os, re, sys

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

EMU_PX = 9525                      # 1 px a 96 dpi
PT_PX = 0.75                       # 1 px = 0,75 pt
ALINHAR = {"esquerda": PP_ALIGN.LEFT, "centro": PP_ALIGN.CENTER, "direita": PP_ALIGN.RIGHT,
           "justificado": PP_ALIGN.JUSTIFY}
VERTICAL = {"topo": MSO_ANCHOR.TOP, "meio": MSO_ANCHOR.MIDDLE, "base": MSO_ANCHOR.BOTTOM}
FORMAS = {"retangulo": MSO_SHAPE.RECTANGLE, "arredondado": MSO_SHAPE.ROUNDED_RECTANGLE, "elipse": MSO_SHAPE.OVAL}


def px(v):
    return Emu(int(round(float(v) * EMU_PX)))


def rgb(hexa):
    h = hexa.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return RGBColor.from_string(h[:6].upper())


def _alfa(fill_xml_parent, opacidade):
    """Transparência no preenchimento sólido (o python-pptx não expõe): <a:alpha val="55000"/>."""
    if opacidade is None or opacidade >= 1:
        return
    clr = fill_xml_parent.find(".//" + qn("a:srgbClr"))
    if clr is not None:
        a = etree.SubElement(clr, qn("a:alpha"))
        a.set("val", str(int(round(max(0.0, opacidade) * 100000))))


def imagem(slide, c, base):
    arq = c["arquivo"] if os.path.isabs(c["arquivo"]) else os.path.join(base, c["arquivo"])
    if not os.path.exists(arq):
        raise SystemExit(f"imagem não encontrada: {arq}")
    pic = slide.shapes.add_picture(arq, px(c.get("x", 0)), px(c.get("y", 0)), px(c["w"]), px(c["h"]))
    pic.name = c.get("nome") or os.path.basename(arq)
    return pic


def forma(slide, c):
    sh = slide.shapes.add_shape(FORMAS.get(c.get("forma", "retangulo"), MSO_SHAPE.RECTANGLE),
                                px(c["x"]), px(c["y"]), px(c["w"]), px(c["h"]))
    sh.name = c.get("nome") or c.get("forma", "forma")
    if c.get("forma") == "arredondado":
        sh.adjustments[0] = min(0.5, float(c.get("raio", 24)) / max(1.0, min(c["w"], c["h"])))
    if c.get("cor"):
        sh.fill.solid(); sh.fill.fore_color.rgb = rgb(c["cor"])
        _alfa(sh.fill._xPr, c.get("opacidade"))
    else:
        sh.fill.background()
    b = c.get("borda")
    if b:
        sh.line.color.rgb = rgb(b.get("cor", "#000000")); sh.line.width = Pt(float(b.get("px", 1)) * PT_PX)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    if sh.has_text_frame:
        sh.text_frame.text = ""
    return sh


def _run_estilo(run, fonte, tamanho_px, cor, negrito, italico, espacamento_px):
    f = run.font
    f.name = fonte; f.size = Pt(tamanho_px * PT_PX); f.bold = bool(negrito); f.italic = bool(italico)
    f.color.rgb = rgb(cor)
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):       # mesma fonte em todos os scripts (acentos não trocam de fonte)
        el = rpr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rpr, qn(tag))
        el.set("typeface", fonte)
    if espacamento_px:
        rpr.set("spc", str(int(round(espacamento_px * PT_PX * 100))))   # centésimos de ponto


def _pedacos(linha, faixas):
    """Divide a linha nos trechos destacados (primeira ocorrência de cada, na ordem): [(texto, estilo|None)]."""
    pedacos = [(linha, None)]
    for fx in faixas or []:
        alvo = fx.get("trecho", "")
        if not alvo:
            continue
        novos = []
        for txt, est in pedacos:
            if est is None and alvo in txt:
                i = txt.index(alvo)
                novos += [(txt[:i], None), (alvo, fx), (txt[i + len(alvo):], None)]
            else:
                novos.append((txt, est))
        pedacos = [(t, e) for t, e in novos if t]
    return pedacos


AVISOS = []


def texto(slide, c):
    txt0 = c["texto"].upper() if c.get("caixa_alta") else c["texto"]
    if c.get("entrelinha") and float(c["entrelinha"]) < 1.05 and "\n" in txt0 and re.search(r"[ÇÁÉÍÓÚÂÊÔÃÕÀ]", txt0):
        AVISOS.append(f"'{c.get('nome') or txt0[:20]}': acento/cedilha em caixa alta com entrelinha {c['entrelinha']}"
                      " (encosta na linha de baixo; usar >= 1.05)")
    tb = slide.shapes.add_textbox(px(c["x"]), px(c["y"]), px(c["w"]), px(c.get("h", c.get("tamanho", 40) * 1.4)))
    tb.name = c.get("nome") or c["texto"].split("\n")[0][:40]
    tf = tb.text_frame
    tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = VERTICAL.get(c.get("vertical", "topo"), MSO_ANCHOR.TOP)
    txt = c["texto"].upper() if c.get("caixa_alta") else c["texto"]
    faixas = c.get("faixas") or []
    if c.get("caixa_alta"):
        faixas = [dict(f, trecho=f.get("trecho", "").upper()) for f in faixas]
    base = {"fonte": c.get("fonte", "Inter"), "tamanho": float(c.get("tamanho", 40)), "cor": c.get("cor", "#000000"),
            "negrito": c.get("negrito", False), "italico": c.get("italico", False), "espacamento": c.get("espacamento", 0)}
    for i, linha in enumerate(txt.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = ALINHAR.get(c.get("alinhar", "esquerda"), PP_ALIGN.LEFT)
        if c.get("entrelinha"):
            p.line_spacing = float(c["entrelinha"])
        p.space_before = p.space_after = Pt(0)
        for parte, est in _pedacos(linha, faixas) or [(" ", None)]:
            e = dict(base, **{k: v for k, v in (est or {}).items() if k != "trecho"})
            r = p.add_run(); r.text = parte
            _run_estilo(r, e["fonte"], float(e["tamanho"]), e["cor"], e["negrito"], e["italico"], e["espacamento"])
    if c.get("sombra"):
        sp = tb._element.spPr
        ef = etree.SubElement(sp, qn("a:effectLst"))
        sh = etree.SubElement(ef, qn("a:outerShdw"), blurRad="76200", dist="25400", dir="5400000", algn="t")
        clr = etree.SubElement(sh, qn("a:srgbClr"), val="000000"); etree.SubElement(clr, qn("a:alpha"), val="55000")
    return tb


def montar(plano_arq, saida=None):
    plano = json.load(open(plano_arq, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(plano_arq))
    W, H = plano.get("tamanho", [1080, 1350])
    prs = Presentation()
    prs.slide_width, prs.slide_height = px(W), px(H)
    vazio = prs.slide_layouts[6]   # layout em branco
    for pg in plano["paginas"]:
        s = prs.slides.add_slide(vazio)
        for c in pg["camadas"]:
            {"imagem": lambda c: imagem(s, c, base), "forma": lambda c: forma(s, c),
             "texto": lambda c: texto(s, c)}[c["tipo"]](c)
    prs.core_properties.title = plano.get("titulo", "Arte do Rick")
    saida = saida or os.path.join(base, re.sub(r"[^\w\- ]+", "", plano.get("titulo", "arte")).strip() + ".pptx")
    prs.save(saida)
    return saida


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plano"); ap.add_argument("--saida")
    a = ap.parse_args()
    print(montar(a.plano, a.saida))
    for av in AVISOS:
        print("AVISO:", av, file=sys.stderr)
