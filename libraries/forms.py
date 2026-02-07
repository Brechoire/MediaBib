"""
Formulaires de l'app libraries.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Library

User = get_user_model()


class LibraryCreateForm(forms.ModelForm):
    """Formulaire de création d'une médiathèque avec compte admin."""

    password1 = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
        help_text=_("Mot de passe pour le compte administrateur de la médiathèque."),
    )
    password2 = forms.CharField(
        label=_("Confirmation du mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmez le mot de passe"}),
    )

    class Meta:
        model = Library
        fields = ["name", "email", "phone", "address", "postal_code", "city"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Nom de la médiathèque"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@mediatheque.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "0123456789"}),
            "address": forms.Textarea(
                attrs={"placeholder": "Adresse complète", "rows": 3}
            ),
            "postal_code": forms.TextInput(attrs={"placeholder": "75000"}),
            "city": forms.TextInput(attrs={"placeholder": "Paris"}),
        }

    def clean_password2(self) -> str:
        """Vérifie que les deux mots de passe correspondent."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Les mots de passe ne correspondent pas."))

        return password2

    def save(self, commit: bool = True) -> Library:
        """Sauvegarde la médiathèque et crée le compte admin associé."""
        library = super().save(commit=commit)

        if commit:
            # Créer l'utilisateur admin de la médiathèque
            User.objects.create_user(
                email=library.email,
                password=self.cleaned_data["password1"],
                first_name=library.name,
                last_name="Admin",
                role="library_admin",
                library=library,
            )

        return library


class LibraryUpdateForm(forms.ModelForm):
    """Formulaire de modification d'une médiathèque."""

    class Meta:
        model = Library
        fields = ["name", "phone", "address", "postal_code", "city", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Nom de la médiathèque"}),
            "phone": forms.TextInput(attrs={"placeholder": "0123456789"}),
            "address": forms.Textarea(
                attrs={"placeholder": "Adresse complète", "rows": 3}
            ),
            "postal_code": forms.TextInput(attrs={"placeholder": "75000"}),
            "city": forms.TextInput(attrs={"placeholder": "Paris"}),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": (
                        "w-4 h-4 text-primary-600 border-gray-300 "
                        "rounded focus:ring-primary-500"
                    )
                }
            ),
        }
        labels = {
            "name": "Nom de la médiathèque",
            "phone": "Téléphone",
            "address": "Adresse",
            "postal_code": "Code postal",
            "city": "Ville",
            "is_active": "Médiathèque active",
        }
        help_texts = {
            "is_active": "Décochez pour désactiver temporairement la médiathèque",
        }
