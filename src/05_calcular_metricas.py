"""
Passo 5 - Métricas por período e por ambiente (semanas 2, 4 e 5).

Lê data/processed/{nos,arestas}_por_periodo.csv e, se existir, data/processed/ambientes.csv
(colunas: personagem, ambiente, capitulo_evidencia, trecho_evidencia).
Saídas em results/tabelas/.
"""
import networkx as nx
import pandas as pd

from comum import PROC, TABELAS

TABELAS.mkdir(parents=True, exist_ok=True)
nos = pd.read_csv(PROC / "nos_por_periodo.csv")
arestas = pd.read_csv(PROC / "arestas_por_periodo.csv")

ambientes = None
if (PROC / "ambientes.csv").exists():
    ambientes = pd.read_csv(PROC / "ambientes.csv").set_index("personagem")["ambiente"]


def montar_grafo(periodo: str) -> nx.Graph:
    G = nx.Graph()
    for r in nos[nos.periodo == periodo].itertuples():
        G.add_node(r.personagem, n_cap=r.n_cap)
    for r in arestas[arestas.periodo == periodo].itertuples():
        # distância = 1/peso: capítulos compartilhados = "mais perto" (usada na betweenness)
        G.add_edge(r.a, r.b, peso=r.peso, jaccard=r.jaccard, dist=1 / r.peso)
    return G


linhas_rede, linhas_no = [], []
for periodo in ["completa", "inicio", "meio", "fim"]:
    G = montar_grafo(periodo)
    gcc = G.subgraph(max(nx.connected_components(G), key=len))
    linhas_rede.append({
        "periodo": periodo,
        "nos": G.number_of_nodes(),
        "arestas": G.number_of_edges(),
        "densidade": round(nx.density(G), 3),                           # semana 2
        "clustering_medio": round(nx.average_clustering(G), 3),         # semana 4
        "componentes": nx.number_connected_components(G),               # semana 4
        "diametro_gcc": nx.diameter(gcc),                               # semana 4
        "eficiencia_global": round(nx.global_efficiency(G), 3),         # semana 4
        "degenerescencia": max(nx.core_number(G).values()),             # semana 5
    })
    forca = dict(G.degree(weight="peso"))
    grau = dict(G.degree())
    btw = nx.betweenness_centrality(G, weight="dist")                   # semana 4
    core = nx.core_number(G)                                            # semana 5
    clo = nx.closeness_centrality(G, distance="dist")                   # semana 4
    for p in G.nodes:
        linhas_no.append({
            "periodo": periodo, "personagem": p, "n_cap": G.nodes[p]["n_cap"],
            "grau": grau[p], "forca": forca[p], "betweenness": round(btw[p], 4),
            "closeness": round(clo[p], 4), "core": core[p],
            "ambiente": ambientes.get(p, "sem_classificacao") if ambientes is not None else "sem_classificacao",
        })

rede = pd.DataFrame(linhas_rede)
no = pd.DataFrame(linhas_no)
rede.to_csv(TABELAS / "metricas_rede_por_periodo.csv", index=False, encoding="utf-8")
no.to_csv(TABELAS / "metricas_nos_por_periodo.csv", index=False, encoding="utf-8")

print("\n== Rede por período =="); print(rede.to_string(index=False))
for periodo in ["inicio", "meio", "fim"]:
    print(f"\n== Top 5 por força em '{periodo}' ==")
    print(no[no.periodo == periodo].nlargest(5, "forca")[["personagem", "forca", "grau", "betweenness", "core"]].to_string(index=False))

if ambientes is not None:
    print("\n== Média por ambiente e período ==")
    print(no.groupby(["periodo", "ambiente"])[["forca", "betweenness", "core"]].mean().round(2).to_string())
    # arestas dentro do mesmo ambiente x entre ambientes (subredes - semana 2)
    ar = arestas.copy()
    ar["amb_a"] = ar.a.map(ambientes); ar["amb_b"] = ar.b.map(ambientes)
    ar["tipo"] = ar.apply(lambda r: "mesmo_ambiente" if r.amb_a == r.amb_b else "entre_ambientes", axis=1)
    inter = ar.groupby(["periodo", "tipo"]).agg(arestas=("peso", "size"), peso_total=("peso", "sum")).reset_index()
    inter.to_csv(TABELAS / "arestas_por_ambiente.csv", index=False, encoding="utf-8")
    print("\n== Arestas dentro x entre ambientes =="); print(inter.to_string(index=False))
