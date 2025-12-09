@echo off
REM Script de Automação para gerar o HTML e fazer o deploy no GitHub Pages
SETLOCAL
REM Use o caminho exato que você encontrou:
SET PYTHON_EXECUTAVEL=C:\Users\Supote\AppData\Local\Programs\Python\Python313\python.exe
SET PAINEL_DIR=C:\Painel web

ECHO ---------------------------------
ECHO INICIANDO ATUALIZACAO AS %TIME%
ECHO ---------------------------------

ECHO 1. GERANDO NOVO PAINEL (index.html)...
"%PYTHON_EXECUTAVEL%" "%PAINEL_DIR%\gera_agenda.py"
PAUSE
IF ERRORLEVEL 1 (
    ECHO ERRO NO PASSO 1: O script Python falhou. Verifique se as dependencias estao instaladas.
    GOTO END
)

ECHO ---------------------------------
ECHO 2. ENVIANDO MUDANCAS PARA O GITHUB...
REM Navega para a pasta para garantir que o Git funcione
cd "%PAINEL_DIR%"

ECHO Adicionando arquivos...
git add .
PAUSE

ECHO Registrando mudanca (commit)...
git commit -m "Atualizacao rapida de agenda as %TIME%"
PAUSE

ECHO Enviando para a nuvem (push)...
git push origin main
PAUSE

ECHO ---------------------------------
ECHO SUCESSO! A PAGINA ESTARA ATUALIZADA EM ATE 2 MINUTOS.
ECHO Pressione qualquer tecla para finalizar.
GOTO END

:END
ECHO ---------------------------------
ECHO !!! HOUVE UMA FALHA NA ATUALIZACAO. Verifique a ultima tela de erro.
PAUSE