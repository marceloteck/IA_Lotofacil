import os
import sqlite3
from collections import Counter
from src.db.memoria_sqlite import carregar_memoria_premiada

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "lotofacil.db")
DATA_DIR = os.path.join(BASE_DIR, "data")

caminho_diretorio_txt = os.path.join("src", "memory")
caminho_arquivo_txt = os.path.join(caminho_diretorio_txt, "memoriaSalva.txt")

os.makedirs(caminho_diretorio_txt, exist_ok=True)

def conectar():
    os.makedirs(DATA_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def gerar_relatorio_texto():
    """Busca dados no banco e prepara o resumo estatístico em string"""
    con = conectar()
    cur = con.cursor()
    
    try:
        cur.execute("""
            SELECT pontos, COUNT(*) 
            FROM memoria_premiada 
            GROUP BY pontos 
            ORDER BY pontos DESC
        """)
        resultados = cur.fetchall()
        total_jogos = sum(row[1] for row in resultados)
        
        linhas_relatorio = []
        linhas_relatorio.append("="*40)
        linhas_relatorio.append("📊 ESTATÍSTICAS DA MEMÓRIA")
        linhas_relatorio.append("="*40)
        
        if not resultados:
            linhas_relatorio.append("A memória ainda está vazia.")
        else:
            for pontos, quantidade in resultados:
                percentual = (quantidade / total_jogos) * 100
                barra = "█" * int(percentual / 5)
                linhas_relatorio.append(f"{pontos} Pts: {quantidade:4d} | {barra} ({percentual:6.2f}%)")
        
        linhas_relatorio.append("-" * 40)
        linhas_relatorio.append(f"Total de jogos memorizados: {total_jogos}")
        linhas_relatorio.append("=" * 40 + "\n")
        
        return "\n".join(linhas_relatorio)
    except Exception as e:
        return f"Erro ao gerar estatísticas: {e}"
    finally:
        con.close()

def executar_processamento():
    # 1. Carregar os jogos para a lista detalhada
    jogos = carregar_memoria_premiada()
    
    # 2. Gerar o resumo estatístico
    resumo = gerar_relatorio_texto()
    
    print(resumo) # Mostra o resumo no console

    if not jogos:
        with open(caminho_arquivo_txt, "w", encoding="utf-8") as f:
            f.write(resumo)
            f.write("\nNenhum jogo detalhado encontrado.")
        print("Nenhum jogo encontrado para listar.")
        return

    # 3. Ordenar jogos (Maior pontuação primeiro)
    jogos_ordenados = sorted(jogos, key=lambda x: x['pontos'], reverse=True)

    # 4. Gravar tudo no arquivo
    with open(caminho_arquivo_txt, "w", encoding="utf-8") as f:
        # Escreve o primeiro relatório (Estatísticas)
        f.write(resumo)
        
        # Escreve o segundo relatório (Lista de Jogos)
        f.write("\n🏆 LISTA DETALHADA DE JOGOS\n")
        f.write("-" * 40 + "\n")
        
        for j in jogos_ordenados:
            linha = f"{j['pontos']} pontos | {j['dezenas']}"
            f.write(linha + "\n")

    print(f"✅ Relatório completo (Estatísticas + Lista) salvo em:\n👉 {caminho_arquivo_txt}")

if __name__ == "__main__":
    executar_processamento()