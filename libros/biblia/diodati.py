import re
REF = re.compile(r"^(?:\d+(?:[.,\-–—]\d+)*\.?|[1-3]|[A-ZÀ-Ý][a-zà-ÿ]{0,7}\.|(?:ver|vers|rif|ecc|cap|v|vv|cf|ved)\.|ecc|ivi|ivi\.)[,;:.!?)]*$")
def limpiar_diodati(t, c, v):
    marker = f"{c}.{v} "
    guard = 0
    while marker in t and guard < 20:
        guard += 1
        i = t.index(marker)
        toks = list(re.finditer(r"\S+", t[i + len(marker):]))
        if not toks: t = t[:i]; break
        fin = toks[0].end()          # el ancla (palabra repetida)
        k = 1
        if len(toks) > 1 and toks[1].group().startswith("cio"):   # glosa: "cioè: Monte della sconfitta .."
            resto0 = t[i + len(marker):]
            j = resto0.find("..", toks[1].start())
            if j >= 0:
                t = t[:i] + resto0[j + 1:]
                continue
        while k < len(toks):
            tk = toks[k].group()
            sig = toks[k + 1].group() if k + 1 < len(toks) else ""
            if REF.match(tk) or (re.match(r"^[A-ZÀ-Ý][a-zà-ÿ]{1,9}$", tk) and re.match(r"^\d", sig)) or (tk in ("e", "ed") and REF.match(sig) and re.match(r"^([\dA-Z]|rif|ver|ecc)", sig)):
                fin = toks[k].end(); k += 1
            else:
                break
        nota = t[i + len(marker): i + len(marker) + fin]
        resto = t[i + len(marker) + fin:]
        # puntuación original pegada después del punto final de la nota
        m = re.search(r"\.([,;:.!?)]*)$", nota)
        extra = m.group(1) if m and k > 1 else ""
        t = t[:i] + extra + resto
    return re.sub(r"\s+([,;:.!?])", r"\1", re.sub(r"\s{2,}", " ", t)).strip()
