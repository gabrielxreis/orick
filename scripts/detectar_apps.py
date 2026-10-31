"""Detecta onde o Rick pode trabalhar nesta máquina e guarda o motor que o usuário escolheu (config.json, fora do git).

  python3 detectar_apps.py detectar          # o que tem instalado + recomendação (JSON); grava em config.json "apps"
  python3 detectar_apps.py escolher <motor>  # photoshop | canva | ia  (grava "motor" no config.json)
  python3 detectar_apps.py status            # motor escolhido e apps detectados

Motores:
  photoshop  PSD em camadas editáveis montado pelo Rick (precisa do Adobe Photoshop, de preferência 2026, no Mac)
  canva      design no Canva (conector oficial do Canva no Claude, ou o Canva no navegador/app) a partir do que o Rick prepara
  ia         peça inteira gerada por IA de imagem (ChatGPT, Gemini/Nano Banana ou IA conectada), sem editor

Nada aqui é obrigatório: sem Photoshop o Rick funciona com Canva ou só IA. A detecção só serve para sugerir.
"""
import glob, json, os, platform, re, sys, time

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(SKILL, "config.json")
MOTORES = ("photoshop", "canva", "ia")
IAS_CONECTADAS = ("higgsfield", "magnific", "artlist", "freepik", "krea", "wonda", "leonardo", "midjourney", "ideogram",
                  "flux", "replicate", "fal", "openai", "gemini", "runway", "recraft")
WIN = platform.system() == "Windows"


def _config():
    try:
        return json.load(open(CONFIG, encoding="utf-8"))
    except Exception:
        return {}


def _salvar(c):
    json.dump(c, open(CONFIG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def _apps_mac(padroes):
    achados = []
    for base in ("/Applications", os.path.expanduser("~/Applications")):
        for p in padroes:
            achados += glob.glob(os.path.join(base, p))
    return sorted(set(achados))


def _apps_win(padroes):
    bases = [os.environ.get(v, "") for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]
    achados = []
    for b in filter(None, bases):
        for p in padroes:
            achados += glob.glob(os.path.join(b, p))
    return sorted(set(achados))


def photoshop():
    if WIN:
        achados = _apps_win([r"Adobe\Adobe Photoshop*\Photoshop.exe"])
    else:
        achados = _apps_mac(["Adobe Photoshop*/Adobe Photoshop*.app", "Adobe Photoshop*.app"])
    versoes = []
    for a in achados:
        m = re.search(r"Photoshop (\d{4}|CC \d{4}|\d+)", a)
        versoes.append(m.group(1) if m else "?")
    return {"instalado": bool(achados), "versoes": sorted(set(versoes)), "caminhos": achados,
            "agente_nativo": any(v.isdigit() and int(v) >= 2026 for v in versoes)}


def _textos_config_claude():
    """Configurações do Claude Code onde aparecem conectores (MCP) e plugins. Só leitura, só para sugerir."""
    arqs = [os.path.expanduser("~/.claude.json"), os.path.expanduser("~/.claude/settings.json"),
            os.path.expanduser("~/.claude/settings.local.json")]
    arqs += glob.glob(os.path.expanduser("~/.claude/plugins/*.json"))
    arqs += [a for a in glob.glob(os.path.expanduser("~/.claude/plugins/**/.mcp.json"), recursive=True)
             if "/.trash/" not in a.replace("\\", "/")]   # conectores que vêm dentro de plugins (ex.: Canva no "marketing")
    out = ""
    for a in arqs:
        try:
            d = json.load(open(a, encoding="utf-8"))
        except Exception:
            continue
        for chave in ("mcpServers", "enabledPlugins"):   # só nomes, nunca tokens
            v = d.get(chave)
            if isinstance(v, dict):
                out += " " + " ".join(v.keys())
        for proj in (d.get("projects") or {}).values():
            if isinstance(proj, dict) and isinstance(proj.get("mcpServers"), dict):
                out += " " + " ".join(proj["mcpServers"].keys())
    return out.lower()


def canva(conf):
    app = _apps_win([r"Programs\Canva\Canva.exe", r"Canva\Canva.exe"]) if WIN else _apps_mac(["Canva.app"])
    return {"app": bool(app), "conector": "canva" in conf, "navegador": True}


def ia(conf):
    app = (_apps_win([r"Programs\ChatGPT\ChatGPT.exe", r"WindowsApps\*ChatGPT*"]) if WIN
           else _apps_mac(["ChatGPT*.app"]))
    return {"chatgpt_app": bool(app), "navegador": ["chatgpt.com", "gemini.google.com"],
            "conectadas": sorted({n for n in IAS_CONECTADAS if n in conf})}


def detectar():
    conf = _textos_config_claude()
    r = {"sistema": platform.system(), "photoshop": photoshop(), "canva": canva(conf), "ia": ia(conf)}
    if r["photoshop"]["instalado"] and not WIN:
        rec, porque = "photoshop", "Photoshop instalado: PSD em camadas editáveis"
    elif r["photoshop"]["instalado"]:
        rec, porque = "ia", "Photoshop no Windows ainda não é controlado pelo Rick (só Mac); IA ou Canva por enquanto"
    elif r["canva"]["app"] or r["canva"]["conector"]:
        rec, porque = "canva", "sem Photoshop; Canva " + ("conectado no Claude" if r["canva"]["conector"] else "instalado")
    else:
        rec, porque = "ia", "sem Photoshop nem Canva: IA de imagem no navegador funciona em qualquer máquina"
    r["recomendado"], r["porque"] = rec, porque
    c = _config(); c["apps"] = dict(r, quando=time.strftime("%Y-%m-%d")); _salvar(c)
    return r


def escolher(motor):
    motor = motor.lower().strip()
    if motor not in MOTORES:
        raise SystemExit(f"motor inválido: {motor} (use {' | '.join(MOTORES)})")
    c = _config(); c["motor"] = motor; c["motor_respondido"] = time.strftime("%Y-%m-%d"); _salvar(c)
    aviso = ""
    if motor == "photoshop" and not ((c.get("apps") or {}).get("photoshop") or {}).get("instalado"):
        aviso = " (Photoshop não foi encontrado: o Rick prepara tudo, mas para montar o PSD precisa instalar)"
    return motor + aviso


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["detectar"]:
        print(json.dumps(detectar(), ensure_ascii=False, indent=1))
    elif a[:1] == ["escolher"] and len(a) > 1:
        print("motor:", escolher(a[1]))
    elif a[:1] == ["status"]:
        c = _config()
        print(json.dumps({"motor": c.get("motor") or "ainda não escolhido", "apps": c.get("apps") or "não detectado"},
                         ensure_ascii=False, indent=1))
    else:
        raise SystemExit(__doc__)
