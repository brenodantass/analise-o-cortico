"""
Passo 7 - Análises que enriquecem a resposta (semanas 4 e 6).

(a) Capítulo de entrada de cada personagem  -> "as ausências contam a cronologia".
(b) Pares frequentes que NUNCA dividem um capítulo (a não-aresta também informa).
(c) Sensibilidade à janela: a mesma lista de menções projetada por CAPÍTULO e por PARÁGRAFO.
Saídas em results/tabelas/.
"""
import itertools

import networkx as nx
import pandas as pd

from comum import PROC, TABELAS

TABELAS.mkdir(parents=True, exist_ok=True)
B = pd.read_csv(PROC / "presenca.csv", index_col="capitulo")
men = pd.read_csv(PROC / "mencoes.csv")

# (a) capítulo de entrada e nº de capítulos
entrada = pd.DataFrame({"capitulo_entrada": B.apply(lambda c: c[c > 0].index.min()),
                        "n_capitulos": B.sum()}).sort_values(["capitulo_entrada", "n_capitulos"],
                                                             ascending=[True, False])
entrada.to_csv(TABELAS / "capitulo_de_entrada.csv", encoding="utf-8")
print("== Entrada dos personagens ==\n", entrada.to_string())

# (b) pares frequentes que nunca se encontram
freq = B.sum()
frequentes = freq[freq >= 5].index
C = B.T @ B
nunca = [(a, b, int(freq[a]), int(freq[b])) for a, b in itertools.combinations(frequentes, 2) if C.loc[a, b] == 0]
pd.DataFrame(nunca, columns=["a", "b", "cap_a", "cap_b"]).to_csv(
    TABELAS / "pares_que_nunca_dividem_capitulo.csv", index=False, encoding="utf-8")
print(f"\n== {len(nunca)} pares (ambos em >=5 capítulos) que nunca dividem um capítulo ==")
for a, b, ca, cb in nunca[:15]:
    print(f"  {a} ({ca}) · {b} ({cb})")

# (c) capítulo x parágrafo
linhas = []
for janela, chaves in [("capitulo", ["capitulo"]), ("paragrafo", ["capitulo", "paragrafo"])]:
    unidade = men.drop_duplicates(chaves + ["personagem"])
    G = nx.Graph()
    G.add_nodes_from(unidade.personagem.unique())
    for _, grupo in unidade.groupby(chaves):
        for a, b in itertools.combinations(sorted(grupo.personagem), 2):
            peso = G[a][b]["peso"] + 1 if G.has_edge(a, b) else 1
            G.add_edge(a, b, peso=peso)
    pesada = max(G.edges(data="peso"), key=lambda e: e[2])
    linhas.append({"janela": janela, "nos": G.number_of_nodes(), "arestas": G.number_of_edges(),
                   "densidade": round(nx.density(G), 3), "clustering": round(nx.average_clustering(G), 3),
                   "componentes": nx.number_connected_components(G),
                   "aresta_mais_pesada": f"{pesada[0]} · {pesada[1]} ({pesada[2]})"})
sens = pd.DataFrame(linhas)
sens.to_csv(TABELAS / "sensibilidade_janela.csv", index=False, encoding="utf-8")
print("\n== A janela muda a rede ==\n", sens.to_string(index=False))
