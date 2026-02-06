# Skills - Bonnes Pratiques de Développement

Ce dossier contient des **skills** documentés de bonnes pratiques pour améliorer la qualité et la sécurité des projets Python.

## Qu'est-ce qu'un Skill ?

Un skill est un dossier documenté qui capitalise sur l'expertise accumulée pour des tâches spécifiques. Chaque skill contient :

- **SKILL.md** : Guide complet avec instructions détaillées
- **QUICKSTART.md** : Référence rapide pour les utilisateurs expérimentés
- **Scripts** : Outils prêts à l'emploi
- **Configurations** : Fichiers de configuration prêts à l'emploi

## Skills disponibles

### 🔧 python-linting

**Objectif** : Maintenir une qualité de code Python optimale avec PEP8, pylint, flake8, black, mypy et ruff.

**Quand l'utiliser** :
- Création d'un nouveau projet Python
- Avant chaque commit
- Revue de code
- Configuration CI/CD

**Installation rapide** :
```bash
pip install black isort flake8 pylint mypy ruff
```

**Documentation** : [skills/python-linting/SKILL.md](python-linting/SKILL.md)  
**Démarrage rapide** : [skills/python-linting/QUICKSTART.md](python-linting/QUICKSTART.md)

---

### 🔒 security-check

**Objectif** : Vérifier l'intégrité et la sécurité du projet avant push sur GitHub.

**Quand l'utiliser** :
- Avant chaque push (30 secondes)
- Avant création de PR (2 minutes)
- Audit mensuel complet (5 minutes)

**Installation rapide** :
```bash
pip install detect-secrets bandit pip-audit pre-commit
pre-commit install
```

**Utilisation** :
```bash
# Linux/Mac
./skills/security-check/scripts/security-check.sh

# Windows
.\skills\security-check\scripts\security-check.ps1
```

**Documentation** : [skills/security-check/SKILL.md](security-check/SKILL.md)  
**Démarrage rapide** : [skills/security-check/QUICKSTART.md](security-check/QUICKSTART.md)

---

### 🌐 django-best-practices

**Objectif** : Bonnes pratiques pour développer avec Django (architecture, modèles, vues, tests, sécurité, performance).

**Quand l'utiliser** :
- Création d'un nouveau projet Django
- Refactoring de code existant
- Revue de code Django
- Optimisation des performances

**Installation rapide** :
```bash
pip install django django-extensions django-debug-toolbar
```

**Documentation** : [skills/django-best-practices/SKILL.md](django-best-practices/SKILL.md)  
**Démarrage rapide** : [skills/django-best-practices/QUICKSTART.md](django-best-practices/QUICKSTART.md)

---

### 🗄️ sql-postgresql

**Objectif** : Bonnes pratiques SQL et PostgreSQL (modélisation, optimisation, sécurité, requêtes performantes).

**Quand l'utiliser** :
- Conception de schémas de base de données
- Optimisation de requêtes lentes
- Migration de données
- Configuration PostgreSQL

**Installation rapide** :
```bash
pip install psycopg2-binary sqlalchemy
```

**Documentation** : [skills/sql-postgresql/SKILL.md](sql-postgresql/SKILL.md)  
**Démarrage rapide** : [skills/sql-postgresql/QUICKSTART.md](sql-postgresql/QUICKSTART.md)

---

### ✨ clean-code

**Objectif** : Principes du Clean Code pour écrire du code lisible, maintenable et évolutif (applicable à tous les langages).

**Quand l'utiliser** :
- Écriture de nouveau code
- Refactoring de code legacy
- Revue de code
- Formation d'équipe

**Documentation** : [skills/clean-code/SKILL.md](clean-code/SKILL.md)  
**Démarrage rapide** : [skills/clean-code/QUICKSTART.md](clean-code/QUICKSTART.md)

---

### 🏗️ solid

**Objectif** : Les 5 principes SOLID pour concevoir des architectures logicielles robustes et maintenables (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).

**Quand l'utiliser** :
- Conception d'architectures logicielles
- Refactoring d'un code difficile à maintenir
- Revue de code orientée architecture
- Écriture de code testable et découplé

**Documentation** : [skills/solid/SKILL.md](solid/SKILL.md)  
**Démarrage rapide** : [skills/solid/QUICKSTART.md](solid/QUICKSTART.md)

---

### 📚 unimarc-bibliographic

**Objectif** : Importer et gérer des notices bibliographiques et exemplaires au format UNIMARC depuis PMB (ou autres sources) vers Django avec architecture modulaire.

**Quand l'utiliser** :
- Migration depuis PMB vers Django
- Import de catalogues bibliographiques
- Développement d'un SIGB (Système Intégré de Gestion de Bibliothèque)
- Intégration de données UNIMARC

**Installation rapide** :
```bash
pip install pymarc lxml
django-admin startapp catalog
django-admin startapp authorities
django-admin startapp items
django-admin startapp unimarc_import
```

**Documentation** : [skills/unimarc-bibliographic/SKILL.md](unimarc-bibliographic/SKILL.md)  
**Démarrage rapide** : [skills/unimarc-bibliographic/QUICKSTART.md](unimarc-bibliographic/QUICKSTART.md)

---

### 🧪 testing

**Objectif** : Bonnes pratiques pour les tests unitaires et fonctionnels (pytest, factories, mocks, coverage).

**Quand l'utiliser** :
- Écriture de nouveaux tests
- Refactoring de tests legacy
- Configuration de CI/CD
- Amélioration de la couverture de tests

**Installation rapide** :
```bash
pip install pytest pytest-cov pytest-django factory-boy
```

**Documentation** : [skills/testing/SKILL.md](testing/SKILL.md)  
**Démarrage rapide** : [skills/testing/QUICKSTART.md](testing/QUICKSTART.md)

---

### 🎨 tailwindcss

**Objectif** : Bonnes pratiques TailwindCSS (configuration, composants, responsive, dark mode, optimisation).

**Quand l'utiliser** :
- Création d'un nouveau projet Tailwind
- Refactoring de CSS legacy
- Création de composants réutilisables
- Optimisation des performances CSS

**Installation rapide** :
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Documentation** : [skills/tailwindcss/SKILL.md](tailwindcss/SKILL.md)  
**Démarrage rapide** : [skills/tailwindcss/QUICKSTART.md](tailwindcss/QUICKSTART.md)

---

### 🚀 django-rest

**Objectif** : Bonnes pratiques Django REST Framework (API REST, authentification JWT, sérialiseurs, ViewSets).

**Quand l'utiliser** :
- Création d'une nouvelle API
- Refactoring d'une API existante
- Ajout d'authentification et permissions
- Documentation API

**Installation rapide** :
```bash
pip install djangorestframework django-filter djangorestframework-simplejwt drf-spectacular
```

**Documentation** : [skills/django-rest/SKILL.md](django-rest/SKILL.md)  
**Démarrage rapide** : [skills/django-rest/QUICKSTART.md](django-rest/QUICKSTART.md)

---

### ⚡ htmx

**Objectif** : Utilisation d'HTMX avec Django pour des interfaces dynamiques sans JavaScript complexe.

**Quand l'utiliser** :
- Création d'interfaces interactives
- Mises à jour partielles de page
- Formulaires avec validation en temps réel
- Chargement dynamique de contenu

**Installation rapide** :
```html
<script src="https://unpkg.com/htmx.org@1.9.12"></script>
```

**Documentation** : [skills/htmx/SKILL.md](htmx/SKILL.md)  
**Démarrage rapide** : [skills/htmx/QUICKSTART.md](htmx/QUICKSTART.md)

---

### 📋 git-workflow

**Objectif** : Standardiser l'utilisation de Git avec Conventional Commits, stratégies de branches et revues de code.

**Quand l'utiliser** :
- Création d'un nouveau dépôt
- Mise en place de conventions d'équipe
- Avant chaque commit
- Création de Pull Requests

**Installation rapide** :
```bash
# Aliases utiles
git config --global alias.lg "log --oneline --graph --decorate --all"
```

**Documentation** : [skills/git-workflow/SKILL.md](git-workflow/SKILL.md)  
**Démarrage rapide** : [skills/git-workflow/QUICKSTART.md](git-workflow/QUICKSTART.md)

---

### 🔐 environment-management

**Objectif** : Gérer de manière sécurisée les configurations et secrets selon les environnements (dev/staging/prod).

**Quand l'utiliser** :
- Initialisation d'un nouveau projet
- Configuration des environnements multiples
- Gestion des secrets et clés API
- Déploiement sur différents serveurs

**Installation rapide** :
```bash
pip install django-environ
```

**Documentation** : [skills/environment-management/SKILL.md](environment-management/SKILL.md)  
**Démarrage rapide** : [skills/environment-management/QUICKSTART.md](environment-management/QUICKSTART.md)

---

### 🐳 docker-containers

**Objectif** : Containeriser les applications Django pour assurer la cohérence entre les environnements.

**Quand l'utiliser** :
- Nouveau projet Django
- Standardisation des environnements d'équipe
- Déploiement en production
- Mise en place de CI/CD

**Installation rapide** :
```bash
# Voir QUICKSTART.md pour Dockerfile et docker-compose.yml complets
```

**Documentation** : [skills/docker-containers/SKILL.md](docker-containers/SKILL.md)  
**Démarrage rapide** : [skills/docker-containers/QUICKSTART.md](docker-containers/QUICKSTART.md)

---

### 🔄 ci-cd-pipeline

**Objectif** : Automatiser les tests, la vérification de qualité et le déploiement à chaque modification.

**Quand l'utiliser** :
- Mise en place d'un nouveau projet
- Configuration des workflows GitHub Actions
- Automatisation des tests
- Déploiement continu

**Installation rapide** :
```bash
# Voir QUICKSTART.md pour workflows GitHub Actions
```

**Documentation** : [skills/ci-cd-pipeline/SKILL.md](ci-cd-pipeline/SKILL.md)  
**Démarrage rapide** : [skills/ci-cd-pipeline/QUICKSTART.md](ci-cd-pipeline/QUICKSTART.md)

---

### ⚡ performance-optimization

**Objectif** : Optimiser les performances des applications Django pour réduire les temps de réponse.

**Quand l'utiliser** :
- Lenteurs détectées en production
- Pages qui mettent > 2s à charger
- N+1 queries dans les logs
- Audit de performance régulier

**Installation rapide** :
```bash
pip install django-debug-toolbar django-redis
```

**Documentation** : [skills/performance-optimization/SKILL.md](performance-optimization/SKILL.md)  
**Démarrage rapide** : [skills/performance-optimization/QUICKSTART.md](performance-optimization/QUICKSTART.md)

---

### 📊 error-monitoring

**Objectif** : Mettre en place un système de monitoring complet pour détecter et tracer les erreurs.

**Quand l'utiliser** :
- Application en production
- Besoin de tracer les erreurs 500
- Monitoring de performance
- Alertes en temps réel

**Installation rapide** :
```bash
pip install sentry-sdk
```

**Documentation** : [skills/error-monitoring/SKILL.md](error-monitoring/SKILL.md)  
**Démarrage rapide** : [skills/error-monitoring/QUICKSTART.md](error-monitoring/QUICKSTART.md)

---

### 🎨 frontend-assets-pipeline

**Objectif** : Gérer, compiler et optimiser les assets frontend (CSS, JavaScript) pour Django.

**Quand l'utiliser** :
- Application avec besoin de CSS/JS avancé
- Utilisation de Tailwind CSS
- Besoin de minification et d'optimisation

**Installation rapide** :
```bash
npm install -D tailwindcss postcss autoprefixer esbuild
```

**Documentation** : [skills/frontend-assets-pipeline/SKILL.md](frontend-assets-pipeline/SKILL.md)  
**Démarrage rapide** : [skills/frontend-assets-pipeline/QUICKSTART.md](frontend-assets-pipeline/QUICKSTART.md)

---

### 🚀 deployment

**Objectif** : Déployer des applications Django en production de manière fiable et automatisée.

**Quand l'utiliser** :
- Application prête pour la production
- Mise en place d'environnements multiples
- Automatisation du déploiement
- Scalabilité et haute disponibilité

**Installation rapide** :
```bash
# Voir QUICKSTART.md pour Heroku, VPS, AWS, etc.
```

**Documentation** : [skills/deployment/SKILL.md](deployment/SKILL.md)  
**Démarrage rapide** : [skills/deployment/QUICKSTART.md](deployment/QUICKSTART.md)

---

### 📖 api-documentation

**Objectif** : Générer et maintenir une documentation API automatique et interactive.

**Quand l'utiliser** :
- API REST publique ou interne
- Équipe de développement multiple
- Intégration avec des clients externes

**Installation rapide** :
```bash
pip install drf-spectacular
```

**Documentation** : [skills/api-documentation/SKILL.md](api-documentation/SKILL.md)  
**Démarrage rapide** : [skills/api-documentation/QUICKSTART.md](api-documentation/QUICKSTART.md)

---

### ⏱️ async-tasks

**Objectif** : Exécuter des tâches en arrière-plan pour améliorer les performances.

**Quand l'utiliser** :
- Envoi d'emails
- Traitement d'images ou fichiers
- Génération de rapports
- Tâches planifiées (cron)

**Installation rapide** :
```bash
pip install celery redis django-celery-results
```

**Documentation** : [skills/async-tasks/SKILL.md](async-tasks/SKILL.md)  
**Démarrage rapide** : [skills/async-tasks/QUICKSTART.md](async-tasks/QUICKSTART.md)

## Workflow recommandé

### 1. Avant de commencer à coder

```bash
# Installer les outils des skills nécessaires
pip install -r skills/python-linting/requirements-dev.txt
pip install detect-secrets bandit pip-audit pre-commit

# Configurer le pre-commit hook
pre-commit install
```

### 2. Pendant le développement

```bash
# Après avoir modifié du code
./skills/security-check/scripts/security-check.sh

# Si tout est vert → commit
# Si erreur → corriger avant de commit
git add .
git commit -m "feat: ma fonctionnalité"
```

### 3. Avant de push

```bash
# Vérification finale
./skills/security-check/scripts/security-check.sh --full
./skills/python-linting/scripts/lint.sh  # si disponible

# Push
git push origin ma-branche
```

## Intégration CI/CD

Les skills incluent des configurations GitHub Actions prêtes à l'emploi :

```bash
# Copier les workflows dans votre projet
mkdir -p .github/workflows
cp skills/security-check/.github/workflows/security.yml .github/workflows/
cp skills/python-linting/.github/workflows/lint.yml .github/workflows/  # si disponible

git add .github/workflows/
git commit -m "ci: add security and linting checks"
```

## Comment utiliser un skill

### Méthode 1 : Lecture complète (première fois)

1. Lire le fichier `SKILL.md` complet
2. Suivre les instructions d'installation
3. Tester avec un exemple

### Méthode 2 : Démarrage rapide (utilisation quotidienne)

1. Consulter `QUICKSTART.md` pour la checklist
2. Exécuter les commandes listées
3. Vérifier les résultats

### Méthode 3 : Référence ponctuelle

1. Chercher dans `SKILL.md` la section pertinente
2. Appliquer la solution documentée

## Ajouter un nouveau skill

Pour créer un nouveau skill :

1. Créer un dossier `skills/nom-du-skill/`
2. Créer `SKILL.md` avec :
   - Objectif
   - Quand l'utiliser
   - Outils utilisés
   - Installation
   - Cas d'usage
   - Pièges à éviter
3. Créer `QUICKSTART.md` avec la checklist rapide
4. Ajouter des scripts si nécessaire

## Bonnes pratiques

- **Toujours consulter le skill** avant une tâche complexe
- **Suivre les workflows** documentés
- **Ne pas sauter les vérifications** de sécurité
- **Maintenir les skills à jour** avec les nouvelles versions des outils

## Ressources

- [Documentation Python](https://docs.python.org/3/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

*Les skills sont vivants : n'hésitez pas à les améliorer avec vos découvertes !*
