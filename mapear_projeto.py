import os
import re

# ==========================
# CONFIGURAÇÕES
# ==========================
PASTA_PROJETO = "."
MAPEAMENTO_DIR = "MAPEAMENTO_DIR"

EXTENSOES_PERMITIDAS = (".py", ".md", ".json", ".yml", ".yaml", ".ini")
PASTAS_IGNORADAS = {
    ".git", "__pycache__", "venv", ".venv", "env", 
    "node_modules", ".idea", ".vscode", MAPEAMENTO_DIR
}

# ==========================
# FUNÇÃO PRINCIPAL
# ==========================
def mapear_projeto():
    if not os.path.exists(MAPEAMENTO_DIR):
        os.makedirs(MAPEAMENTO_DIR)

    for raiz, pastas, arquivos in os.walk(PASTA_PROJETO):
        pastas[:] = [p for p in pastas if p not in PASTAS_IGNORADAS]
        arquivos_validos = [arq for arq in arquivos if arq.lower().endswith(EXTENSOES_PERMITIDAS)]

        if not arquivos_validos:
            continue

        nome_f = raiz.replace(os.sep, "_").replace(".", "RAIZ").strip("_")
        caminho_saida = os.path.join(MAPEAMENTO_DIR, f"map_{nome_f}.txt")

        with open(caminho_saida, "w", encoding="utf-8") as saida:
            for arquivo in arquivos_validos:
                caminho_arq = os.path.join(raiz, arquivo)
                saida.write(f">>> FILE: {caminho_arq}\n")
                
                try:
                    with open(caminho_arq, "r", encoding="utf-8") as f:
                        conteudo = f.read()
                        
                        # Remove excesso de quebras de linha (3 ou mais viram apenas 2)
                        # \n{2,} encontra 2 ou mais quebras. Substituindo por \n garante 
                        # que não haja linhas em branco excessivas.
                        conteudo_limpo = re.sub(r'\n\s*\n+', '\n\n', conteudo).strip()
                        
                        saida.write(conteudo_limpo)
                except Exception as e:
                    saida.write(f"[ERRO: {e}]")
                
                saida.write("\n\n") # Separação entre arquivos diferentes

    print(f"✅ Mapeamento ultra-compacto concluído em: {MAPEAMENTO_DIR}")

if __name__ == "__main__":
    mapear_projeto()