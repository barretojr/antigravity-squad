[CmdletBinding()]
param(
    [string]$TargetProject,
    [switch]$Global
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceDir = Join-Path $ScriptDir '.antigravity'
$Kinds = @('agents', 'rules', 'skills', 'commands')

if (-not (Test-Path -LiteralPath $SourceDir -PathType Container)) {
    throw "Pasta fonte '.antigravity' não encontrada em: $ScriptDir"
}

function Copy-SquadTo {
    param([string]$DestinationRoot)
    foreach ($Kind in $Kinds) {
        $From = Join-Path $SourceDir $Kind
        if (Test-Path -LiteralPath $From -PathType Container) {
            $To = Join-Path $DestinationRoot $Kind
            New-Item -ItemType Directory -Path $To -Force | Out-Null
            Copy-Item -Path (Join-Path $From '*') -Destination $To -Recurse -Force
        }
    }
    $SkillDir = Join-Path $DestinationRoot 'skills\antigravity-squad'
    New-Item -ItemType Directory -Path $SkillDir -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $SourceDir 'skills\antigravity-squad\SKILL.md') -Destination $SkillDir -Force
    Copy-Item -Path (Join-Path $SourceDir 'skills\antigravity-squad\templates\*') -Destination (Join-Path $SkillDir 'templates') -Recurse -Force
}

function Copy-ToGlobalConfig {
    $ConfigDir = Join-Path $HOME '.gemini\config'
    New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null
    Copy-SquadTo -DestinationRoot $ConfigDir
    $LegacySkillDir = Join-Path $HOME '.gemini\antigravity-cli\skills\antigravity-squad'
    New-Item -ItemType Directory -Path $LegacySkillDir -Force | Out-Null
    Copy-Item -Path (Join-Path $SourceDir 'skills\antigravity-squad\*') -Destination $LegacySkillDir -Recurse -Force
    Write-Host "Squad instalado globalmente em $ConfigDir." -ForegroundColor Green
}

if ($Global) {
    Copy-ToGlobalConfig
    exit 0
}

if ([string]::IsNullOrWhiteSpace($TargetProject)) {
    Write-Host '1) Instalar no diretório atual'
    Write-Host '2) Informar outro projeto'
    Write-Host '3) Instalar globalmente'
    Write-Host 'q) Cancelar'
    $Choice = Read-Host 'Opção'
    switch ($Choice) {
        '1' { $TargetProject = (Get-Location).Path }
        '2' { $TargetProject = Read-Host 'Raiz do projeto' }
        '3' { Copy-ToGlobalConfig; exit 0 }
        default { Write-Host 'Cancelado.'; exit 0 }
    }
}

if (-not (Test-Path -LiteralPath $TargetProject -PathType Container)) {
    throw "Diretório de projeto não encontrado: $TargetProject"
}
$DestDir = Join-Path $TargetProject '.agents'
New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
Copy-SquadTo -DestinationRoot $DestDir
Write-Host "Squad instalado no workspace: $DestDir" -ForegroundColor Green
Write-Host 'Reabra ou recarregue o Antigravity e invoque /antigravity-squad.'