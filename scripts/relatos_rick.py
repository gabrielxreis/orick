"""Relatos que chegaram das máquinas que usam o Rick (lado do DONO). A fila é a MESMA da VPS do Gab: os itens do Rick
chegam com o nome começando por RICK_ (ver relatar_rick.py). Lê com a key de criador pelo presets_vps.py do /ogab (só no
Mac do dono, fora do git).

  python3 relatos_rick.py fila                       # só os itens RICK_ da fila (erros em relatos/, presets em presets/)
  python3 relatos_rick.py puxar                      # baixa e remonta em ~/.claude/orick_relatos_vps para tratar
  python3 relatos_rick.py apagar <path>              # tira da VPS o que já foi tratado (path exato da fila)
  python3 relatos_rick.py resolver <assinatura> <commit> ["nota"]   # marcar como resolvido depois do commit+push
  python3 relatos_rick.py resolvidos
  python3 relatos_rick.py lido                       # fila lida agora (a mesma marca do Gab: libera commits por 3 h)
  python3 relatos_rick.py checar                     # usado pelo pre-commit
  python3 relatos_rick.py hook                       # instala o pre-commit no repo do Rick (commit só depois de ler)

Regra do dono (igual ao Gab): antes de commitar no Rick, ler a fila inteira. Erro: reproduzir, corrigir no repo,
commit+push, `resolver` e `apagar` aquele item. Preset bom: entra em presets/<nome>/ (sem marca de cliente), commit;
preset fraco ou repetido: só apagar da fila.
"""
import json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import relatar_rick as rick

RESOLVIDOS = os.path.expanduser("~/.claude/orick_relatos/resolvidos.json")
DIR_PADRAO = os.path.expanduser("~/.claude/orick_relatos_vps")
HOOK = """#!/bin/sh
# /orick (dono): commit só depois de ler os relatos da fila da VPS. Ver scripts/relatos_rick.py.
python3 "$(git rev-parse --show-toplevel)/scripts/relatos_rick.py" checar || exit 1
"""


def _gab(nome):
    d = rick.ogab_dir()
    if not d:
        raise SystemExit("/ogab não está instalado: a fila dos relatos é lida pelas ferramentas dele")
    sys.path.insert(0, os.path.join(d, "scripts"))
    try:
        return __import__(nome)
    except Exception as e:
        raise SystemExit(f"{nome}.py do /ogab indisponível ({e}): a fila só é lida no Mac do dono (key de criador)")


def _do_rick(path):
    return any(p.upper().startswith("RICK_") or p.upper().startswith("RICK ") for p in path.split("/"))


def itens():
    vps = _gab("presets_vps")
    return [p for p in vps._chamar("/v1/criador/presets")["presets"] if _do_rick(p["path"])]


def fila():
    ps = itens()
    if not ps:
        print("fila do Rick vazia")
    for p in ps:
        print(f"{p['bytes']:>8}  {p['path']}")
    if ps:
        print(f"total: {len(ps)}")
    return ps


def puxar(dirbase):
    vps, gab = _gab("presets_vps"), _gab("relatar")
    ps = itens()
    for p in ps:
        partes = p["path"].split("/")
        destino = os.path.join(dirbase, partes[0], (partes[1] if len(partes) >= 4 else "")[:8], partes[-2])
        os.makedirs(destino, exist_ok=True)
        texto = vps._chamar("/v1/criador/baixar", {"path": p["path"]})["conteudo"]
        if "/relatos/" in "/" + p["path"]:
            open(os.path.join(destino, "relato.txt"), "w", encoding="utf-8").write(texto)
            print(f"relato: {destino}/relato.txt")
            continue
        feitos = gab.desempacotar(texto, destino)
        if not feitos:
            open(os.path.join(destino, "pacote.txt"), "w", encoding="utf-8").write(texto)
        print(f"preset: {destino} ({len(feitos)} arquivo(s))")
    print(f"\n{len(ps)} item(ns) do Rick em {dirbase}" if ps else "fila do Rick vazia")


def apagar(path):
    _gab("presets_vps").apagar(path)


def resolvidos():
    try:
        return json.load(open(RESOLVIDOS, encoding="utf-8"))
    except Exception:
        return {}


def resolver(assinatura, commit, nota=""):
    r = resolvidos(); r[assinatura] = {"commit": commit, "nota": nota, "quando": time.strftime("%Y-%m-%d")}
    os.makedirs(os.path.dirname(RESOLVIDOS), exist_ok=True)
    json.dump(r, open(RESOLVIDOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return r[assinatura]


def hook():
    destino = os.path.join(rick.SKILL, ".git", "hooks", "pre-commit")
    open(destino, "w").write(HOOK); os.chmod(destino, 0o755)
    return destino


if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = a[0] if a else ""
    if cmd == "fila":
        fila()
    elif cmd == "puxar":
        puxar(a[a.index("--dir") + 1] if "--dir" in a else DIR_PADRAO)
    elif cmd == "apagar" and len(a) > 1:
        apagar(a[1])
    elif cmd == "resolver" and len(a) >= 3:
        print(resolver(a[1], a[2], a[3] if len(a) > 3 else ""))
    elif cmd == "resolvidos":
        print(json.dumps(resolvidos(), ensure_ascii=False, indent=1))
    elif cmd in ("lido", "checar"):
        g = _gab("relatos")
        if cmd == "lido":
            g.lido(); print("leitura marcada (vale para o Gab e o Rick por", g.LEITURA_VALE, "h)")
        else:
            sys.exit(0 if g.checar() else 1)
    elif cmd == "hook":
        print("pre-commit instalado:", hook())
    else:
        raise SystemExit(__doc__)
