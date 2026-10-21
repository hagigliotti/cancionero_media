#!/usr/bin/env python3
"""Convierte las Biblias de dominio público (open-bibles, formatos OSIS / USFX) a JSON para la app.

Salida:  <destino>/indice.json
         <destino>/<idioma>/<n>.json   (n = 1..66)   {"n":1,"nombre":"Génesis","caps":[["v1","v2",...], ...]}
"""
import json, re, sys, os, html
from collections import Counter

FUENTES = {
    "es": ("spa-rv1909.usfx.xml", "RV1909", "Reina-Valera 1909"),
    "en": ("eng-kjv.osis.xml", "KJV", "King James Version"),
    "it": ("ita-riveduta.osis.xml", "RIV", "Riveduta (Luzzi)"),
    "fr": ("fra-ostervald.osis.xml", "OST", "Ostervald"),
    "de": ("deu-luther1912.osis.xml", "LUT1912", "Luther 1912"),
    "pt": ("por-almeida.usfx.xml", "ALM", "Almeida"),
}

OSIS = ("Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song "
        "Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal Matt Mark Luke John Acts Rom "
        "1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John 2John 3John Jude Rev").split()
USFX = ("GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM EZK "
        "DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH "
        "1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV").split()

NOMBRES = {
    "es": "Génesis|Éxodo|Levítico|Números|Deuteronomio|Josué|Jueces|Rut|1 Samuel|2 Samuel|1 Reyes|2 Reyes|1 Crónicas|2 Crónicas|Esdras|Nehemías|Ester|Job|Salmos|Proverbios|Eclesiastés|Cantares|Isaías|Jeremías|Lamentaciones|Ezequiel|Daniel|Oseas|Joel|Amós|Abdías|Jonás|Miqueas|Nahúm|Habacuc|Sofonías|Hageo|Zacarías|Malaquías|Mateo|Marcos|Lucas|Juan|Hechos|Romanos|1 Corintios|2 Corintios|Gálatas|Efesios|Filipenses|Colosenses|1 Tesalonicenses|2 Tesalonicenses|1 Timoteo|2 Timoteo|Tito|Filemón|Hebreos|Santiago|1 Pedro|2 Pedro|1 Juan|2 Juan|3 Juan|Judas|Apocalipsis",
    "en": "Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1 Samuel|2 Samuel|1 Kings|2 Kings|1 Chronicles|2 Chronicles|Ezra|Nehemiah|Esther|Job|Psalms|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1 Corinthians|2 Corinthians|Galatians|Ephesians|Philippians|Colossians|1 Thessalonians|2 Thessalonians|1 Timothy|2 Timothy|Titus|Philemon|Hebrews|James|1 Peter|2 Peter|1 John|2 John|3 John|Jude|Revelation",
    "it": "Genesi|Esodo|Levitico|Numeri|Deuteronomio|Giosuè|Giudici|Rut|1 Samuele|2 Samuele|1 Re|2 Re|1 Cronache|2 Cronache|Esdra|Neemia|Ester|Giobbe|Salmi|Proverbi|Ecclesiaste|Cantico dei Cantici|Isaia|Geremia|Lamentazioni|Ezechiele|Daniele|Osea|Gioele|Amos|Abdia|Giona|Michea|Nahum|Abacuc|Sofonia|Aggeo|Zaccaria|Malachia|Matteo|Marco|Luca|Giovanni|Atti|Romani|1 Corinzi|2 Corinzi|Galati|Efesini|Filippesi|Colossesi|1 Tessalonicesi|2 Tessalonicesi|1 Timoteo|2 Timoteo|Tito|Filemone|Ebrei|Giacomo|1 Pietro|2 Pietro|1 Giovanni|2 Giovanni|3 Giovanni|Giuda|Apocalisse",
    "fr": "Genèse|Exode|Lévitique|Nombres|Deutéronome|Josué|Juges|Ruth|1 Samuel|2 Samuel|1 Rois|2 Rois|1 Chroniques|2 Chroniques|Esdras|Néhémie|Esther|Job|Psaumes|Proverbes|Ecclésiaste|Cantique des cantiques|Ésaïe|Jérémie|Lamentations|Ézéchiel|Daniel|Osée|Joël|Amos|Abdias|Jonas|Michée|Nahum|Habacuc|Sophonie|Aggée|Zacharie|Malachie|Matthieu|Marc|Luc|Jean|Actes|Romains|1 Corinthiens|2 Corinthiens|Galates|Éphésiens|Philippiens|Colossiens|1 Thessaloniciens|2 Thessaloniciens|1 Timothée|2 Timothée|Tite|Philémon|Hébreux|Jacques|1 Pierre|2 Pierre|1 Jean|2 Jean|3 Jean|Jude|Apocalypse",
    "de": "1. Mose|2. Mose|3. Mose|4. Mose|5. Mose|Josua|Richter|Rut|1. Samuel|2. Samuel|1. Könige|2. Könige|1. Chronik|2. Chronik|Esra|Nehemia|Ester|Hiob|Psalmen|Sprüche|Prediger|Hoheslied|Jesaja|Jeremia|Klagelieder|Hesekiel|Daniel|Hosea|Joel|Amos|Obadja|Jona|Micha|Nahum|Habakuk|Zefanja|Haggai|Sacharja|Maleachi|Matthäus|Markus|Lukas|Johannes|Apostelgeschichte|Römer|1. Korinther|2. Korinther|Galater|Epheser|Philipper|Kolosser|1. Thessalonicher|2. Thessalonicher|1. Timotheus|2. Timotheus|Titus|Philemon|Hebräer|Jakobus|1. Petrus|2. Petrus|1. Johannes|2. Johannes|3. Johannes|Judas|Offenbarung",
    "pt": "Gênesis|Êxodo|Levítico|Números|Deuteronômio|Josué|Juízes|Rute|1 Samuel|2 Samuel|1 Reis|2 Reis|1 Crônicas|2 Crônicas|Esdras|Neemias|Ester|Jó|Salmos|Provérbios|Eclesiastes|Cantares|Isaías|Jeremias|Lamentações|Ezequiel|Daniel|Oseias|Joel|Amós|Obadias|Jonas|Miqueias|Naum|Habacuque|Sofonias|Ageu|Zacarias|Malaquias|Mateus|Marcos|Lucas|João|Atos|Romanos|1 Coríntios|2 Coríntios|Gálatas|Efésios|Filipenses|Colossenses|1 Tessalonicenses|2 Tessalonicenses|1 Timóteo|2 Timóteo|Tito|Filemom|Hebreus|Tiago|1 Pedro|2 Pedro|1 João|2 João|3 João|Judas|Apocalipse",
}


def limpiar(t):
    t = re.sub(r"<note\b.*?</note>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    # caracteres de control cp1252 mal convertidos (el archivo italiano trae \x92 en vez de ’)
    t = t.translate({0x91: "‘", 0x92: "’", 0x93: "“", 0x94: "”", 0x96: "–", 0x97: "—", 0x85: "…"})
    return re.sub(r"\s+", " ", t).strip()


def leer_osis(s):
    libros = {}
    # versículos con contenedor (<verse osisID=..>texto</verse>) o con hitos (sID ... eID)
    if re.search(r"<verse[^>]*\bsID=", s):
        partes = re.split(r"(<verse[^>]*/>)", s)
        actual = None
        for p in partes:
            m = re.match(r"<verse[^>]*osisID=[\"']([^\"']+)[\"'][^>]*sID=", p)
            if m:
                actual = m.group(1); libros.setdefault(actual, ""); continue
            if p.startswith("<verse") and "eID" in p:
                actual = None; continue
            if actual:
                libros[actual] += p
    else:
        for m in re.finditer(r"<verse[^>]*osisID=[\"']([^\"']+)[\"'][^>]*>(.*?)</verse>", s, re.S):
            libros[m.group(1)] = m.group(2)
    out = {}
    for oid, txt in libros.items():
        oid = oid.split()[0]
        b, c, v = oid.split(".")[:3]
        if b not in OSIS:
            continue
        out.setdefault(OSIS.index(b) + 1, {}).setdefault(int(c), {})[int(v)] = limpiar(txt)
    return out


def leer_usfx(s):
    out = {}
    for mb in re.finditer(r'<book id="(\w+)">(.*?)</book>', s, re.S):
        if mb.group(1) not in USFX:
            continue
        n = USFX.index(mb.group(1)) + 1
        cuerpo = re.sub(r"<(h|toc)\b[^>]*>.*?</\1>", "", mb.group(2), flags=re.S)
        cuerpo = re.sub(r"<f\b.*?</f>|<x\b.*?</x>", "", cuerpo, flags=re.S)
        cap = 0
        for tok in re.split(r'(<c id="\d+"\s*/>|<v id="\d+"\s*/>|<ve\s*/>)', cuerpo):
            mc = re.match(r'<c id="(\d+)"', tok)
            if mc:
                cap, vers = int(mc.group(1)), None; continue
            mv = re.match(r'<v id="(\d+)"', tok)
            if mv:
                vers = int(mv.group(1)); out.setdefault(n, {}).setdefault(cap, {})[vers] = ""; continue
            if tok.startswith("<ve"):
                vers = None; continue
            if cap and vers:
                out[n][cap][vers] += tok
        for c in out.get(n, {}).values():
            for v in c:
                c[v] = limpiar(c[v])
    return out


def main(src, destino):
    indice = {"versiones": {}, "libros": {}}
    for lang, (archivo, sigla, nombre) in FUENTES.items():
        s = open(os.path.join(src, archivo), encoding="utf-8").read()
        datos = leer_osis(s) if ".osis." in archivo else leer_usfx(s)
        os.makedirs(os.path.join(destino, lang), exist_ok=True)
        nombres = NOMBRES[lang].split("|")
        caps_por_libro = []
        for n in range(1, 67):
            b = datos.get(n, {})
            caps = []
            for c in range(1, (max(b) if b else 0) + 1):
                vs = b.get(c, {})
                caps.append([vs.get(v, "") for v in range(1, (max(vs) if vs else 0) + 1)])
            caps_por_libro.append(len(caps))
            with open(os.path.join(destino, lang, f"{n}.json"), "w", encoding="utf-8") as fo:
                json.dump({"n": n, "nombre": nombres[n - 1], "caps": caps}, fo, ensure_ascii=False, separators=(",", ":"))
        faltan = [n for n in range(1, 67) if not caps_por_libro[n - 1]]
        print(lang, sigla, "libros sin texto:", faltan, "caps:", sum(caps_por_libro))
        indice["versiones"][lang] = {"sigla": sigla, "nombre": nombre, "licencia": "Dominio público"}
        indice["libros"][lang] = nombres
        indice.setdefault("capitulos", {})[lang] = caps_por_libro
    with open(os.path.join(destino, "indice.json"), "w", encoding="utf-8") as fo:
        json.dump(indice, fo, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
