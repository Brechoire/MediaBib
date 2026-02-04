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
