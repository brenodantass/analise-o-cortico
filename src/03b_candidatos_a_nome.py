import re
from collections import defaultdict

import pandas as pd

from comum import PROC, TABELAS
from personagens import ALIASES

unidades = pd.read_csv(PROC / "unidades.csv")
conhecidas = {f for fs in ALIASES.values() for f in fs}
texto_todo = " ".join(unidades.texto)

padrao = re.compile(r"(?<=[a-zà-ú,;] )([A-ZÀ-Ú][\wà-ú'-]+(?: (?:de|da|do|dos|das|e) [A-ZÀ-Ú][\wà-ú'-]+|"
                    r" [A-ZÀ-Ú][\wà-ú'-]+)*)")
caps = defaultdict(set)
for u in unidades.itertuples():
    for m in padrao.finditer(u.texto):
        caps[m.group(1)].add(u.capitulo)

linhas = []
for forma, cs in caps.items():
    if forma in conhecidas or any(forma in c or c in forma for c in conhecidas):
        continue
    minuscula = bool(re.search(rf"(?<!\w){re.escape(forma.lower())}(?!\w)", texto_todo))
    linhas.append({"forma": forma, "n_capitulos": len(cs), "aparece_em_minuscula": minuscula,
                   "capitulos": ",".join(map(str, sorted(cs)))})

df = pd.DataFrame(linhas, columns=["forma", "n_capitulos", "aparece_em_minuscula", "capitulos"])
df = df.sort_values("n_capitulos", ascending=False)
TABELAS.mkdir(parents=True, exist_ok=True)
df.to_csv(TABELAS / "candidatos_a_nome.csv", index=False, encoding="utf-8")
print("Candidatos que passam no teste da minúscula e aparecem em >= 2 capítulos:")
print(df[(~df.aparece_em_minuscula) & (df.n_capitulos >= 2)].head(60).to_string(index=False))
