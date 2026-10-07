# Script de Inicializacao - BRVAL Hub de Treinamentos (DP & RH)
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "         BRVAL Hub de Treinamentos (HR Tech)           " -ForegroundColor Yellow
Write-Host "   Auditoria de Elegibilidade e Integracao (3 Anos)    " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

$pythonCandidate = "C:\Users\fernando.fernandes\AppData\Local\Programs\Python\Python311\python.exe"
if (Test-Path $pythonCandidate) {
    $pythonExe = $pythonCandidate
} else {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $pythonExe = "python"
    } else {
        Write-Host "[ERRO] Executavel do Python nao localizado." -ForegroundColor Red
        Exit 1
    }
}

Write-Host "Iniciando Streamlit na porta 8501..." -ForegroundColor Green
& $pythonExe -m streamlit run app.py --server.headless false --server.port 8501
