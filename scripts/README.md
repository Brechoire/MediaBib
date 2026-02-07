# Workflow de Test Local - MediaBibli

Ce dossier contient les scripts et configurations pour exécuter le workflow CI/CD en local, avant de push sur GitHub.

## 📋 Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Méthode 1 : Pre-commit (automatique)](#méthode-1--pre-commit-automatique)
  - [Méthode 2 : Script CI Local (manuel)](#méthode-2--script-ci-local-manuel)
- [Workflow GitHub Actions](#workflow-github-actions)
- [Troubleshooting](#troubleshooting)
- [Commandes Récapitulatives](#commandes-récapitulatives)

---

## Prérequis

- **Python 3.11+** installé
- **PowerShell 5.1+** (Windows)
- **Git** installé
- Environnement virtuel activé (`env`)

### Vérification des prérequis

```powershell
# Vérifier Python
python --version  # Doit afficher 3.11 ou supérieur

# Vérifier PowerShell
$PSVersionTable.PSVersion  # Doit être 5.1 ou supérieur

# Vérifier Git
git --version
```

---

## Installation

### 1. Installer les hooks pre-commit

```powershell
# Assurez-vous d'être dans le répertoire du projet
cd C:\Python\MediaBibli

# Activer l'environnement virtuel
.\env\Scripts\activate

# Installer pre-commit
pip install pre-commit

# Installer les hooks
cd ..  # Remonter dans le répertoire parent
pre-commit install
```

### 2. Vérifier l'installation

```powershell
# Tester les hooks sur tous les fichiers (première fois)
pre-commit run --all-files
```

**Note :** La première exécution télécharge et installe tous les outils, cela peut prendre 2-3 minutes.

---

## Utilisation

### Méthode 1 : Pre-commit (automatique)

Les hooks s'exécutent **automatiquement** à chaque commit.

```powershell
# Faire des modifications dans le code
# ...

# Ajouter les fichiers modifiés
git add .

# Commit (les hooks s'exécutent automatiquement)
git commit -m "feat: ajout de la nouvelle fonctionnalité"

# Si les hooks échouent, corrigez et recommitez
```

#### Options avancées pre-commit

```powershell
# Forcer l'exécution de tous les hooks sur tous les fichiers
pre-commit run --all-files

# Exécuter un hook spécifique
pre-commit run black
pre-commit run ruff
pre-commit run mypy

# Ignorer les hooks pour un commit spécifique (⚠️ déconseillé)
git commit -m "message" --no-verify

# Mettre à jour les hooks vers les dernières versions
pre-commit autoupdate
```

### Méthode 2 : Script CI Local (manuel)

Utilisez ce script avant de push pour vérifier que tout passera sur GitHub.

```powershell
# Exécuter le CI complet (recommandé avant push)
.\scripts\ci-local.ps1

# Mode rapide (uniquement Ruff + tests)
.\scripts\ci-local.ps1 -Quick

# Ignorer les tests (plus rapide)
.\scripts\ci-local.ps1 -SkipTests

# Ignorer la sécurité
.\scripts\ci-local.ps1 -SkipSecurity

# Ignorer le lint
.\scripts\ci-local.ps1 -SkipLint
```

#### Ce que vérifie le script

Le script exécute **exactement** les mêmes vérifications que GitHub Actions :

1. **Lint (5 étapes)** :
   - ✅ Black (formatage)
   - ✅ isort (imports)
   - ✅ Ruff (lint rapide)
   - ✅ Flake8 (lint complémentaire)
   - ✅ MyPy (types)

2. **Tests (2 étapes)** :
   - ✅ Migrations Django
   - ✅ pytest avec coverage

3. **Sécurité (4 étapes)** :
   - ✅ detect-secrets (secrets)
   - ✅ Bandit (vulnérabilités Python)
   - ✅ pip-audit (vulnérabilités dépendances)
   - ✅ Vérification fichiers sensibles

---

## Workflow GitHub Actions

Le fichier `.github/workflows/ci.yml` définit le workflow CI qui s'exécute sur GitHub :

### Jobs

1. **lint** (10 min max)
   - Exécuté en premier
   - Si échec, les autres jobs ne tournent pas

2. **test** (15 min max)
   - Dépend du job `lint`
   - Exécute migrations + tests
   - Génère rapport de coverage

3. **security** (10 min max)
   - Dépend du job `lint`
   - Vérifie la sécurité du code

### Branches surveillées

Le CI s'exécute sur :
- `main`
- `master`
- `develop`

Et sur toutes les Pull Requests vers ces branches.

---

## Troubleshooting

### ❌ "pre-commit command not found"

```powershell
# Solution : Installer pre-commit
pip install pre-commit

# Ou avec l'environnement virtuel activé
.\env\Scripts\pip install pre-commit
```

### ❌ "Script cannot be loaded because running scripts is disabled"

```powershell
# PowerShell bloque l'exécution de scripts
# Solution temporaire (pour cette session)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Solution permanente (administrateur requis)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ Black modifie mes fichiers

C'est normal ! Black formate automatiquement le code.

```powershell
# Après le premier run, ajoutez les modifications
git add .
git commit -m "style: formatage avec Black"
```

### ❌ MyPy trouve des erreurs de type

```powershell
# Ignorer les imports manquants (déjà configuré)
# ou ajoutez des stubs
pip install types-requests types-PyYAML

# Pour ignorer une ligne spécifique
# type: ignore
```

### ❌ Tests lents

```powershell
# Mode rapide (uniquement tests échoués)
pytest -x

# Uniquement un fichier de test
pytest accounts/tests/test_models.py

# Avec verbose
pytest -v --tb=short
```

### ❌ Bandit bloque sur un faux positif

```python
# Pour ignorer une ligne spécifique
# nosec
```

### ❌ Fichiers sensibles détectés par erreur

Si un fichier légitime est marqué comme sensible, vérifiez :
- Qu'il est bien dans `.gitignore`
- Qu'il n'est pas commité

---

## Commandes Récapitulatives

### 🚀 Avant chaque commit

```powershell
# Méthode recommandée : les hooks s'exécutent automatiquement
git add .
git commit -m "feat: description"
```

### 🔍 Avant chaque push

```powershell
# Vérification complète
.\scripts\ci-local.ps1

# Si tout est vert, vous pouvez push
git push origin ma-branche
```

### ⚡ Mode développement rapide

```powershell
# Vérification rapide
.\scripts\ci-local.ps1 -Quick

# OU uniquement pre-commit sur fichiers modifiés
git add .
pre-commit run
```

### 🔧 Maintenance

```powershell
# Mettre à jour les outils
pre-commit autoupdate

# Nettoyer le cache
cd ..
pre-commit clean

# Réinstaller les hooks
pre-commit install --force
```

---

## Performance

| Commande | Temps estimé | Usage |
|----------|--------------|-------|
| `git commit` (hooks auto) | 10-30s | Développement quotidien |
| `pre-commit run --all-files` | 1-2min | Vérification manuelle |
| `scripts/ci-local.ps1 -Quick` | 30-60s | Avant push rapide |
| `scripts/ci-local.ps1` (complet) | 2-3min | Vérification complète |

---

## Ressources

- [Documentation Pre-commit](https://pre-commit.com/)
- [Documentation Black](https://black.readthedocs.io/)
- [Documentation Ruff](https://docs.astral.sh/ruff/)
- [Documentation MyPy](https://mypy.readthedocs.io/)
- [Documentation Bandit](https://bandit.readthedocs.io/)

---

## Support

En cas de problème persistant :
1. Vérifiez que l'environnement virtuel est activé
2. Mettez à jour les dépendances : `pip install -r requirements.txt`
3. Réinstallez pre-commit : `pre-commit install --force`
4. Consultez les logs détaillés avec `--verbose`
