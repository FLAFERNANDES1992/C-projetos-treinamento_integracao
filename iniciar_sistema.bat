@echo off
chcp 65001 > nul
title BRVAL Hub de Treinamentos - DP & RH

echo =======================================================
echo          BRVAL Hub de Treinamentos (HR Tech)
echo       Auditoria de Elegibilidade e Integracao (3 Anos)
echo =======================================================
echo.
echo [1/2] Localizando ambiente Python...

set "PYTHON_EXE=C:\Users\fernando.fernandes\AppData\Local\Programs\Python\Python311\python.exe"

if not exist "%PYTHON_EXE%" (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_EXE=python"
    ) else (
        echo [ERRO] Python nao foi encontrado no caminho padrao nem no PATH do sistema.
        pause
        exit /b 1
    )
)

echo [2/2] Iniciando aplicacao Streamlit em http://localhost:8501 ...
echo.
echo Pressione CTRL+C na janela para encerrar o servidor.
echo.

"%PYTHON_EXE%" -m streamlit run app.py --server.headless false --server.port 8501

pause
