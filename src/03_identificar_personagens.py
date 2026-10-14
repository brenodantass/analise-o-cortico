import re

import pandas as pd

from comum import PROC, TOTAL_CAPITULOS
from personagens import ALIASES, IGNORAR_CONTEXTOS

unidades = pd.read_csv(PROC / "unidades.csv")

formas = sorted(((f, p) for p, fs in ALIASES.items() for f in fs), key=lambda x: -len(x[0]))
regex = {f: re.compile(rf"(?<!\w){re.escape(f)}(?!\w)") for f, _ in formas}

mencoes = []
for u in unidades.itertuples():
    texto = u.texto
    for ctx in IGNORAR_CONTEXTOS:
        texto = texto.replace(ctx, " " * len(ctx))
    ocupado = []
    for forma, personagem in formas:
        for m in regex[forma].finditer(texto):
            if any(m.start() < b and a < m.end() for a, b in ocupado):
                continue
            ocupado.append((m.start(), m.end()))
            mencoes.append({"capitulo": u.capitulo, "paragrafo": u.paragrafo,
                            "personagem": personagem, "forma": forma})

men = pd.DataFrame(mencoes)
men.to_csv(PROC / "mencoes.csv", index=False, encoding="utf-8")

B = (men.assign(v=1).pivot_table(index="capitulo", columns="personagem", values="v",
                                 aggfunc="max", fill_value=0)
        .reindex(range(1, TOTAL_CAPITULOS + 1), fill_value=0))
B.to_csv(PROC / "presenca.csv", encoding="utf-8")

print(f"{len(men)} menções, {B.shape[1]} personagens encontrados de {len(ALIASES)} no dicionário")
print("\nCapítulos em que cada personagem aparece (menor -> maior):")
print(B.sum().sort_values().to_string())
nunca = sorted(set(ALIASES) - set(B.columns))
if nunca:
    print("\nNo dicionário, mas NUNCA achados (confira a grafia):", nunca)
print("\nFormas mais usadas (para auditar):")
print(men.groupby(["personagem", "forma"]).size().sort_values(ascending=False).head(15).to_string())
