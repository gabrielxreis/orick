"""Relatos do Rick: erros que o Rick corrigiu nesta máquina e presets de design novos que o usuário criou vão, ANÔNIMOS,
para a MESMA fila da VPS do Gabriel que recebe os relatos do Gab (/v1/preset, com a key de licença do /ogab).

  python3 relatar_rick.py registrar --titulo "..." --erro "..." --causa "..." --correcao "..." [--arquivo scripts/x.py ...]
  python3 relatar_rick.py preset <presets/nome>   # registra um preset novo (estrutura, sem textos nem fotos do cliente)
  python3 relatar_rick.py varrer                  # acha os presets que ESTE usuário criou (presets/<nome>/ fora do git)
                                                  # e as INVENÇÕES na skill: scripts e docs novos, melhorias nos arquivos
                                                  # (git diff) e o que ficou guardado em stash no Passo zero
  python3 relatar_rick.py enviar                  # varre + manda os pendentes (Passo zero, em segundo plano)
  python3 relatar_rick.py status                  # consentimento, pendentes e enviados

Usa o canal do Gab: precisa do /ogab instalado (licenca.py e a key) e do consentimento dele ("relatos": true no
config.json do /ogab, que vem do aceite dos termos). Sem /ogab, sem key ou sem consentimento nada sai da máquina
(fica em ~/.claude/orick_relatos/pendentes). Na máquina do dono ("dono_biblioteca": true no /ogab) não envia.
Tudo chega na fila com o nome começando por "RICK " (na VPS vira RICK_...), para o dono separar do que é do Gab.
Anonimização é a do Gab (caminhos, e-mails, chaves, nome do usuário e dos clientes); aqui também saem os nomes das
marcas em clientes/ e na pasta de saída do Rick. Preset vai como pacote de texto (README.md, preset.json, .jsx);
imagem e PSD vão só pelo nome. Destino: SÓ a fila da VPS (nunca planilha, formulário, Drive, e-mail).
"""
import glob, hashlib, json, os, platform, re, subprocess, sys, time

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.expanduser("~/.claude/orick_relatos")
PEND, ENV = os.path.join(PASTA, "pendentes"), os.path.join(PASTA, "enviados")
VARRIDOS = os.path.join(PASTA, "presets_vistos.json")
PREFIXO = "RICK "
TEXTO = (".md", ".json", ".jsx", ".js", ".py", ".txt", ".css", ".html")
# invenções: o que o usuário (ou o Claude dele) criou/melhorou na skill. Fica de fora o que é dele ou da máquina.
EXT_INVENCAO = TEXTO + (".sh", ".ps1", ".swift", ".mjs")
FORA_INVENCAO = ("presets/", "clientes/", "config.json", ".venv/", "docs/catalogo/local/", "scripts/swift/ocr")
TEMP_INVENCAO = re.compile(r"(^|/)(_?tmp|_?temp|_?cache|__pycache__)(/|$)|\.parcial$", re.I)
MIN_LINHAS_INVENCAO = 6   # menos que isso é ajuste, não invenção
LIMITE_ARQ = 40000
LIMITE_PARTE, PARTES_MAX = 45000, 6


def ogab_dir():
    for d in (os.environ.get("OGAB_DIR", ""), "~/.claude/skills/ogab", "~/.agents/skills/ogab"):
        d = os.path.expanduser(d)
        if d and os.path.exists(os.path.join(d, "scripts", "relatar.py")):
            return d
    return None


def _gab():
    """Módulos relatar e licenca do /ogab (o canal é o mesmo). None se o /ogab não estiver instalado."""
    d = ogab_dir()
    if not d:
        return None, None
    sys.path.insert(0, os.path.join(d, "scripts"))
    try:
        import relatar as gab, licenca
        return gab, licenca
    except Exception:
        return None, None


def _versao():
    try:
        return subprocess.run(["git", "-C", SKILL, "log", "-1", "--format=%h %cs"], capture_output=True, text=True,
                              timeout=10).stdout.strip() or "?"
    except Exception:
        return "?"


def _nomes(gab):
    cfg = gab._config() if gab else {}
    nomes = set(gab._nomes_privados(cfg)) if gab else set()
    for d in glob.glob(os.path.join(SKILL, "clientes", "*")):
        if os.path.isdir(d) and not os.path.basename(d).startswith(("_", ".")):
            nomes.add(os.path.basename(d))
    nomes.add(os.path.basename(os.path.expanduser("~")))
    return sorted((n for n in nomes if n and len(n) >= 3), key=len, reverse=True)


def _anon(txt, gab, nomes):
    t = str(txt or "").replace(SKILL, "SKILL_DIR")
    if gab:
        return gab.anonimizar(t, nomes)
    t = t.replace(os.path.expanduser("~"), "~")
    for n in nomes:
        t = re.sub(re.escape(n), "<cliente>", t, flags=re.I)
    return t


def _gravar(rel):
    os.makedirs(PEND, exist_ok=True)
    arq = os.path.join(PEND, f"{time.strftime('%Y%m%d-%H%M%S')}-{rel['assinatura']}.json")
    json.dump(rel, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return arq


def registrar(titulo, erro, causa="", correcao="", arquivos=()):
    gab, _ = _gab(); nomes = _nomes(gab); diff = ""
    if arquivos:
        diff = subprocess.run(["git", "-C", SKILL, "diff", "--"] + list(arquivos), capture_output=True, text=True).stdout
    rel = {"tipo": "bug", "titulo": titulo, "erro": erro, "causa": causa, "correcao": correcao, "diff": diff}
    for k, lim in {"titulo": 200, "erro": 3000, "causa": 2000, "correcao": 3000, "diff": 15000}.items():
        rel[k] = _anon(rel[k], gab, nomes)[:lim]
    assin = gab._assinatura(rel["erro"] or rel["titulo"]) if gab else hashlib.sha1(rel["erro"].encode()).hexdigest()[:10]
    rel.update({"assinatura": assin, "versao": _versao(), "skill": "orick",
                "sistema": f"{platform.system()} {platform.release()} {platform.machine()}",
                "quando": time.strftime("%Y-%m-%dT%H:%M:%S")})
    return _gravar(rel)


def _pacote(pasta, gab, nomes):
    """Pacote no formato que o `relatar.py desempacotar` do Gab lê (cabeçalho RICK)."""
    blocos, fora, manifesto = [], [], {}
    for arq in sorted(glob.glob(os.path.join(pasta, "**", "*"), recursive=True)):
        if not os.path.isfile(arq) or os.path.basename(arq).startswith("."):
            continue
        rel = os.path.relpath(arq, pasta)
        if not arq.lower().endswith(TEXTO):
            fora.append(f"{_anon(rel, gab, nomes)} ({os.path.getsize(arq) // 1024} KB, vai pelo nome)")
            continue
        txt = open(arq, encoding="utf-8", errors="replace").read()
        txt = re.sub(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+", "data:<removido>", txt)
        txt = _anon(txt, gab, nomes); rel = _anon(rel, gab, nomes)
        manifesto[rel] = hashlib.sha1(txt.encode()).hexdigest()
        blocos.append(f"--- arquivo: {rel} ---\n{txt}\n")
    if not blocos:
        raise ValueError("preset sem arquivo de texto (README.md / preset.json)")
    blocos.append("--- manifesto ---\n" + json.dumps({"arquivos": manifesto, "por_nome": fora}, ensure_ascii=False) + "\n")
    partes, atual = [], ""
    for b in blocos:
        while b:
            if len(atual) + len(b) <= LIMITE_PARTE - 300:
                atual += b; b = ""
            elif atual:
                partes.append(atual); atual = ""
            else:
                corte = LIMITE_PARTE - 300
                atual, b = b[:corte], "--- continua ---\n" + b[corte:]
    if atual:
        partes.append(atual)
    if len(partes) > PARTES_MAX:
        raise ValueError(f"preset grande demais ({len(partes)} partes, limite {PARTES_MAX})")
    return [f"=== PACOTE RICK ogab v1 parte {i}/{len(partes)} ===\n{p}" for i, p in enumerate(partes, 1)]


def registrar_preset(pasta):
    gab, _ = _gab(); nomes = _nomes(gab); pasta = os.path.abspath(pasta)
    nome = _anon(os.path.basename(pasta.rstrip("/")), gab, nomes)
    pacote = _pacote(pasta, gab, nomes)
    rel = {"tipo": "preset", "titulo": nome, "diff": "\n".join(pacote), "skill": "orick", "versao": _versao(),
           "assinatura": hashlib.sha1(("orick:" + nome).encode()).hexdigest()[:10],
           "quando": time.strftime("%Y-%m-%dT%H:%M:%S")}
    return _gravar(rel)


def _impressao(pasta):
    h = hashlib.sha1()
    for a in sorted(glob.glob(os.path.join(pasta, "**", "*"), recursive=True)):
        if os.path.isfile(a):
            h.update(a.encode()); h.update(str(os.path.getsize(a)).encode()); h.update(str(int(os.path.getmtime(a))).encode())
    return h.hexdigest()[:16]


def _presets_do_usuario():
    """presets/<nome>/ que não vieram do git (o usuário criou nesta máquina)."""
    try:
        out = subprocess.run(["git", "-C", SKILL, "ls-files", "presets"], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return []
    rastreados = {l.split("/")[1] for l in out.splitlines() if l.count("/") >= 2}
    return [d.rstrip("/") for d in sorted(glob.glob(os.path.join(SKILL, "presets", "*", "")))
            if os.path.basename(d.rstrip("/")) not in rastreados]


def varrer():
    gab, _ = _gab()
    if gab and gab._config().get("dono_biblioteca"):
        return []   # o dono publica direto
    try:
        vistos = json.load(open(VARRIDOS, encoding="utf-8"))
    except Exception:
        vistos = {}
    feitos = []
    for pasta in _presets_do_usuario():
        chave, imp = os.path.relpath(pasta, SKILL), _impressao(pasta)
        if vistos.get(chave) == imp:
            continue
        try:
            res = registrar_preset(pasta)
        except Exception as e:
            res = f"não registrado: {e}"
        vistos[chave] = imp; feitos.append((chave, res))
    if feitos:
        os.makedirs(PASTA, exist_ok=True)
        json.dump(vistos, open(VARRIDOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    try:
        inv = registrar_invencoes()
    except Exception as e:
        inv = []; feitos.append(("invenções na skill", f"erro: {e}"))
    if inv:
        feitos.append(("invenções na skill", f"{len(inv)} parte(s) registrada(s)"))
    return feitos


def _git(*args):
    r = subprocess.run(["git", "-C", SKILL, *args], capture_output=True, text=True, timeout=60)
    return r.stdout if r.returncode == 0 else ""


def _nosso(rel, blob):
    """Blob que já passou pelo repo (qualquer commit; o stash não conta): não é invenção do usuário."""
    return bool(blob) and any(l.split(" ", 1)[0] == blob for l in
                              _git("rev-list", "--objects", "--branches", "--tags", "--remotes", "--", rel).splitlines())


def _fora(rel):
    return rel.startswith(FORA_INVENCAO) or TEMP_INVENCAO.search(rel) or not rel.endswith(EXT_INVENCAO)


def _blocos_invencao():
    """[(rótulo, texto)] do que este usuário criou ou melhorou na skill (presets vão pelo varrer de presets)."""
    blocos = []
    for rel in sorted(_git("ls-files", "--others", "--exclude-standard").splitlines()):
        f = os.path.join(SKILL, rel)
        if _fora(rel) or os.path.getsize(f) > 200_000 or _nosso(rel, _git("hash-object", f).strip()):
            continue
        try:
            blocos.append((f"arquivo novo: {rel}", open(f, encoding="utf-8").read()))
        except Exception:
            pass
    mudados = [r for r in _git("diff", "HEAD", "--name-only").splitlines()
               if r and not _fora(r) and not _nosso(r, _git("hash-object", os.path.join(SKILL, r)).strip())]
    d = _git("diff", "HEAD", "--", *mudados) if mudados else ""
    if d.strip():
        blocos.append(("melhorias nos arquivos da skill (git diff)", d))
    for linha in _git("stash", "list").splitlines():   # Passo zero guarda as mudanças locais antes do pull
        ref = linha.split(":", 1)[0]
        nomes = (_git("stash", "show", "--name-only", "--include-untracked", ref) or _git("stash", "show", "--name-only", ref)).split()
        seus = [r for r in nomes if not _fora(r) and not _nosso(r, (_git("rev-parse", f"{ref}:{r}") or _git("rev-parse", f"{ref}^3:{r}")).strip())]
        if not seus:
            continue
        sd = _git("diff", f"{ref}^1", ref, "--", *seus)   # `git stash show` não aceita filtro de arquivo
        for r in seus:
            novo = _git("show", f"{ref}^3:{r}") if f"b/{r}" not in sd else ""
            if novo:
                sd += f"\n--- arquivo novo: {r} ---\n{novo}"
        if sd.strip():
            blocos.append((f"guardado em stash antes do update ({ref})", sd))
    return blocos


def registrar_invencoes():
    """Grava em pendentes/ as invenções deste usuário na skill (anonimizadas, em partes). Não repete o mesmo conteúdo."""
    blocos = _blocos_invencao()
    if not blocos or sum(t.count("\n") for _, t in blocos) < MIN_LINHAS_INVENCAO:
        return []
    gab, _ = _gab(); nomes = _nomes(gab); corpo = ""
    for rot, txt in blocos:
        txt = _anon(re.sub(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+", "data:<removido>", txt), gab, nomes)
        if len(txt) > LIMITE_ARQ:
            txt = txt[:LIMITE_ARQ] + f"\n... cortado: {len(txt) - LIMITE_ARQ} caracteres a mais"
        corpo += f"--- {_anon(rot, gab, nomes)} ---\n{txt}\n"
    assin = "inv-" + hashlib.sha1(corpo.encode()).hexdigest()[:10]
    if any(assin in os.path.basename(f) for f in glob.glob(os.path.join(PASTA, "*", "*.json"))):
        return []   # já registrado (pendente ou enviado)
    passo = LIMITE_PARTE - 300
    partes = [corpo[i:i + passo] for i in range(0, len(corpo), passo)][:PARTES_MAX]
    n, saidas = len(partes), []
    os.makedirs(PEND, exist_ok=True); carimbo = time.strftime("%Y%m%d-%H%M%S")
    for i, p_ in enumerate(partes, 1):
        rel = {"tipo": "invencao", "skill": "orick", "assinatura": assin, "versao": _versao(),
               "titulo": f"invenção na skill ({len(blocos)} item(ns))" + (f" (parte {i}/{n})" if n > 1 else ""),
               "erro": _anon("; ".join(r for r, _ in blocos), gab, nomes)[:3000],
               "diff": f"=== PACOTE INVENCAO ogab v1 parte {i}/{n} ===\n{p_}",
               "sistema": f"{platform.system()} {platform.release()} {platform.machine()}",
               "quando": time.strftime("%Y-%m-%dT%H:%M:%S")}
        f = os.path.join(PEND, f"{carimbo}-{assin}" + (f"-p{i}" if n > 1 else "") + ".json")
        json.dump(rel, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1); saidas.append(f)
    return saidas


def _log(msg):
    os.makedirs(PASTA, exist_ok=True)
    with open(os.path.join(PASTA, "envio.log"), "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


def _pode():
    """(gab, licenca, cfg, motivo): só envia com /ogab + key + "relatos": true e fora da máquina do dono."""
    gab, lic = _gab()
    if not gab or not lic:
        return None, None, {}, "sem /ogab instalado (o canal de relatos é o dele)"
    cfg = gab._config()
    if cfg.get("dono_biblioteca"):
        return None, None, cfg, "máquina do dono (corrige direto)"
    if cfg.get("relatos") is not True:
        return None, None, cfg, "sem consentimento de relatos no /ogab"
    if not lic._ler().get("key"):
        return None, None, cfg, "sem key de licença do /ogab"
    return gab, lic, cfg, ""


def enviar():
    gab, lic, cfg, motivo = _pode()
    if motivo:
        return 0
    try:
        for chave, res in varrer():
            _log(f"varredura {chave}: {res}")
    except Exception as e:
        _log(f"varredura falhou: {e}")
    key, maq = lic._ler()["key"], lic.maquina()
    usuario = str((cfg.get("comunidade") or {}).get("nome") or "anon")[:60]
    os.makedirs(ENV, exist_ok=True)
    rot = [("titulo", "titulo"), ("erro", "erro"), ("causa", "causa"), ("correcao", "correcao"),
           ("versao", "versao"), ("sistema", "sistema"), ("diff", "diff")]
    n = 0
    for arq in sorted(glob.glob(os.path.join(PEND, "*.json")))[:40]:
        try:
            rel = json.load(open(arq, encoding="utf-8"))
        except Exception:
            continue
        if rel.get("tipo") == "preset":
            tipo, pacote = "preset", rel.get("diff", "")
        else:
            tipo, pacote = "relato", "[skill] orick\n" + "\n".join(f"[{r}] {rel.get(k, '')}" for k, r in rot if rel.get(k))
        res = lic._post("/v1/preset", {"key": key, "maquina": maq, "usuario": usuario, "tipo": tipo, "pacote": pacote,
                                       "preset": (PREFIXO + (rel.get("titulo") or tipo))[:80]})
        if res is None:
            break   # sem internet: tenta na próxima abertura
        if res.get("status") == "ok":
            os.replace(arq, os.path.join(ENV, os.path.basename(arq))); n += 1
        else:
            _log(f"recusado {os.path.basename(arq)}: {res}")
    if n:
        _log(f"{n} item(ns) enviado(s) para a VPS")
    return n


def status():
    _, _, cfg, motivo = _pode()
    return {"envia": not motivo, "motivo": motivo or "ok", "ogab": ogab_dir() or "não instalado",
            "pendentes": len(glob.glob(os.path.join(PEND, "*.json"))), "enviados": len(glob.glob(os.path.join(ENV, "*.json")))}


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["registrar"]:
        def arg(n, pad=""):
            return a[a.index(n) + 1] if n in a else pad
        arqs = [a[i + 1] for i, x in enumerate(a) if x == "--arquivo" and i + 1 < len(a)]
        print(registrar(arg("--titulo"), arg("--erro"), arg("--causa"), arg("--correcao"), arqs))
    elif a[:1] == ["preset"] and len(a) > 1:
        print(registrar_preset(a[1]))
    elif a[:1] == ["varrer"]:
        for chave, res in varrer() or [("-", "nada novo")]:
            print(f"  {chave}: {res}")
    elif a[:1] == ["enviar"]:
        print(enviar(), "enviado(s)")
    elif a[:1] == ["status"]:
        print(json.dumps(status(), ensure_ascii=False))
    else:
        raise SystemExit(__doc__)
