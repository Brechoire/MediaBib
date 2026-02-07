"""
Fixtures et factories pour les tests.
"""

import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def client():
    """Fixture pour le client de test Django."""
    from django.test import Client
    return Client()


@pytest.fixture
def superadmin_user(db):
    """Fixture pour créer un utilisateur superadmin."""
    return User.objects.create_superuser(
        email="superadmin@mediabib.com",
        password="SuperAdmin123!",
        first_name="Super",
        last_name="Admin",
        role="superadmin"
    )


@pytest.fixture
def library_admin_user(db):
    """Fixture pour créer un utilisateur admin de médiathèque."""
    return User.objects.create_user(
        email="library@mediabib.com",
        password="Library123!",
        first_name="Library",
        last_name="Admin",
        role="library_admin"
    )


@pytest.fixture
def reader_user(db):
    """Fixture pour créer un utilisateur lecteur."""
    return User.objects.create_user(
        email="reader@mediabib.com",
        password="Reader123!",
        first_name="John",
        last_name="Reader",
        role="reader"
    )
