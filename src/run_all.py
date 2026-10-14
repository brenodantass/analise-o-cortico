"""Roda o pipeline inteiro, do download às figuras (reprodução em um comando).

    python src/run_all.py
"""
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ETAPAS = ["00_baixar_texto.py", "01_inspecionar_texto.py", "02_preparar_capitulos.py",
          "03_identificar_personagens.py", "04_construir_redes.py", "05_calcular_metricas.py",
          "06_gerar_figuras.py", "07_analises_extras.py"]

for etapa in ETAPAS:
    print(f"\n{'=' * 70}\n>>> {etapa}\n{'=' * 70}")
    if subprocess.run([sys.executable, str(SRC / etapa)]).returncode != 0:
        sys.exit(f"Falhou em {etapa}. Corrija antes de continuar.")
print("\nPipeline completo. Resultados em results/ e data/processed/.")
