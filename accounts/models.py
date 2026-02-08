"""
Modèles de l'app accounts.
"""

from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Manager personnalisé pour le modèle CustomUser."""

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "CustomUser":
        """Crée et sauvegarde un utilisateur avec l'email et le mot de passe donnés."""
        if not email:
            raise ValueError(_("L'adresse email est obligatoire"))

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        from typing import cast

        return cast("CustomUser", user)

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "CustomUser":
        """Crée et sauvegarde un superutilisateur avec email et mot de passe donnés."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "superadmin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Le superutilisateur doit avoir is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Le superutilisateur doit avoir is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé avec email comme identifiant."""

    ROLE_CHOICES = [
        ("superadmin", _("Super Administrateur")),
        ("library_admin", _("Administrateur de médiathèque")),
        ("reader", _("Lecteur")),
    ]

    email = models.EmailField(
        verbose_name=_("Adresse email"),
        unique=True,
        help_text=_("L'adresse email servira d'identifiant de connexion"),
    )
    first_name = models.CharField(verbose_name=_("Prénom"), max_length=150, blank=True)
    last_name = models.CharField(verbose_name=_("Nom"), max_length=150, blank=True)
    phone = models.CharField(verbose_name=_("Téléphone"), max_length=20, blank=True)
    role = models.CharField(
        verbose_name=_("Rôle"),
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader",
        db_index=True,
        help_text=_("Le rôle détermine les permissions de l'utilisateur"),
    )
    library = models.ForeignKey(
        "libraries.Library",
        verbose_name=_("Médiathèque"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="users",
    )
    is_active = models.BooleanField(
        verbose_name=_("Actif"),
        default=True,
        db_index=True,
        help_text=_("Désactivez cette case pour désactiver le compte"),
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff"),
        default=False,
        help_text=_("Détermine si l'utilisateur peut accéder à l'admin"),
    )
    date_joined = models.DateTimeField(
        verbose_name=_("Date d'inscription"), auto_now_add=True, db_index=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["role", "library"]),
            models.Index(fields=["is_active", "date_joined"]),
        ]

    def __str__(self) -> str:
        """Retourne la représentation textuelle de l'utilisateur."""
        return str(self.email)

    @property
    def is_superadmin(self) -> bool:
        """Vérifie si l'utilisateur est un superadmin."""
        return bool(self.role == "superadmin")

    @property
    def is_library_admin(self) -> bool:
        """Vérifie si l'utilisateur est un admin de médiathèque."""
        return bool(self.role == "library_admin")

    @property
    def is_reader(self) -> bool:
        """Vérifie si l'utilisateur est un lecteur."""
        return bool(self.role == "reader")

    def get_full_name(self) -> str:
        """Retourne le nom complet de l'utilisateur."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or str(self.email)

    def get_short_name(self) -> str:
        """Retourne le prénom de l'utilisateur."""
        short_name = str(self.first_name)
        return short_name or str(self.email)
