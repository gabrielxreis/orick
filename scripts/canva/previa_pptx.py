"""Prévia de cada página de um PPTX do Rick (conferir antes de mandar ao Canva), sem abrir nenhum app.

  python3 previa_pptx.py arte.pptx [--largura 1080]

Gera <arte>_p01.png, <arte>_p02.png... ao lado do PPTX (Quick Look do macOS, uma página por vez) e, com mais de
uma página, a folha <arte>_folha.jpg (carrossel_entrega.py). Fora do Mac: abrir o PPTX no PowerPoint/LibreOffice.
"""
import argparse, copy, glob, os, shutil, subprocess, sys, tempfile

from pptx import Presentation

AQUI = os.path.dirname(os.path.abspath(__file__))


def so_pagina(origem, i, destino):
    prs = Presentation(origem)
    lista = prs.slides._sldIdLst
    for n, sld in reversed(list(enumerate(list(lista)))):
        if n != i:
            prs.part.drop_rel(sld.rId); lista.remove(sld)
    prs.save(destino)


def previa(pptx, largura=1080):
    if sys.platform != "darwin":
        raise SystemExit("prévia automática só no Mac (Quick Look); abra o PPTX no PowerPoint ou LibreOffice")
    n = len(Presentation(pptx).slides)
    base = os.path.splitext(pptx)[0]; saidas = []
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(n):
            arq = os.path.join(tmp, f"p{i + 1:02d}.pptx")
            so_pagina(pptx, i, arq)
            subprocess.run(["qlmanage", "-t", "-s", str(largura), "-o", tmp, arq], capture_output=True, timeout=120)
            png = arq + ".png"
            if os.path.exists(png):
                dst = f"{base}_p{i + 1:02d}.png"; shutil.move(png, dst); saidas.append(dst)
    if len(saidas) > 1:
        with tempfile.TemporaryDirectory() as pasta:
            for s in saidas:
                shutil.copy(s, pasta)
            subprocess.run([sys.executable, os.path.join(os.path.dirname(AQUI), "carrossel_entrega.py"), pasta],
                           capture_output=True, timeout=300)
            folha = os.path.join(pasta, "folha_carrossel.jpg")
            if os.path.exists(folha):
                shutil.copy(folha, base + "_folha.jpg"); saidas.append(base + "_folha.jpg")
    return saidas


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("pptx"); ap.add_argument("--largura", type=int, default=1080)
    a = ap.parse_args()
    print("\n".join(previa(os.path.abspath(a.pptx), a.largura)))
