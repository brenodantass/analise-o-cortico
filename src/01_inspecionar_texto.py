"""
Passo 1 - Inspecionar o texto e localizar os capítulos.

Na edição do Gutenberg (#69187):
  - o ÍNDICE usa linhas "CAPITULO I", "CAPITULO II"... (NÃO são os capítulos reais);
  - no corpo, cada capítulo começa com o numeral romano SOZINHO na linha ("I", "II"...).
O romance tem 23 capítulos.

Para não confundir "I" (numeral) com outra linha qualquer, aceitamos os numerais
em ordem: só vale o próximo esperado (1, 2, 3, ...).

Uso:
    python src/01_inspecionar_texto.py
    python src/01_inspecionar_texto.py caminho/outro_arquivo.txt
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "data" / "raw" / "o_cortico.txt"
TOTAL_ESPERADO = 23


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


def main() -> None:
    if not CAMINHO.exists():
        sys.exit(f"Arquivo não encontrado: {CAMINHO}\nRode antes: python src/00_baixar_texto.py")

    texto = CAMINHO.read_text(encoding="utf-8-sig")
    print(f"Arquivo: {CAMINHO}\nCaracteres: {len(texto):,}")

    # 1) Marcadores do Gutenberg (cabeçalho/rodapé de licença não fazem parte do romance)
    ini = re.search(r"\*\*\* START OF .*?\*\*\*", texto)
    fim = re.search(r"\*\*\* END OF .*?\*\*\*", texto)
    print("\nMarcador de início:", "encontrado" if ini else "NÃO encontrado")
    print("Marcador de fim:   ", "encontrado" if fim else "NÃO encontrado")
    corpo = texto[ini.end() if ini else 0 : fim.start() if fim else len(texto)]

    # 2) Capítulos: numeral romano sozinho na linha, aceito na ordem esperada
    padrao = re.compile(r"^[ \t]*([IVXLC]+)[ \t]*$", re.MULTILINE)
    achados, ignorados, esperado = [], [], 1
    for m in padrao.finditer(corpo):
        if romano_para_int(m.group(1)) == esperado:
            achados.append(m)
            esperado += 1
        else:
            ignorados.append(m.group(1))

    print(f"\nCapítulos encontrados: {len(achados)} (esperado: {TOTAL_ESPERADO})")
    if len(achados) != TOTAL_ESPERADO:
        print("ATENÇÃO: quantidade diferente do esperado. NÃO avance antes de ajustar o padrão.")
    if ignorados:
        print("Linhas parecidas com numeral, mas fora de sequência (ignoradas):", ignorados[:10])

    # 3) Resumo por capítulo para conferência manual
    print(f"\n{'Cap':>4} {'palavras':>9}  início do capítulo")
    for i, m in enumerate(achados):
        fim_cap = achados[i + 1].start() if i + 1 < len(achados) else len(corpo)
        trecho = corpo[m.end() : fim_cap].strip()
        inicio = " ".join(trecho.split())[:70]
        print(f"{m.group(1):>4} {len(trecho.split()):>9}  {inicio}...")

    # 4) Conferir o final do último capítulo (há epílogo/rodapé que precise sair?)
    if achados:
        ultimo = corpo[achados[-1].end() :].strip()
        print("\nÚltimos 300 caracteres do último capítulo (confira se é o fim do romance):")
        print(repr(ultimo[-300:]))


if __name__ == "__main__":
    main()
