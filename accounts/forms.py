"""
Formulaires de l'app accounts.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SuperAdminSetupForm(UserCreationForm):
    """Formulaire d'inscription du premier superadmin."""

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Prénom"),
        widget=forms.TextInput(attrs={"placeholder": "Prénom"}),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Nom"),
        widget=forms.TextInput(attrs={"placeholder": "Nom"}),
    )
    email = forms.EmailField(
        required=True,
        label=_("Adresse email"),
        widget=forms.EmailInput(attrs={"placeholder": "email@exemple.com"}),
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def save(self, commit: bool = True) -> User:
        """Sauvegarde l'utilisateur en tant que superadmin."""
        user = super().save(commit=False)
        user.role = "superadmin"
        user.is_staff = True
        user.is_superuser = True

        if commit:
            user.save()

        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Formulaire d'authentification personnalisé."""

    username = forms.EmailField(
        label=_("Adresse email"),
        widget=forms.EmailInput(
            attrs={"placeholder": "email@exemple.com", "autocomplete": "email"}
        ),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulaire de changement de mot de passe personnalisé."""

    old_password = forms.CharField(
        label=_("Ancien mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "placeholder": "Ancien mot de passe",
            }
        ),
    )
    new_password1 = forms.CharField(
        label=_("Nouveau mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Nouveau mot de passe",
            }
        ),
    )
    new_password2 = forms.CharField(
        label=_("Confirmation du nouveau mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Confirmez le nouveau mot de passe",
            }
        ),
    )
