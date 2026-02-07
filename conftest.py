"""Configuration pytest racine pour MediaBibli."""

import os
import sys

import django

# Setup Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# Setup Django
django.setup()
