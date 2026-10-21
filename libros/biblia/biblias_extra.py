#!/usr/bin/env python3
"""Versiones extra de la Biblia (dominio público o licencia libre) para el lector de la app.

Salida (además de lo que ya genera biblia_a_json.py para la versión principal de cada idioma):
    <destino>/v/<id>/<n>.json      {"n":1,"nombre":"Génesis","caps":[[...], ...]}
    <destino>/versiones.json       lista de todas las versiones (incluidas las principales)
"""
import json, os, re, sys, glob, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from biblia_a_json import leer_osis, NOMBRES, USFX  # noqa: E402

SRC = "/home/claude/scrollmapper"
BDB = "/home/claude/biblias_src"
sys.path.insert(0, "/home/claude/conv")
from diodati import limpiar_diodati  # noqa: E402

# id, idioma, sigla, nombre, año, licencia, crédito, tipo, origen
VERSIONES = [
    # principales (ya publicadas en <idioma>/<n>.json)
    ("rv1909", "es", "RV1909", "Reina-Valera 1909", 1909, "Dominio público", "", "principal", "es"),
    ("kjv", "en", "KJV", "King James Version", 1611, "Public domain", "", "principal", "en"),
    ("riveduta", "it", "RIV", "Riveduta (Luzzi)", 1927, "Pubblico dominio", "", "principal", "it"),
    ("ostervald", "fr", "OST", "Ostervald", 1996, "Domaine public", "", "principal", "fr"),
    ("luther1912", "de", "LUT1912", "Luther 1912", 1912, "Gemeinfrei", "", "principal", "de"),
    ("almeida", "pt", "ALM", "Almeida", 1911, "Domínio público", "", "principal", "pt"),
    # español
    ("rv1865", "es", "RV1865", "Reina-Valera 1865", 1865, "Dominio público", "", "bdb", "SpaRV1865"),
    ("bes", "es", "BES", "La Biblia en Español Sencillo", 2022, "CC BY 4.0", "AudioBiblia.org / Irma Flores", "usfx", "spa-bes.usfx.xml"),
    ("vbl", "es", "VBL", "Versión Biblia Libre", 2022, "CC BY-SA 4.0", "Jonathan Gallagher", "usfx", "spa-vbl.usfx.xml"),
    ("pdpt", "es", "PDPT", "Palabra de Dios para ti", 2022, "CC BY-SA 4.0", "Bible League International", "usfx", "spa-pddpt.usfx.xml"),
    ("platense", "es", "BPL", "Biblia Platense (Straubinger)", 1951, "Dominio público", "", "bdb", "SpaPlatense"),
    # inglés
    ("web", "en", "WEB", "World English Bible", 2020, "Public domain", "", "usfx", "eng-web.usfx.xml"),
    ("bsb", "en", "BSB", "Berean Standard Bible", 2022, "Public domain (CC0)", "", "bdb", "BSB"),
    ("asv", "en", "ASV", "American Standard Version", 1901, "Public domain", "", "bdb", "ASV"),
    ("nheb", "en", "NHEB", "New Heart English Bible", 2020, "Public domain", "", "bdb", "NHEB"),
    ("ylt", "en", "YLT", "Young's Literal Translation", 1898, "Public domain", "", "bdb", "YLT"),
    ("darby", "en", "DBY", "Darby Bible", 1890, "Public domain", "", "bdb", "Darby"),
    ("drc", "en", "DRC", "Douay-Rheims (Challoner)", 1752, "Public domain", "", "bdb", "DRC"),
    ("bbe", "en", "BBE", "Bible in Basic English", 1964, "Public domain", "", "bdb", "BBE"),
    ("webster", "en", "WBT", "Webster Bible", 1833, "Public domain", "", "bdb", "Webster"),
    ("geneva", "en", "GNV", "Geneva Bible", 1599, "Public domain", "", "bdb", "Geneva1599"),
    # italiano
    ("diodati", "it", "DIO", "Diodati", 1885, "Pubblico dominio", "", "diodati", "it-db1885"),
    # francés
    ("martin", "fr", "MAR", "David Martin", 1744, "Domaine public", "", "bdb", "FreBDM1744"),
    ("darbyfr", "fr", "JND", "Darby (français)", 1885, "Domaine public", "", "bdb", "FreJND"),
    ("crampon", "fr", "CRA", "Crampon", 1923, "Domaine public", "", "bdb", "FreCrampon"),
    # alemán
    ("luther1545", "de", "LUT1545", "Luther 1545", 1545, "Gemeinfrei", "", "bdb", "GerBoLut"),
    ("elb1905", "de", "ELB1905", "Elberfelder 1905", 1905, "Gemeinfrei", "", "bdb", "GerElb1905"),
    ("elb1871", "de", "ELB1871", "Elberfelder 1871", 1871, "Gemeinfrei", "", "bdb", "GerElb1871"),
    ("menge", "de", "MENGE", "Menge-Bibel", 1939, "Gemeinfrei", "", "bdb", "GerMenge"),
    ("zurcher", "de", "ZUR", "Zürcher Bibel", 1931, "Gemeinfrei", "", "bdb", "GerZurcher"),
    ("textbibel", "de", "TXT", "Textbibel (Kautzsch/Weizsäcker)", 1906, "Gemeinfrei", "", "bdb", "GerTextbibel"),
    ("gruenewald", "de", "GRU", "Grünewald-Bibel", 1924, "Gemeinfrei", "", "bdb", "GerGruenewald"),
    # portugués
    ("blivre", "pt", "BLIVRE", "Bíblia Livre", 2018, "CC BY 3.0 BR", "Diego Santos, Mario Sérgio e Marco Teles", "bdb", "PorBLivre"),
    ("blivretr", "pt", "BLTR", "Bíblia Livre (Textus Receptus)", 2018, "CC BY 3.0 BR", "Diego Santos, Mario Sérgio e Marco Teles", "bdb", "PorBLivreTR"),
    ("nva", "pt", "NVA", "Nova Versão de Acesso Livre", 2020, "CC BY-SA 4.0", "Diego Santos e Marco Teles", "bdb", "PorNVA"),
]

BDB_NOMBRES = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "I Samuel", "II Samuel",
               "I Kings", "II Kings", "I Chronicles", "II Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
               "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
               "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark",
               "Luke", "John", "Acts", "Romans", "I Corinthians", "II Corinthians", "Galatians", "Ephesians", "Philippians",
               "Colossians", "I Thessalonians", "II Thessalonians", "I Timothy", "II Timothy", "Titus", "Philemon", "Hebrews",
               "James", "I Peter", "II Peter", "I John", "II John", "III John", "Jude", "Revelation of John"]
BDB_ALIAS = {"Revelation": 66, "Song of Songs": 22, "Canticles": 22, "Psalm": 19}

DIODATI_LIBROS = ("genesi esodo levitico numeri deuteronomio giosuè giudici rut isamuele iisamuele ire iire icroniche iicroniche "
                  "esdra neemia ester giobbe salmi proverbi ecclesiaste canticodei~cantici isaia geremia lamentazioni ezechiele "
                  "daniele osea gioele amos abdia giona michea nahum abacuc sofonia aggeo zaccaria malachia evangelodis.matteo "
                  "evangelodis.marco evangelodis.luca evangelodis.giovanni fattidegliapostoli epistoladis.paoloa'~romani "
                  "epistoladis.paoloia'~corinti epistoladis.paoloiia'~corinti epistoladis.paoloa'~galati epistoladis.paoloagliefesi "
                  "epistoladis.paoloa'~filippesi epistoladis.paoloa'~colossesi epistoladis.paoloia'~tessalonicesi "
                  "epistoladis.paoloiia'~tessalonicesi epistoladis.paoloiatimoteo epistoladis.paoloiiatimoteo epistoladis.paoloatito "
                  "epistoladis.paoloafilemone epistolaagliebrei epistoladis.giacomo epistolaidis.pietro epistolaiidis.pietro "
                  "epistolaidis.giovanni epistolaiidis.giovanni epistolaiiidis.giovanni epistoladis.giuda apocalisse").split()


def limpiar(t):
    t = re.sub(r"<(note|f|x|fe)\b.*?</\1>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = t.translate({0x91: "‘", 0x92: "’", 0x93: "“", 0x94: "”", 0x96: "–", 0x97: "—", 0x85: "…"})
    t = re.sub(r"\[\d+\]|\{[^}]*\}", "", t)   # marcas de notas que quedan sueltas
    return re.sub(r"\s+", " ", t).strip()


def leer_usfx2(s):
    out = {}
    for mb in re.finditer(r'<book id="(\w+)">(.*?)</book>', s, re.S):
        if mb.group(1) not in USFX:
            continue
        n = USFX.index(mb.group(1)) + 1
        cuerpo = re.sub(r"<(h|toc|id|s|ms|mt|d|r|f|x|fe|note|rem|ide)\b[^>]*>.*?</\1>", "", mb.group(2), flags=re.S)
        cuerpo = re.sub(r"<(?:id|toc|h|s|d|r)\b[^>]*/>", "", cuerpo)
        cap, vers = 0, None
        for tok in re.split(r'(<c id="\d+"\s*/>|<v id="[\d\-]+"[^>]*/>|<ve\s*/>)', cuerpo):
            mc = re.match(r'<c id="(\d+)"', tok)
            if mc:
                cap, vers = int(mc.group(1)), None
                continue
            mv = re.match(r'<v id="(\d+)', tok)
            if mv:
                vers = int(mv.group(1))
                out.setdefault(n, {}).setdefault(cap, {}).setdefault(vers, "")
                continue
            if tok.startswith("<ve"):
                vers = None
                continue
            if cap and vers:
                out[n][cap][vers] += tok
        for c in out.get(n, {}).values():
            for v in c:
                c[v] = limpiar(c[v])
    return out


def leer_bdb(nombre):
    d = json.load(open(os.path.join(BDB, nombre + ".json"), encoding="utf-8"))
    out = {}
    for b in d["books"]:
        n = BDB_NOMBRES.index(b["name"]) + 1 if b["name"] in BDB_NOMBRES else BDB_ALIAS.get(b["name"])
        if not n:
            continue
        for ch in b["chapters"]:
            for v in ch["verses"]:
                out.setdefault(n, {}).setdefault(int(ch["chapter"]), {})[int(v["verse"])] = limpiar(v["text"])
    return out


def leer_diodati(carpeta):
    out = {}
    base = os.path.join(SRC, "wldeh_bible-api/bibles", carpeta, "books")
    for i, lib in enumerate(DIODATI_LIBROS):
        for f in glob.glob(os.path.join(base, lib, "chapters", "*.json")):
            for v in json.load(open(f, encoding="utf-8"))["data"]:
                c, vv = int(v["chapter"]), int(v["verse"])
                out.setdefault(i + 1, {}).setdefault(c, {})[vv] = limpiar(limpiar_diodati(v["text"], v["chapter"], v["verse"]))
    return out


def arreglar(vid, t):
    t = re.sub(r"^[*¶]\s*|\s*¶\s*", " ", t).strip()          # marcas de párrafo
    t = re.sub(r"(?<=\s)\*(?=\S)", "", t)
    if vid == "darby":
        t = re.sub(r"(?<=[a-z])(?=God)", " ", t)              # "ofGod" -> "of God" (error de la fuente)
    if vid == "darbyfr":
        t = re.sub(r"([’'])\s+(?=[A-ZÉÈÀa-zéèàêîô])", r"\1", t)  # "l’ Éternel" -> "l’Éternel"
    return re.sub(r"\s{2,}", " ", t).strip()


def a_caps(b):
    caps = []
    for c in range(1, (max(b) if b else 0) + 1):
        vs = b.get(c, {})
        caps.append([vs.get(v, "") for v in range(1, (max(vs) if vs else 0) + 1)])
    return caps


def main(destino):
    lista = []
    for vid, lang, sigla, nombre, anio, lic, cred, tipo, origen in VERSIONES:
        nombres = NOMBRES[lang].split("|")
        if tipo == "principal":
            caps = []
            for n in range(1, 67):
                d = json.load(open(os.path.join(destino, origen, f"{n}.json"), encoding="utf-8"))
                caps.append(len(d["caps"]))
            ruta = origen
        else:
            if tipo == "bdb":
                datos = leer_bdb(origen)
            elif tipo == "usfx":
                datos = leer_usfx2(open(os.path.join(SRC, "open-bibles", origen), encoding="utf-8").read())
            elif tipo == "osis":
                datos = leer_osis(open(os.path.join(SRC, "open-bibles", origen), encoding="utf-8").read())
            else:
                datos = leer_diodati(origen)
            for b in datos.values():
                for c in b.values():
                    for v in c:
                        c[v] = arreglar(vid, c[v])
            ruta = f"v/{vid}"
            os.makedirs(os.path.join(destino, ruta), exist_ok=True)
            caps = []
            for n in range(1, 67):
                cc = a_caps(datos.get(n, {}))
                caps.append(len(cc))
                if cc:
                    with open(os.path.join(destino, ruta, f"{n}.json"), "w", encoding="utf-8") as fo:
                        json.dump({"n": n, "nombre": nombres[n - 1], "caps": cc}, fo, ensure_ascii=False, separators=(",", ":"))
        faltan = [n for n in range(1, 67) if not caps[n - 1]]
        versos = 0
        if tipo != "principal":
            versos = sum(1 for b in datos.values() for c in b.values() for v in c.values() if v)
        print(f"{vid:12} {lang} libros: {66 - len(faltan):2}  versículos: {versos:6}  faltan: {faltan[:10]}{'…' if len(faltan) > 10 else ''}")
        lista.append({"id": vid, "idioma": lang, "sigla": sigla, "nombre": nombre, "anio": anio, "licencia": lic,
                      "credito": cred, "ruta": ruta, "capitulos": caps})
    with open(os.path.join(destino, "versiones.json"), "w", encoding="utf-8") as fo:
        json.dump({"versiones": lista}, fo, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main(sys.argv[1])
