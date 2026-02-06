# MediaBibli - Guide pour Agents de Code

## Vue d'ensemble du projet

**MediaBibli** est une application web Django en cours de développement destinée à la gestion d'une bibliothèque de médias en ligne. Le projet est configuré en français et intègre un système de "skills" documentant les bonnes pratiques de développement.

### Caractéristiques principales

- **Framework**: Django 5.2.11
- **Langue**: Français (fr-fr)
- **Fuseau horaire**: Europe/Paris
- **Base de données**: SQLite3 (développement)
- **Localisation**: France (configuration UNIMARC pour données bibliographiques)

---

## Structure du projet

```
/path/to/MediaBibli/
├── app/                      # Configuration principale Django
│   ├── __init__.py
│   ├── asgi.py              # Configuration ASGI
│   ├── settings.py          # Paramètres Django
│   ├── urls.py              # Routage URL principal
│   └── wsgi.py              # Configuration WSGI
├── home/                     # Application Django principale
│   ├── __init__.py
│   ├── admin.py             # Configuration admin Django
│   ├── apps.py              # Configuration de l'application
│   ├── migrations/          # Migrations de base de données
│   ├── models.py            # Modèles de données (actuellement vide)
│   ├── templates/
│   │   └── home/
│   │       └── index.html   # Template page d'accueil
│   ├── tests.py             # Tests (actuellement vide)
│   ├── urls.py              # Routage URL de l'app home
│   └── views.py             # Vues (home_view simple)
├── templates/
│   └── base.html            # Template de base
├── xml/                     # Données bibliographiques UNIMARC
│   ├── Anor.xml
│   └── Fourmies-36087 (1).xml
├── skills/                  # Documentation des bonnes pratiques
│   ├── README.md
│   └── [20+ skills]/
│       ├── SKILL.md
│       └── QUICKSTART.md
├── manage.py                # Utilitaire de commande Django
├── requirements.txt         # Dépendances Python
├── db.sqlite3              # Base de données SQLite
├── .pre-commit-config.yaml  # Configuration pre-commit hooks
├── .secrets.baseline        # Baseline pour détection de secrets
└── .gitignore              # Fichiers ignorés par Git
```

---

## Stack technique

### Dépendances principales

| Catégorie | Outil | Version |
|-----------|-------|---------|
| Framework Web | Django | 5.2.11 |
| Authentification | django-allauth | 65.13.0 |
| API REST | djangorestframework | 3.16.0 |
| JWT | djangorestframework-simplejwt | 5.5.1 |
| Admin | django-unfold | 0.71.0 |
| Tailwind CSS | django-tailwind | 4.4.1 |
| Éditeur | django-ckeditor-5 | 0.2.17 |
| Sécurité | django-csp | 4.0 |
| Rate Limiting | django-ratelimit | 4.1.0 |
| Protection login | django-axes | 8.0.0 |

### Dépendances de développement et sécurité

- **Linting/Formatage**: black, flake8, pylint, mypy, ruff, isort
- **Sécurité**: bandit, detect-secrets, pip-audit
- **Tests**: pytest, pytest-cov, pytest-django
- **Pre-commit**: pre_commit

### Données bibliographiques

- **pymarc**: 5.2.3 (manipulation de notices UNIMARC/MARC)
- **lxml**: 6.0.0 (parsing XML)

---

## Commandes de build et développement

### Environnement virtuel

```bash
# L'environnement virtuel est déjà créé dans le dossier `env/`
# Activation Windows:
.\env\Scripts\activate

# Activation Linux/Mac:
source env/bin/activate
```

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Commandes Django

```bash
# Lancer le serveur de développement
python manage.py runserver

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Shell Django
python manage.py shell

# Collecter les fichiers statiques
python manage.py collectstatic
```

### Tests

```bash
# Exécuter tous les tests
pytest

# Ou avec Django
python manage.py test

# Avec couverture
pytest --cov=. --cov-report=html
```

---

## Conventions de code

### Style Python

Le projet utilise les outils de linting et formatage suivants:

1. **Black** - Formateur de code opinioné
   - Longueur de ligne: 88 caractères par défaut
   - Cible: Python 3.8+

2. **isort** - Organisation des imports
   - Profil: black (compatibilité)

3. **Flake8** - Vérification de style
   - Max line length: 88
   - Ignore: E203, W503

4. **Pylint** - Analyse statique avancée
   - Désactivations communes: C0103, C0114, C0115, C0116, R0903, R0913

5. **MyPy** - Vérification de types
   - `disallow_untyped_defs = true` recommandé

6. **Ruff** - Linter ultra-rapide (Rust)
   - Remplace flake8, pylint, isort

### Workflow de linting recommandé

```bash
# 1. Formatage
black .
isort .

# 2. Linting
flake8 .
pylint home/ app/
mypy home/ app/

# Ou avec Ruff uniquement
ruff format .
ruff check .
```

### Conventions Django

- **Modèles**: noms en minuscules, singulier (ex: `Book`, `Author`)
- **Vues**: suffixe `_view` pour les vues fonctions
- **Templates**: organisation par application (`templates/app_name/`)
- **URLs**: noms des patterns en minuscules avec tirets (ex: `book-detail`)

---

## Stratégie de tests

### Structure des tests

```
home/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_forms.py
```

### Configuration pytest (à ajouter dans pyproject.toml)

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "app.settings"
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = ["-v", "--tb=short", "--strict-markers"]
```

### Principes FIRST

- **F**ast: Tests rapides (< 100ms par test)
- **I**ndependent: Pas de dépendance entre tests
- **R**epeatable: Résultats identiques à chaque exécution
- **S**elf-validating: Assertions claires (pass/fail)
- **T**imely: Écrits en parallèle du code

---

## Sécurité

### Outils de sécurité configurés

1. **detect-secrets** - Détection de secrets dans le code
   - Baseline: `.secrets.baseline`
   - Commande: `detect-secrets scan`

2. **bandit** - Analyse statique de sécurité Python
   - Exclusion: tests, venv, migrations
   - Commande: `bandit -r . -ll`

3. **pip-audit** - Vérification des vulnérabilités de dépendances
   - Commande: `pip-audit --desc`

4. **pre-commit** - Vérifications automatiques avant commit
   - Configuration: `.pre-commit-config.yaml`
   - Installation: `pre-commit install`

### Fichiers sensibles (dans .gitignore)

- `.env`, `.env.*`
- `*.key`, `*.pem`, `*.p12`
- `local_settings.py`, `settings.local.py`
- `credentials.json`

### Vérifications avant push

```bash
# Vérification rapide (30 secondes)
detect-secrets scan
bandit -r . -ll -x tests,venv,env,__pycache__
pip-audit --desc

# Vérification complète (2 minutes)
pre-commit run --all-files
```

---

## Skills disponibles

Le dossier `skills/` contient 20 modules de documentation:

| Skill | Description |
|-------|-------------|
| `python-linting` | Black, flake8, pylint, mypy, ruff |
| `security-check` | detect-secrets, bandit, pip-audit |
| `testing` | pytest, factories, mocks, coverage |
| `django-best-practices` | Architecture, modèles, vues, sécurité |
| `django-rest` | DRF, JWT, sérialiseurs, ViewSets |
| `sql-postgresql` | Modélisation, optimisation SQL |
| `clean-code` | Principes Clean Code |
| `solid` | Principes SOLID |
| `git-workflow` | Conventional Commits, stratégies de branches |
| `tailwindcss` | Configuration, composants, responsive |
| `htmx` | Interfaces dynamiques sans JS complexe |
| `docker-containers` | Containerisation Django |
| `ci-cd-pipeline` | GitHub Actions, automatisation |
| `deployment` | Déploiement production |
| `performance-optimization` | Cache, requêtes N+1, index |
| `error-monitoring` | Sentry, logging |
| `environment-management` | Variables d'environnement |
| `frontend-assets-pipeline` | CSS/JS compilation |
| `api-documentation` | Documentation API automatique |
| `async-tasks` | Celery, tâches en arrière-plan |
| `unimarc-bibliographic` | Import notices bibliographiques |

Chaque skill contient:
- `SKILL.md` - Guide complet
- `QUICKSTART.md` - Référence rapide
- Scripts (quand applicable)

---

## Configuration actuelle

### Paramètres Django (app/settings.py)

```python
# Clé secrète (à changer en production!)
SECRET_KEY = "django-insecure-..."

# Mode debug (False en production)
DEBUG = True

# Hôtes autorisés (à configurer en production)
ALLOWED_HOSTS = []

# Applications installées
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home",
]

# Base de données
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Internationalisation
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True
```

### URLs (app/urls.py)

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
]
```

---

## Données UNIMARC

Le dossier `xml/` contient des notices bibliographiques au format UNIMARC (format d'échange pour les bibliothèques). Ces fichiers sont utilisés pour:

- Importer des catalogues bibliographiques
- Migrer depuis PMB (Système Intégré de Gestion de Bibliothèque)
- Alimenter la base de données MediaBibli

Format: XML avec structure UNIMARC standard (zones 001, 200, 210, etc.)

---

## Déploiement

### Prérequis production

1. Changer `SECRET_KEY` (variable d'environnement)
2. Définir `DEBUG = False`
3. Configurer `ALLOWED_HOSTS`
4. Utiliser PostgreSQL (recommandé)
5. Configurer whitenoise pour les fichiers statiques
6. Utiliser gunicorn comme serveur WSGI

### Variables d'environnement recommandées

```bash
DJANGO_SECRET_KEY=votre-cle-secrete
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=votredomaine.com,www.votredomaine.com
DATABASE_URL=postgres://user:pass@localhost/dbname
```

---

## Notes pour les agents de code

1. **Langue du projet**: Tous les commentaires, docstrings et messages utilisateur doivent être en français.

2. **Structure des templates**: Hériter de `base.html`, utiliser les blocs `{% block title %}` et `{% block %}`.

3. **Modèles**: Actuellement vides - à créer selon les besoins (Book, Author, etc.)

4. **Données bibliographiques**: Voir le skill `unimarc-bibliographic` pour l'import XML.

5. **Sécurité**: TOUJOURS exécuter les vérifications avant commit:
   ```bash
   pre-commit run --all-files
   ```

6. **Base de données**: SQLite pour le dev, PostgreSQL recommandé pour la production (voir skill `sql-postgresql`).

7. **Tests**: Aucun test existant - à développer selon le skill `testing`.

8. **Skills**: Consulter les skills avant toute tâche complexe (architecture, sécurité, performance).
