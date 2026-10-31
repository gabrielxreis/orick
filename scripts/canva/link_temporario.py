"""Link HTTPS público e TEMPORÁRIO de um arquivo, para o Canva importar (import-design-from-url só lê link público).

  python3 link_temporario.py abrir arte.pptx      # sobe no Google Drive do usuário (pasta "Rick - envios para o Canva"),
                                                  # abre "qualquer pessoa com o link" e imprime a URL de download direto
  python3 link_temporario.py fechar <file_id>     # tira o link público (o arquivo fica no Drive, privado)
  python3 link_temporario.py fechar todos         # fecha todos os links que o Rick abriu
  python3 link_temporario.py status

Precisa do `gws` (Google Workspace CLI) logado. Sempre fechar logo depois que o Canva importar: o arquivo pode ter
material de cliente. Sem `gws`: o usuário arrasta o PPTX para o Canva (Criar design > Importar arquivo), mesmo resultado.
"""
import json, os, shutil, subprocess, sys, time

REG = os.path.expanduser("~/.claude/orick_canva_links.json")
PASTA = "Rick - envios para o Canva"


def gws(args, cwd=None):
    if not shutil.which("gws"):
        raise SystemExit("gws não instalado: arraste o PPTX para o Canva (Criar design > Importar arquivo)")
    r = subprocess.run(["gws", *args], capture_output=True, text=True, cwd=cwd)
    out = "\n".join(l for l in r.stdout.splitlines() if not l.startswith("Using keyring"))
    if r.returncode:
        raise SystemExit(f"gws falhou: {(r.stderr or out)[-400:]}")
    return json.loads(out) if out.strip() else {}


def _reg():
    try:
        return json.load(open(REG, encoding="utf-8"))
    except Exception:
        return {}


def _salvar(d):
    json.dump(d, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _pasta():
    q = f'name = "{PASTA}" and mimeType = "application/vnd.google-apps.folder" and "root" in parents and trashed = false'
    fs = gws(["drive", "files", "list", "--params", json.dumps({"q": q, "fields": "files(id)"})]).get("files", [])
    if fs:
        return fs[0]["id"]
    return gws(["drive", "files", "create", "--params", json.dumps({"fields": "id"}),
                "--json", json.dumps({"name": PASTA, "mimeType": "application/vnd.google-apps.folder"})])["id"]


def abrir(arq):
    arq = os.path.abspath(arq)
    f = gws(["drive", "files", "create", "--params", json.dumps({"fields": "id,name,size"}),
             "--json", json.dumps({"name": os.path.basename(arq), "parents": [_pasta()]}),
             "--upload", os.path.basename(arq)], cwd=os.path.dirname(arq))
    p = gws(["drive", "permissions", "create", "--params", json.dumps({"fileId": f["id"], "fields": "id"}),
             "--json", json.dumps({"role": "reader", "type": "anyone"})])
    url = f"https://drive.usercontent.google.com/download?id={f['id']}&export=download&confirm=t"
    d = _reg(); d[f["id"]] = {"nome": f["name"], "permissao": p["id"], "aberto": time.strftime("%Y-%m-%d %H:%M")}; _salvar(d)
    print(json.dumps({"file_id": f["id"], "url": url}, ensure_ascii=False))
    return f["id"], url


def fechar(fid):
    d = _reg()
    ids = list(d) if fid == "todos" else [fid]
    for i in ids:
        perm = (d.get(i) or {}).get("permissao") or "anyoneWithLink"
        try:
            gws(["drive", "permissions", "delete", "--params", json.dumps({"fileId": i, "permissionId": perm})])
            print("link fechado:", i)
        except SystemExit as e:
            print("não fechou", i, str(e)[:120])
            continue
        d.pop(i, None)
    _salvar(d)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["abrir"] and len(a) > 1:
        abrir(a[1])
    elif a[:1] == ["fechar"] and len(a) > 1:
        fechar(a[1])
    elif a[:1] == ["status"]:
        print(json.dumps(_reg(), ensure_ascii=False, indent=1) if _reg() else "nenhum link aberto")
    else:
        raise SystemExit(__doc__)
