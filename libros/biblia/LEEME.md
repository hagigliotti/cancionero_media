# Biblia (para el lector de la app)

Textos de dominio público, convertidos con `biblia_a_json.py` desde
[seven1m/open-bibles](https://github.com/seven1m/open-bibles).

| idioma | sigla | versión | licencia |
|---|---|---|---|
| es | RV1909 | Reina-Valera 1909 (1909) | Dominio público |
| en | KJV | King James Version (1611) | Public domain |
| it | RIV | Riveduta (Luzzi) (1927) | Pubblico dominio |
| fr | OST | Ostervald (1996) | Domaine public |
| de | LUT1912 | Luther 1912 (1912) | Gemeinfrei |
| pt | ALM | Almeida (1911) | Domínio público |
| es | RV1865 | Reina-Valera 1865 (1865) | Dominio público |
| es | BES | La Biblia en Español Sencillo (2022) | CC BY 4.0 · AudioBiblia.org / Irma Flores |
| es | VBL | Versión Biblia Libre (2022) | CC BY-SA 4.0 · Jonathan Gallagher |
| es | PDPT | Palabra de Dios para ti (2022) | CC BY-SA 4.0 · Bible League International |
| es | BPL | Biblia Platense (Straubinger) (1951) | Dominio público |
| en | WEB | World English Bible (2020) | Public domain |
| en | BSB | Berean Standard Bible (2022) | Public domain (CC0) |
| en | ASV | American Standard Version (1901) | Public domain |
| en | NHEB | New Heart English Bible (2020) | Public domain |
| en | YLT | Young's Literal Translation (1898) | Public domain |
| en | DBY | Darby Bible (1890) | Public domain |
| en | DRC | Douay-Rheims (Challoner) (1752) | Public domain |
| en | BBE | Bible in Basic English (1964) | Public domain |
| en | WBT | Webster Bible (1833) | Public domain |
| en | GNV | Geneva Bible (1599) | Public domain |
| it | DIO | Diodati (1885) | Pubblico dominio |
| fr | MAR | David Martin (1744) | Domaine public |
| fr | JND | Darby (français) (1885) | Domaine public |
| fr | CRA | Crampon (1923) | Domaine public |
| de | LUT1545 | Luther 1545 (1545) | Gemeinfrei |
| de | ELB1905 | Elberfelder 1905 (1905) | Gemeinfrei |
| de | ELB1871 | Elberfelder 1871 (1871) | Gemeinfrei |
| de | MENGE | Menge-Bibel (1939) | Gemeinfrei |
| de | ZUR | Zürcher Bibel (1931) | Gemeinfrei |
| de | TXT | Textbibel (Kautzsch/Weizsäcker) (1906) | Gemeinfrei |
| de | GRU | Grünewald-Bibel (1924) | Gemeinfrei |
| pt | BLIVRE | Bíblia Livre (2018) | CC BY 3.0 BR · Diego Santos, Mario Sérgio e Marco Teles |
| pt | BLTR | Bíblia Livre (Textus Receptus) (2018) | CC BY 3.0 BR · Diego Santos, Mario Sérgio e Marco Teles |
| pt | NVA | Nova Versão de Acesso Livre (2020) | CC BY-SA 4.0 · Diego Santos e Marco Teles |

- `versiones.json`: todas las versiones (id, idioma, licencia, ruta y capítulos por libro).
- Las versiones principales están en `<idioma>/<n>.json`; las demás en `v/<id>/<n>.json`.
- `biblias_extra.py` + `diodati.py` generan las versiones extra (fuentes: seven1m/open-bibles, scrollmapper/bible_databases, wldeh/bible-api).
- Douay-Rheims y Platense numeran los Salmos como la Vulgata (Salmo 23 = 22).
