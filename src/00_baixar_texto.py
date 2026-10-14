import hashlib
import sys
import urllib.request
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "data" / "raw" / "o_cortico.txt"
REGISTRO = RAIZ / "data" / "raw" / "FONTE.txt"

URLS = [
    "https://www.gutenberg.org/cache/epub/69187/pg69187.txt",
    "https://letrasmais.net.br/lira/index.php?pg=76&post=1012",
]

def baixar(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (projeto academico UFRN)"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()

def main() -> None:
    if DESTINO.exists() and "--forcar" not in sys.argv:
        print(f"Já existe: {DESTINO}\nUse --forcar para baixar novamente.")
        return

    conteudo, url_usada = None, None
    for url in URLS:
        try:
            print("Tentando:", url)
            dados = baixar(url)
            if b"START OF THE PROJECT GUTENBERG EBOOK" in dados:
                conteudo, url_usada = dados, url
                break
            print("  Conteúdo inesperado (sem marcador do Gutenberg), tentando próxima URL...")
        except Exception as erro:  # noqa: BLE001
            print("  Falhou:", erro)

    if conteudo is None:
        sys.exit("Não foi possível baixar. Baixe manualmente (veja instruções no topo deste arquivo).")

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_bytes(conteudo)  # preserva o original byte a byte

    sha = hashlib.sha256(conteudo).hexdigest()
    REGISTRO.write_text(
        "Obra: O Cortiço - Aluísio Azevedo (4ª ed., H. Garnier, 1897 - transcrição digital)\n"
        "Fonte: Project Gutenberg, eBook #69187\n"
        f"URL usada: {url_usada}\n"
        f"Data de acesso: {date.today().isoformat()}\n"
        f"Tamanho: {len(conteudo)} bytes\n"
        f"SHA-256: {sha}\n",
        encoding="utf-8",
    )
    print(f"\nOK! Salvo em {DESTINO} ({len(conteudo)/1024:.0f} kB)")
    print(f"Registro da fonte em {REGISTRO}")

if __name__ == "__main__":
    main()
