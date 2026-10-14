"""
Passo 2 - Fatiar: transforma o texto em uma tabela de UNIDADES (capítulo, parágrafo).

Parágrafos são separados por linha em branco. Dentro de um parágrafo, as quebras de
linha viram espaço (porque "José\nDias" não é "José Dias" - lição da semana 6).
Saída: data/processed/unidades.csv  (colunas: capitulo, paragrafo, texto)
"""
import re

import pandas as pd

from comum import PROC, ler_capitulos

linhas = []
for numero, texto in ler_capitulos():
    paragrafos = [p for p in re.split(r"\n\s*\n", texto) if p.strip()]
    for j, p in enumerate(paragrafos, start=1):
        linhas.append({"capitulo": numero, "paragrafo": j, "texto": " ".join(p.split())})

df = pd.DataFrame(linhas)
PROC.mkdir(parents=True, exist_ok=True)
df.to_csv(PROC / "unidades.csv", index=False, encoding="utf-8")

print(f"{df['capitulo'].nunique()} capítulos, {len(df)} parágrafos")
print(df.groupby("capitulo").size().to_string())
