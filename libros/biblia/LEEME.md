# Biblia (para el lector de la app)

Textos de dominio público, convertidos con `biblia_a_json.py` desde
[seven1m/open-bibles](https://github.com/seven1m/open-bibles).

| idioma | versión |
|---|---|
| es | Reina-Valera 1909 |
| en | King James Version |
| it | Riveduta (Luzzi, 1927) |
| fr | Ostervald |
| de | Luther 1912 |
| pt | Almeida |

- `indice.json`: versiones, nombres de los libros y cantidad de capítulos por idioma.
- `<idioma>/<n>.json` (n = 1 Génesis … 66 Apocalipsis): `{"n", "nombre", "caps": [[versículo 1, versículo 2, …], …]}`.
