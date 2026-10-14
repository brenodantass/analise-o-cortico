# O ambiente social e a evolução da rede de personagens em *O Cortiço*

## Integrantes

Breno Gustavo de Araujo Dantas | Letícia Cibele Lima do Nascimento | Maria Luiza da Costa Barbosa

## Vídeo


## Problema e pergunta

**Pergunta.** Como a rede de coocorrência de personagens de *O Cortiço* (Aluísio Azevedo, 1890) muda do início ao
meio e ao final do romance, e personagens associados a ambientes sociais diferentes (cortiço, sobrado de Miranda,
outros) ocupam posições diferentes na rede?

**Por que em rede.** 
**Quem se beneficia.** 

## Dados

- **Fonte:** https://letrasmais.net.br/lira/index.php?pg=76&post=1012
- **Como obter:** `python src/00_baixar_texto.py`.
- **Limpeza:** cabeçalho/rodapé do Gutenberg e índice ignorados; 23 capítulos separados pelos numerais romanos;
  quebras de linha dentro de parágrafos normalizadas (`src/02_preparar_capitulos.py`).
- **Dicionário de personagens:** feito à mão (`src/personagens.py`), com variantes da ortografia da edição.
- **Ambiente social:** classificado à mão em `data/processed/ambientes.csv`, com capítulo e trecho de evidência.

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
|---|---|---|---|
|  | | |

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
