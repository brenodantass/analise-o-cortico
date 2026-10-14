import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEXTO = RAIZ / "data" / "raw" / "o_cortico.txt"
PROC = RAIZ / "data" / "processed"
TABELAS = RAIZ / "results" / "tabelas"
GRAFOS = RAIZ / "results" / "grafos"
TOTAL_CAPITULOS = 23

PERIODOS = {
    "inicio": range(1, 9),
    "meio": range(9, 17),
    "fim": range(17, 24),
}

def romano_para_int(s: str) -> int:
    valores = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    total = 0
    for i, c in enumerate(s):
        v = valores[c]
        if i + 1 < len(s) and valores[s[i + 1]] > v:
            total -= v
        else:
            total += v
    return total


def ler_capitulos() -> list[tuple[int, str]]:
    texto = TEXTO.read_text(encoding="utf-8-sig")
    ini = re.search(r"\*\*\* START OF .*?\*\*\*", texto)
    fim = re.search(r"\*\*\* END OF .*?\*\*\*", texto)
    corpo = texto[ini.end() if ini else 0 : fim.start() if fim else len(texto)]

    padrao = re.compile(r"^[ \t]*([IVXLC]+)[ \t]*$", re.MULTILINE)
    marcas, esperado = [], 1
    for m in padrao.finditer(corpo):
        if romano_para_int(m.group(1)) == esperado:
            marcas.append(m)
            esperado += 1
    if len(marcas) != TOTAL_CAPITULOS:
        raise SystemExit(f"Esperava {TOTAL_CAPITULOS} capítulos, achei {len(marcas)}. Rode 01_inspecionar_texto.py.")

    capitulos = []
    for i, m in enumerate(marcas):
        fim_cap = marcas[i + 1].start() if i + 1 < len(marcas) else len(corpo)
        capitulos.append((i + 1, corpo[m.end() : fim_cap].strip()))
    return capitulos
