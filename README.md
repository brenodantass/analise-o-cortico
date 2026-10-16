# O ambiente social e a evolução da rede de personagens em *O Cortiço*

## Integrantes

Breno Gustavo de Araujo Dantas | Letícia Cibele Lima do Nascimento | Maria Luiza da Costa Barbosa

## Vídeo


## Problema e pergunta

**Pergunta.** Como a rede de coocorrência de personagens de *O Cortiço* (Aluísio Azevedo, 1890) muda do início ao
meio e ao final do romance, e personagens associados a ambientes sociais diferentes (cortiço, sobrado de Miranda,
outros) ocupam posições diferentes na rede?

**Por que em rede.** A pergunta é sobre relações, não sobre contagem. Quantas vezes um personagem é citado não diz
quem faz a ponte entre o cortiço e o sobrado, nem se os dois mundos se misturam ou ficam separados. Essas são
propriedades da estrutura (caminhos, pontes, grupos coesos, mistura entre atributos), e só existem quando os
personagens são nós e as cenas compartilhadas são arestas.
**Quem se beneficia.** Leitores e professores de literatura brasileira, que ganham uma leitura estrutural do romance
(quem liga os grupos sociais e como isso muda) que complementa a leitura crítica tradicional. O projeto também serve de
exemplo de método: mostra como uma decisão de modelagem (a janela de coocorrência) muda as conclusões.

## Dados

- **Fonte:** https://letrasmais.net.br/lira/index.php?pg=76&post=1012
- **Como obter:** `python src/00_baixar_texto.py`.
- **Limpeza:** cabeçalho/rodapé do Gutenberg e índice ignorados; 23 capítulos separados pelos numerais romanos;
  quebras de linha dentro de parágrafos normalizadas (`src/02_preparar_capitulos.py`).
- **Dicionário de personagens:** feito à mão (`src/personagens.py`), com variantes da ortografia da edição.
- **Ambiente social:** classificado à mão em `data/processed/ambientes.csv`, com capítulo e trecho de evidência.

Critério de classificação: onde o personagem mora ou trabalha, segundo o texto. Cortiço (22): moradores, lavadeiras,
e também João Romão, Bertoleza e os caixeiros da venda, que ficam à entrada da estalagem. Sobrado de Miranda (8):
a família, os hóspedes (Henrique, Botelho) e a criadagem (Izaura, Leonor, Valentim). Outros (2): Firmo e João da
Costa, que aparecem como visitantes ou vêm de fora.
## Modelagem

| Elemento | Definição |
|---|---|
| Nó | Personagem (variantes unificadas no dicionário) |
| Aresta | Dois personagens aparecem no mesmo capítulo |
| Peso | Nº de capítulos compartilhados (também Jaccard como peso normalizado) |
| Direção | Não direcionado |
| Atributos | `n_cap` (capítulos em que aparece), `ambiente` |
| Recortes | Início (caps. I–VIII), meio (IX–XVI), fim (XVII–XXIII) e obra completa |

**O que ficou de fora:** _preencha (ex.: o cortiço como "personagem", coletivos como "as lavadeiras", personagens só
mencionados, relações entre personagens que não dividem capítulo, nomeação ≠ presença)._

## Conteúdo do curso utilizado

| conceito | semana | onde aparece | para que serviu |
| Tipos de grafo (não dirigido, ponderado), nó, aresta, peso | 2 | `src/04_construir_redes.py`; `src/08_paragrafo_e_ambientes.py` (`grafo_paragrafo`, l. 41) | definir o modelo das redes por capítulo e por parágrafo |
| Atributos de nó | 2 | `data/processed/ambientes.csv`; `src/05_calcular_metricas.py` (l. 57); `src/08` (l. 46) | comparar a posição de cada ambiente |
| Rede bipartida (capítulo x personagem), matriz de incidência e projeção | 6 | `data/processed/presenca.csv` (incidência); `src/04_construir_redes.py` (l. 15, `Bp.T @ Bp`) | obter a rede de personagens por capítulo |
| Coocorrência e janela | 6 | `src/08` (l. 41 a 55); `src/07_analises_extras.py` (l. 38 a 52) | construir a rede por parágrafo e medir o efeito da janela |
| Índice de Jaccard | 6 | `src/04_construir_redes.py` (l. 23) | peso normalizado das arestas por capítulo |
| Esqueleto por limiar | 6 | `src/06_gerar_figuras.py` (`JACCARD_MIN`, l. 19); `src/08` (esqueleto Jaccard, l. 127 em diante) | tornar legível a rede por capítulo e ver quando ela se fragmenta |
| Densidade | 2 | `src/05` (l. 40); `src/08` (l. 82) | mostrar que a rede por capítulo é quase completa (0,95) e a por parágrafo não (0,35 a 0,43) |
| Grau (e grau normalizado) | 2 | `src/05` (l. 48); `src/08` (l. 96) | medir quão conectado é cada personagem e cada ambiente |
| Subredes (dentro e entre ambientes) | 2 | `src/05` (l. 70 a 79); `src/08` (l. 100 a 108, `mistura_ambientes_paragrafo.csv`) | medir quanto da rede liga cortiço e sobrado |
| Componentes | 4 | `src/05` (l. 42); `src/08` (l. 84) | ver se a rede se parte (por parágrafo, no meio há 2 componentes) |
| Caminhos e diâmetro | 4 | `src/05` (l. 43); `src/08` (l. 85) | rede pequena: diâmetro 2 (capítulo) e 3 (parágrafo) |
| Eficiência global | 4 | `src/05` (l. 44); `src/08` (l. 86) | medir a facilidade de circulação entre personagens |
| Clustering | 4 | `src/05` (l. 41); `src/08` (l. 83) | medir a formação de grupos fechados (0,86 a 0,98 por capítulo contra 0,59 a 0,72 por parágrafo) |
| Centralidade de grau, closeness e betweenness | 4 | `src/05` (l. 49 a 51); `src/08` (l. 91 a 92) | identificar quem faz a ponte entre grupos (Miranda no início, João Romão depois) |
| k-core, core number e degenerescência | 5 | `src/05` (l. 45 e 50); `src/08` (l. 79 e 87) | medir o núcleo mais coeso da rede em cada fase |

Ferramentas **de fora do curso** (complementares, não substituem as acima): coeficiente de assortatividade por atributo
(`nx.attribute_assortativity_coefficient`, `src/08` l. 60) e teste de permutação com 1.000 sorteios dos ambientes
(`src/08` l. 58 a 70), usados para saber se a separação entre cortiço e sobrado é maior que o acaso. No lugar de NER
(semana 6), usamos um dicionário de personagens feito à mão.

## Como executar

```
python -m venv .venv
.venv\Scripts\activate            # Windows (Linux/macOS: source .venv/bin/activate)
python -m pip install -r requirements.txt
python src/run_all.py
```

Resultados em `data/processed/` e `results/` (tabelas e figuras).

## Resultados

## Referências

- Azevedo, A. *O Cortiço*. Project Gutenberg #69187.
- Material da disciplina: lesson08 (Do texto à rede) e Projeto_Avaliacao_1.
