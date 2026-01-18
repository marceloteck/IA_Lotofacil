"""
🧾 LOGGER CENTRAL DO SISTEMA
Responsável por logs padronizados em todo o projeto.
"""

import logging
import sys

# ==================================================
# ⚙️ CONFIGURAÇÃO BASE
# ==================================================
LOGGER_NAME = "IA_Lotofacil"
LOG_LEVEL = logging.INFO  # mude para DEBUG se quiser mais detalhes

# ==================================================
# 🧠 CRIA LOGGER
# ==================================================
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(LOG_LEVEL)

# Evita duplicar handlers (erro comum)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ==================================================
# 🚫 NÃO PROPAGA PARA ROOT LOGGER
# ==================================================
logger.propagate = False
