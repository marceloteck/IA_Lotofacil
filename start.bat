@echo off
:inicio
cls
echo =================================================
echo   Iniciando: python -m teste_treinamento
echo =================================================
echo.

:: Executa o comando desejado
python -m teste_treinamento

echo.
echo =================================================
echo   Execucao finalizada. - TESTE
echo =================================================
echo.

:menu
set /p escolha="Deseja executar novamente? (S para Sim / N para Sair): "

if /i "%escolha%"=="S" goto inicio
if /i "%escolha%"=="N" goto sair

echo Opcao invalida. Por favor, digite S ou N.
goto menu

:sair
echo Saindo...
pause
exit