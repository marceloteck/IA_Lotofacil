@echo off
echo =========================================
echo   INSTALADOR - IA LOTOFACIL (WINDOWS)
echo =========================================

REM Verificar Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Python nao encontrado.
    echo 👉 Instale Python 3.10+ e marque "Add to PATH"
    pause
    exit /b
)

echo ✅ Python encontrado.

REM Criar ambiente virtual
IF NOT EXIST venv (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
call venv\Scripts\activate

REM Atualizar pip
echo 🔄 Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo 📥 Instalando dependencias...
pip install -r requirements.txt

REM Criar banco SQLite se não existir
IF NOT EXIST data\lotofacil.db (
    echo 🗄️ Criando banco SQLite...
    python src\database\db_init.py
)

echo =========================================
echo ✅ INSTALACAO CONCLUIDA COM SUCESSO
echo =========================================
pause
