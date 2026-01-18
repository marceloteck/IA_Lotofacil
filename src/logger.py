# ==========================================================
# LOGGER CENTRALIZADO — IA LOTOFÁCIL
# Observabilidade sem interferência
# ==========================================================

import os
from datetime import datetime

# ----------------------------------------------------------
# CONFIGURAÇÕES GERAIS
# ----------------------------------------------------------
LOG_ATIVO = True
PASTA_LOGS = "logs"

os.makedirs(PASTA_LOGS, exist_ok=True)

# ----------------------------------------------------------
# FUNÇÃO BASE (NUNCA QUEBRA O SISTEMA)
# ----------------------------------------------------------
def _escrever_log(nome_arquivo, mensagem):
    if not LOG_ATIVO:
        return

    try:
        caminho = os.path.join(PASTA_LOGS, nome_arquivo)
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(caminho, "a", encoding="utf-8") as f:
            f.write(f"[{agora}] {mensagem}\n")

    except Exception:
        # Segurança total: log nunca derruba o sistema
        pass

# ==========================================================
# LOGS ESPECIALIZADOS
# ==========================================================

def log_treinamento(msg):
    _escrever_log("treinamento.log", msg)

def log_motor(msg):
    _escrever_log("motor.log", msg)

def log_avaliador(msg):
    _escrever_log("avaliador.log", msg)

def log_pesos(msg):
    _escrever_log("pesos.log", msg)

def log_foco_1415(msg):
    _escrever_log("foco_1415.log", msg)

def log_geracao(msg):
    _escrever_log("geracao.log", msg)

# ==========================================================
# UTILIDADES (OPCIONAL)
# ==========================================================

def log_divisor(nome="GERAL"):
    linha = f"{'-'*10} {nome} {'-'*10}"
    _escrever_log("treinamento.log", linha)
