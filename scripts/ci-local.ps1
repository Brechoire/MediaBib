#!/usr/bin/env pwsh
#Requires -Version 5.1

<#
.SYNOPSIS
    Script CI Local - Reproduit exactement le workflow GitHub Actions en local

.DESCRIPTION
    Ce script exécute toutes les vérifications du workflow GitHub Actions CI :
    - Phase 1: Lint (Black, isort, Ruff, Flake8, MyPy)
    - Phase 2: Tests (Migrations, pytest avec coverage)
    - Phase 3: Sécurité (detect-secrets, Bandit, pip-audit, fichiers sensibles)

    Le script continue même si une étape échoue pour montrer tous les problèmes.

.EXAMPLE
    .\scripts\ci-local.ps1

.EXAMPLE
    .\scripts\ci-local.ps1 -SkipTests  # Pour ignorer les tests (plus rapide)

.NOTES
    Fichier : ci-local.ps1
    Auteur  : MediaBibli Team
    Version : 1.0
#>

[CmdletBinding()]
param(
    [switch]$SkipTests,
    [switch]$SkipSecurity,
    [switch]$SkipLint,
    [switch]$Quick  # Mode rapide : uniquement Ruff + tests
)

# Configuration des couleurs
$Colors = @{
    Success = 'Green'
    Error   = 'Red'
    Warning = 'Yellow'
    Info    = 'Cyan'
    Title   = 'Magenta'
    Reset   = 'White'
}

# Variables globales
$Script:Results = @{
    Total   = 0
    Passed  = 0
    Failed  = 0
    Warnings = 0
    Steps   = @()
}
$Script:StartTime = Get-Date

# ============================================
# FONCTIONS UTILITAIRES
# ============================================

function Write-Title($Text) {
    Write-Host "`n" ('=' * 70) -ForegroundColor $Colors.Title
    Write-Host "  $Text" -ForegroundColor $Colors.Title
    Write-Host ('=' * 70) -ForegroundColor $Colors.Title
}

function Write-Step($StepNumber, $TotalSteps, $Text) {
    Write-Host "`n[$StepNumber/$TotalSteps] $Text" -ForegroundColor $Colors.Info
}

function Invoke-CIStep {
    param(
        [string]$Name,
        [scriptblock]$ScriptBlock,
        [string]$WorkingDirectory = $PSScriptRoot\..
    )

    $Script:Results.Total++
    $stepStart = Get-Date
    $currentDir = Get-Location

    try {
        Set-Location $WorkingDirectory
        & $ScriptBlock 2>&1
        $exitCode = $LASTEXITCODE
        Set-Location $currentDir

        $duration = (Get-Date) - $stepStart

        if ($exitCode -eq 0) {
            Write-Host "  ✅ $Name (" -NoNewline
            Write-Host "$($duration.ToString('mm\:ss'))" -NoNewline -ForegroundColor $Colors.Info
            Write-Host ")"
            $Script:Results.Passed++
            $Script:Results.Steps += @{ Name = $Name; Status = 'PASSED'; Duration = $duration }
            return $true
        } else {
            Write-Host "  ❌ $Name (" -NoNewline
            Write-Host "$($duration.ToString('mm\:ss'))" -NoNewline -ForegroundColor $Colors.Warning
            Write-Host ") - Exit code: $exitCode"
            $Script:Results.Failed++
            $Script:Results.Steps += @{ Name = $Name; Status = 'FAILED'; Duration = $duration; ExitCode = $exitCode }
            return $false
        }
    }
    catch {
        Set-Location $currentDir
        $duration = (Get-Date) - $stepStart
        Write-Host "  ❌ $Name (" -NoNewline
        Write-Host "$($duration.ToString('mm\:ss'))" -NoNewline -ForegroundColor $Colors.Warning
        Write-Host ") - Exception: $_"
        $Script:Results.Failed++
        $Script:Results.Steps += @{ Name = $Name; Status = 'FAILED'; Duration = $duration; Error = $_ }
        return $false
    }
}

function Show-Summary {
    $totalDuration = (Get-Date) - $Script:StartTime

    Write-Title "RÉSUMÉ DU CI LOCAL"

    Write-Host "`n📊 Statistiques :" -ForegroundColor $Colors.Info
    Write-Host "   Total des étapes : $($Script:Results.Total)"
    Write-Host "   ✅ Réussies      : $($Script:Results.Passed)" -ForegroundColor $Colors.Success
    Write-Host "   ❌ Échouées      : $($Script:Results.Failed)" -ForegroundColor $(if ($Script:Results.Failed -gt 0) { $Colors.Error } else { $Colors.Success })
    Write-Host "   ⏱️  Durée totale  : $($totalDuration.ToString('mm\:ss\.fff'))"

    if ($Script:Results.Failed -gt 0) {
        Write-Host "`n📋 Échecs détaillés :" -ForegroundColor $Colors.Error
        $Script:Results.Steps | Where-Object { $_.Status -eq 'FAILED' } | ForEach-Object {
            Write-Host "   - $($_.Name)" -ForegroundColor $Colors.Error
        }

        Write-Host "`n⚠️  Le push GitHub risque d'échouer !" -ForegroundColor $Colors.Warning
        Write-Host "   Corrigez les erreurs ci-dessus avant de push." -ForegroundColor $Colors.Warning
        exit 1
    } else {
        Write-Host "`n🎉 Toutes les vérifications ont réussi !" -ForegroundColor $Colors.Success
        Write-Host "   Vous pouvez push en toute confiance." -ForegroundColor $Colors.Success
        exit 0
    }
}

# ============================================
# DÉBUT DU SCRIPT
# ============================================

$Host.UI.RawUI.WindowTitle = "MediaBibli - CI Local"

Write-Title "🚀 CI LOCAL - MediaBibli"
Write-Host "Ce script reproduit exactement le workflow GitHub Actions CI." -ForegroundColor $Colors.Info
Write-Host "Démarrage..." -ForegroundColor $Colors.Info

# Déterminer le mode
if ($Quick) {
    Write-Host "`n⚡ Mode RAPIDE activé (Ruff + Tests uniquement)" -ForegroundColor $Colors.Warning
}

# Compter le nombre total d'étapes
$totalSteps = if ($Quick) { 4 } elseif ($SkipTests) { 9 } elseif ($SkipSecurity) { 7 } elseif ($SkipLint) { 4 } else { 13 }
$currentStep = 0

# ============================================
# PHASE 1 : LINT
# ============================================

if (-not $SkipLint -and -not $Quick) {
    Write-Title "PHASE 1/3 : LINT"

    # Étape 1: Black
    $currentStep++
    Write-Step $currentStep $totalSteps "Vérification du formatage avec Black"
    Invoke-CIStep -Name "Black" -ScriptBlock {
        black --check --diff .
    } | Out-Null

    # Étape 2: isort
    $currentStep++
    Write-Step $currentStep $totalSteps "Vérification des imports avec isort"
    Invoke-CIStep -Name "isort" -ScriptBlock {
        isort --check-only --diff --profile black .
    } | Out-Null

    # Étape 3: Ruff
    $currentStep++
    Write-Step $currentStep $totalSteps "Linting avec Ruff"
    Invoke-CIStep -Name "Ruff" -ScriptBlock {
        ruff check .
    } | Out-Null

    # Étape 4: Flake8
    $currentStep++
    Write-Step $currentStep $totalSteps "Linting avec Flake8"
    Invoke-CIStep -Name "Flake8" -ScriptBlock {
        flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203,W503
    } | Out-Null

    # Étape 5: MyPy
    $currentStep++
    Write-Step $currentStep $totalSteps "Vérification des types avec MyPy"
    Invoke-CIStep -Name "MyPy" -ScriptBlock {
        mypy . --ignore-missing-imports
    } | Out-Null
}
elseif ($Quick) {
    Write-Title "PHASE 1/2 : LINT (Rapide)"

    # Mode rapide : uniquement Ruff
    $currentStep++
    Write-Step $currentStep $totalSteps "Linting avec Ruff"
    Invoke-CIStep -Name "Ruff" -ScriptBlock {
        ruff check .
    } | Out-Null
}

# ============================================
# PHASE 2 : TESTS
# ============================================

if (-not $SkipTests) {
    Write-Title "PHASE $(if ($Quick) {'2/2'} elseif ($SkipLint) {'1/2'} elseif ($SkipSecurity) {'2/2'} else {'2/3'}) : TESTS"

    # Configuration des variables d'environnement
    $env:SECRET_KEY = "django-insecure-test-key-not-for-production"
    $env:DEBUG = "False"
    $env:DJANGO_SETTINGS_MODULE = "app.settings"

    # Étape : Migrations
    $currentStep++
    Write-Step $currentStep $totalSteps "Application des migrations Django"
    Invoke-CIStep -Name "Migrations" -ScriptBlock {
        python manage.py migrate --run-syncdb
    } | Out-Null

    # Étape : Tests avec coverage
    $currentStep++
    Write-Step $currentStep $totalSteps "Exécution des tests avec pytest"
    if ($Quick) {
        Invoke-CIStep -Name "Pytest" -ScriptBlock {
            pytest -x -q --tb=short
        } | Out-Null
    } else {
        Invoke-CIStep -Name "Pytest (with coverage)" -ScriptBlock {
            pytest --cov=. --cov-report=term --cov-report=xml
        } | Out-Null
    }
}

# ============================================
# PHASE 3 : SÉCURITÉ
# ============================================

if (-not $SkipSecurity -and -not $Quick) {
    Write-Title "PHASE $(if ($SkipLint) {'2/2'} elseif ($SkipTests) {'2/2'} else {'3/3'}) : SÉCURITÉ"

    # Étape 6: detect-secrets
    $currentStep++
    Write-Step $currentStep $totalSteps "Détection des secrets"
    Invoke-CIStep -Name "detect-secrets" -ScriptBlock {
        if (Test-Path .secrets.baseline) {
            detect-secrets scan --baseline .secrets.baseline
        } else {
            Write-Host "⚠️  Baseline non trouvée, création..." -ForegroundColor Yellow
            detect-secrets scan > .secrets.baseline
            Write-Host "📝 Baseline créée, pensez à la committer" -ForegroundColor Yellow
            return 0
        }
    } | Out-Null

    # Étape 7: Bandit
    $currentStep++
    Write-Step $currentStep $totalSteps "Analyse de sécurité avec Bandit"
    Invoke-CIStep -Name "Bandit" -ScriptBlock {
        bandit -r . -ll -x tests,venv,env,__pycache__,build,dist,node_modules,.git
    } | Out-Null

    # Étape 8: pip-audit
    $currentStep++
    Write-Step $currentStep $totalSteps "Vérification des vulnérabilités des dépendances"
    Invoke-CIStep -Name "pip-audit" -ScriptBlock {
        pip-audit -r requirements.txt --desc
    } | Out-Null

    # Étape 9: Fichiers sensibles
    $currentStep++
    Write-Step $currentStep $totalSteps "Vérification des fichiers sensibles"
    Invoke-CIStep -Name "Sensitive Files Check" -ScriptBlock {
        $sensitivePatterns = @('.env', '.key', '.pem', '.p12', '.pfx', 'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519', '.htpasswd', '.netrc')
        $foundFiles = @()

        # Récupérer la liste des fichiers git s'il y a un repo
        if (Test-Path .git) {
            $gitFiles = git ls-files 2>$null
            if ($gitFiles) {
                foreach ($pattern in $sensitivePatterns) {
                    $matches = $gitFiles | Where-Object { $_ -match $pattern }
                    if ($matches) {
                        $foundFiles += $matches
                    }
                }
            }
        }

        # Vérification directe des fichiers
        foreach ($pattern in $sensitivePatterns) {
            $files = Get-ChildItem -Path . -Name -Recurse -ErrorAction SilentlyContinue |
                Where-Object { $_ -match $pattern -and $_ -notmatch '(env|venv|__pycache__|node_modules|.git)' }
            if ($files) {
                $foundFiles += $files
            }
        }

        if ($foundFiles.Count -gt 0) {
            Write-Host "❌ Fichiers sensibles trouvés :" -ForegroundColor Red
            $foundFiles | Select-Object -Unique | ForEach-Object {
                Write-Host "   - $_" -ForegroundColor Red
            }
            return 1
        } else {
            Write-Host "✅ Aucun fichier sensible trouvé" -ForegroundColor Green
            return 0
        }
    } | Out-Null
}

# ============================================
# RÉSUMÉ FINAL
# ============================================

Show-Summary
