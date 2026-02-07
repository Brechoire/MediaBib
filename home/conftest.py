"""Configuration pytest pour l'application home."""

import os
import sys
import django

# Add the project directory to the sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()
