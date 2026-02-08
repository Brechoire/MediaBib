"""
Fixtures et factories pour les tests.
"""

from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from accounts.models import CustomUser

User = get_user_model()


@pytest.fixture
def client() -> Client:
    """Fixture pour le client de test Django."""
    return Client()


@pytest.fixture
def superadmin_user(db: Any) -> CustomUser:
    """Fixture pour créer un utilisateur superadmin."""
    from typing import cast

    user = User.objects.create_superuser(
        email="superadmin@mediabib.com",
        password="SuperAdmin123!",
        first_name="Super",
        last_name="Admin",
        role="superadmin",
    )
    return cast(CustomUser, user)


@pytest.fixture
def library_admin_user(db: Any) -> CustomUser:
    """Fixture pour créer un utilisateur admin de médiathèque."""
    from typing import cast

    user = User.objects.create_user(
        email="library@mediabib.com",
        password="Library123!",
        first_name="Library",
        last_name="Admin",
        role="library_admin",
    )
    return cast(CustomUser, user)


@pytest.fixture
def reader_user(db: Any) -> CustomUser:
    """Fixture pour créer un utilisateur lecteur."""
    from typing import cast

    user = User.objects.create_user(
        email="reader@mediabib.com",
        password="Reader123!",
        first_name="John",
        last_name="Reader",
        role="reader",
    )
    return cast(CustomUser, user)
