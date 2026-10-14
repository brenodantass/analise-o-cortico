
import pandas as pd

from comum import PERIODOS, PROC

B = pd.read_csv(PROC / "presenca.csv", index_col="capitulo")

recortes = {"completa": list(B.index)}
recortes.update({nome: list(caps) for nome, caps in PERIODOS.items()})

nos, arestas = [], []
for nome, caps in recortes.items():
    Bp = B.loc[caps]
    Bp = Bp.loc[:, Bp.sum() > 0]            
    C = Bp.T @ Bp                            
    for p in Bp.columns:
        nos.append({"periodo": nome, "personagem": p, "n_cap": int(C.loc[p, p])})
    cols = list(Bp.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            w = int(C.loc[a, b])
            if w > 0:
                jac = w / (C.loc[a, a] + C.loc[b, b] - w)
                arestas.append({"periodo": nome, "a": a, "b": b, "peso": w, "jaccard": round(jac, 4)})

pd.DataFrame(nos).to_csv(PROC / "nos_por_periodo.csv", index=False, encoding="utf-8")
pd.DataFrame(arestas).to_csv(PROC / "arestas_por_periodo.csv", index=False, encoding="utf-8")

resumo = (pd.DataFrame(nos).groupby("periodo").size().rename("nos").to_frame()
          .join(pd.DataFrame(arestas).groupby("periodo").size().rename("arestas")))
print(resumo.loc[["completa", "inicio", "meio", "fim"]])
