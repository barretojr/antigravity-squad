<#
.SYNOPSIS
    Script de instalação e distribuição do Antigravity Autonomous Engineering Squad.
.DESCRIPTION
    Permite instalar o esquadrão de agentes em um projeto específico (.antigravity)
    ou de forma global no Antigravity CLI para estar disponível em qualquer diretório.
.PARAMETER TargetProject
    Caminho do projeto onde a pasta .antigravity será instalada.
.PARAMETER Global
    Se informado, instala o esquadrão no diretório global do Antigravity CLI (~/.gemini/antigravity-cli).
#>
param(
    [string]$TargetProject,
    [switch]$Global
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceDir = Join-Path $ScriptDir ".antigravity"

Write-Host "`n🚀 [Antigravity Squad Installer]`n" -ForegroundColor Cyan

if (-not (Test-Path $SourceDir)) {
    Write-Error "Pasta '.antigravity' não foi encontrada em: $ScriptDir"
    exit 1
}

# Modo Global
if ($Global) {
    $GlobalSkillsDir = Join-Path $HOME ".gemini\antigravity-cli\skills\antigravity-squad"
    Write-Host "📦 Instalando globalmente em: $GlobalSkillsDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $GlobalSkillsDir -Force | Out-Null
    Copy-Item -Path "$SourceDir\*" -Destination $GlobalSkillsDir -Recurse -Force
    Write-Host "✅ Esquadrão instalado globalmente com sucesso!" -ForegroundColor Green
    Write-Host "Agora você pode usar o comando /teamwork em qualquer projeto no Antigravity." -ForegroundColor White
    exit 0
}

# Se o TargetProject não foi passado, exibe menu interativo
if ([string]::IsNullOrWhiteSpace($TargetProject)) {
    Write-Host "Escolha como deseja instalar:" -ForegroundColor White
    Write-Host "1) No projeto atual ($(Get-Location))" -ForegroundColor Gray
    Write-Host "2) Informar o caminho de outro projeto" -ForegroundColor Gray
    Write-Host "3) Globalmente na máquina (~/.gemini/antigravity-cli)" -ForegroundColor Gray
    Write-Host "q) Cancelar" -ForegroundColor Gray

    $choice = Read-Host "`nOpção"
    switch ($choice) {
        "1" { $TargetProject = (Get-Location).Path }
        "2" { $TargetProject = Read-Host "Digite o caminho completo da raiz do projeto" }
        "3" {
            $GlobalSkillsDir = Join-Path $HOME ".gemini\antigravity-cli\skills\antigravity-squad"
            Write-Host "`n📦 Instalando globalmente em: $GlobalSkillsDir" -ForegroundColor Yellow
            New-Item -ItemType Directory -Path $GlobalSkillsDir -Force | Out-Null
            Copy-Item -Path "$SourceDir\*" -Destination $GlobalSkillsDir -Recurse -Force
            Write-Host "✅ Esquadrão instalado globalmente com sucesso!`n" -ForegroundColor Green
            exit 0
        }
        default {
            Write-Host "Operação cancelada." -ForegroundColor Yellow
            exit 0
        }
    }
}

if (-not (Test-Path $TargetProject)) {
    Write-Error "O diretório informado não existe: $TargetProject"
    exit 1
}

$DestPath = Join-Path $TargetProject ".antigravity"
Write-Host "`n📁 Copiando esquadrão para: $DestPath" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $DestPath -Force | Out-Null
Copy-Item -Path "$SourceDir\*" -Destination $DestPath -Recurse -Force

Write-Host "✅ Instalação concluída com sucesso!" -ForegroundColor Green
Write-Host "Para utilizar, abra o Antigravity neste projeto e digite no chat:" -ForegroundColor White
Write-Host "   /teamwork [sua demanda aqui]" -ForegroundColor Cyan
Write-Host ""
