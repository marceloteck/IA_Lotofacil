import os

# ==========================
# CONFIGURAÇÕES
# ==========================
PASTA_PROJETO = "."  # raiz do projeto
ARQUIVO_SAIDA = "mapeamento_completo_projeto.txt"

EXTENSOES_PERMITIDAS = (
    ".py",
    ".md",
    ".json",
    ".yml",
    ".yaml",
    ".ini",
)

PASTAS_IGNORADAS = {
    ".git",
    "__pycache__",
    ".txt",
    "venv",
    ".venv",
    "env",
    "node_modules",
    ".idea",
    ".vscode"
}

# ==========================
# FUNÇÃO PRINCIPAL
# ==========================
def mapear_projeto():
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as saida:
        saida.write("MAPEAMENTO COMPLETO DO PROJETO PYTHON\n")
        saida.write("=" * 80 + "\n\n")

        for raiz, pastas, arquivos in os.walk(PASTA_PROJETO):
            # Remove pastas ignoradas
            pastas[:] = [p for p in pastas if p not in PASTAS_IGNORADAS]

            for arquivo in arquivos:
                if arquivo.lower().endswith(EXTENSOES_PERMITIDAS):
                    caminho_completo = os.path.join(raiz, arquivo)

                    saida.write("=" * 80 + "\n")
                    saida.write(f"📄 ARQUIVO: {caminho_completo}\n")
                    saida.write("=" * 80 + "\n\n")

                    try:
                        with open(caminho_completo, "r", encoding="utf-8") as f:
                            conteudo = f.read()
                            saida.write(conteudo)
                    except Exception as e:
                        saida.write(f"[ERRO AO LER O ARQUIVO: {e}]\n")

                    saida.write("\n\n")

    print(f"✅ Mapeamento concluído! Arquivo gerado: {ARQUIVO_SAIDA}")

# ==========================
# EXECUÇÃO
# ==========================
if __name__ == "__main__":
    mapear_projeto()
