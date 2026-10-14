"""
Passo 6 - Figuras: as 3 redes (início, meio, fim) com POSIÇÕES FIXAS, para o olho comparar
estrutura e não layout (Gestalt - destino comum, semana 6).

Tamanho do nó = nº de capítulos em que aparece | largura = peso | cor = ambiente.
Só desenha arestas com peso >= LIMIAR (esqueleto por limiar; ajuste olhando as tabelas).
Saídas: results/grafos/*.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from comum import GRAFOS, PROC

LIMIAR = 2
GRAFOS.mkdir(parents=True, exist_ok=True)
nos = pd.read_csv(PROC / "nos_por_periodo.csv")
arestas = pd.read_csv(PROC / "arestas_por_periodo.csv")
amb = (pd.read_csv(PROC / "ambientes.csv").set_index("personagem")["ambiente"]
       if (PROC / "ambientes.csv").exists() else pd.Series(dtype=str))
cores = {a: c for a, c in zip(sorted(amb.unique()), ["#e8683a", "#2a6fd1", "#1fae7a", "#9187e8", "#999999"])}


def grafo(periodo, limiar=1):
    G = nx.Graph()
    for r in nos[nos.periodo == periodo].itertuples():
        G.add_node(r.personagem, n_cap=r.n_cap)
    for r in arestas[(arestas.periodo == periodo) & (arestas.peso >= limiar)].itertuples():
        G.add_edge(r.a, r.b, peso=r.peso)
    return G


# layout calculado UMA vez, na rede completa, e reutilizado nos três períodos
G0 = grafo("completa")
pos = nx.spring_layout(G0, weight="peso", seed=42, k=1.2)

fig, eixos = plt.subplots(1, 3, figsize=(21, 7))
for ax, periodo in zip(eixos, ["inicio", "meio", "fim"]):
    G = grafo(periodo, LIMIAR)
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.35,
                           width=[0.4 + 0.4 * G[u][v]["peso"] for u, v in G.edges])
    nx.draw_networkx_nodes(G, pos, ax=ax,
                           node_size=[60 + 40 * G.nodes[n]["n_cap"] for n in G.nodes],
                           node_color=[cores.get(amb.get(n), "#bbbbbb") for n in G.nodes])
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7)
    ax.set_title(f"{periodo} (peso ≥ {LIMIAR}): {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")
    ax.axis("off")
fig.savefig(GRAFOS / "redes_por_periodo.png", dpi=150, bbox_inches="tight")
print("Salvo:", GRAFOS / "redes_por_periodo.png")

# top 10 por força em cada período
m = pd.read_csv(PROC.parent.parent / "results" / "tabelas" / "metricas_nos_por_periodo.csv")
fig, eixos = plt.subplots(1, 3, figsize=(18, 5))
for ax, periodo in zip(eixos, ["inicio", "meio", "fim"]):
    top = m[m.periodo == periodo].nlargest(10, "forca").iloc[::-1]
    ax.barh(top.personagem, top.forca, color=[cores.get(a, "#bbbbbb") for a in top.ambiente])
    ax.set_title(f"Top 10 por força - {periodo}")
fig.savefig(GRAFOS / "top_forca_por_periodo.png", dpi=150, bbox_inches="tight")
print("Salvo:", GRAFOS / "top_forca_por_periodo.png")
