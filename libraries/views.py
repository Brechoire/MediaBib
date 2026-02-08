"""
Vues de l'app libraries.
"""

from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, QuerySet
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import LibraryCreateForm, LibraryUpdateForm
from .models import Library


class SuperAdminRequiredMixin(UserPassesTestMixin):
    """Mixin qui vérifie que l'utilisateur est un superadmin."""

    def test_func(self) -> bool:
        """Vérifie si l'utilisateur est un superadmin."""
        from typing import cast

        user = self.request.user
        is_auth = cast(bool, user.is_authenticated)
        is_super = cast(bool, user.is_superadmin)
        return is_auth and is_super


class LibraryAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin qui vérifie que l'utilisateur est un admin de médiathèque."""

    def test_func(self) -> bool:
        """Vérifie si l'utilisateur est un admin de médiathèque."""
        if not self.request.user.is_authenticated:
            return False
        # Superadmin peut tout faire
        if self.request.user.is_superadmin:
            return True
        # Library admin peut modifier sa propre médiathèque
        return (
            self.request.user.is_library_admin and self.request.user.library is not None
        )


class LibraryListView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    """Liste des médiathèques (pour les superadmins)."""

    model = Library
    template_name = "libraries/library_list.html"
    context_object_name = "libraries"
    ordering = ["-created_at"]
    paginate_by = 25  # Pagination pour optimiser les performances

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Ajoute des informations au contexte."""
        from typing import cast

        context = cast(dict[str, Any], super().get_context_data(**kwargs))
        context["breadcrumb_items"] = [
            {"label": "Médiathèques", "url": None},
        ]
        return context


class LibraryCreateView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    """Création d'une médiathèque (pour les superadmins)."""

    model = Library
    form_class = LibraryCreateForm
    template_name = "libraries/library_form.html"
    success_url = reverse_lazy("libraries:list")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Ajoute des informations au contexte."""
        from typing import cast

        context = cast(dict[str, Any], super().get_context_data(**kwargs))
        context["title"] = "Créer une médiathèque"
        context["breadcrumb_items"] = [
            {"label": "Médiathèques", "url": reverse_lazy("libraries:list")},
            {"label": "Créer", "url": None},
        ]

        # Récupérer le mot de passe généré de la session (affichage unique)
        generated_password = self.request.session.pop("generated_password", None)
        if generated_password:
            context["generated_password"] = generated_password
            # Marquer la session comme modifiée pour s'assurer que le pop est sauvegardé
            self.request.session.modified = True

        return context

    def form_valid(self, form: LibraryCreateForm) -> HttpResponse:
        """Sauvegarde et stocke le mot de passe en clair pour affichage."""
        from typing import cast

        # Récupérer le mot de passe avant qu'il ne soit hashé
        password = form.cleaned_data.get("password1")

        response = cast(HttpResponse, super().form_valid(form))

        # Stocker le mot de passe en clair dans la session
        if password:
            self.request.session["generated_password"] = password

        # Message de succès
        messages.success(
            self.request,
            f"La médiathèque '{self.object.name}' a été créée avec succès !",
        )

        return response


class LibraryUpdateView(LibraryAdminRequiredMixin, UpdateView):
    """Modification d'une médiathèque."""

    model = Library
    form_class = LibraryUpdateForm
    template_name = "libraries/library_update.html"
    pk_url_kwarg = "pk"

    def get_queryset(self) -> QuerySet[Library]:
        """Restreint la modification selon le rôle de l'utilisateur."""
        if self.request.user.is_superadmin:
            # Superadmin peut modifier toutes les médiathèques
            return Library.objects.all()
        else:
            # Library admin peut uniquement modifier sa propre médiathèque
            return Library.objects.filter(pk=self.request.user.library_id)

    def get_object(self, queryset: QuerySet[Library] | None = None) -> Library:
        """Récupère l'objet avec vérification des permissions."""
        from typing import cast

        obj = cast(Library, super().get_object(queryset))

        # Vérifier que le library admin ne modifie que sa propre médiathèque
        if (
            not self.request.user.is_superadmin
            and obj.pk != self.request.user.library_id
        ):
            raise Http404(
                "Vous n'avez pas la permission de modifier cette médiathèque."
            )

        return obj

    def get_success_url(self) -> str:
        """Redirige vers la page appropriée après modification."""
        if self.request.user.is_superadmin:
            return str(reverse_lazy("libraries:list"))
        else:
            return str(reverse_lazy("dashboard:index"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Ajoute des informations au contexte."""
        from typing import cast

        context = cast(dict[str, Any], super().get_context_data(**kwargs))
        context["title"] = f"Modifier : {self.object.name}"

        if self.request.user.is_superadmin:
            context["breadcrumb_items"] = [
                {"label": "Médiathèques", "url": reverse_lazy("libraries:list")},
                {"label": self.object.name, "url": None},
            ]
        else:
            context["breadcrumb_items"] = [
                {"label": "Ma médiathèque", "url": reverse_lazy("dashboard:index")},
                {"label": "Modifier", "url": None},
            ]

        return context

    def form_valid(self, form: LibraryUpdateForm) -> HttpResponse:
        """Sauvegarde le formulaire et affiche un message de succès."""
        from typing import cast

        response = cast(HttpResponse, super().form_valid(form))
        messages.success(
            self.request,
            f"'{self.object.name}' a été mis à jour avec succès !",
        )
        return response


class LibraryDetailView(LoginRequiredMixin, DetailView):
    """Détail d'une médiathèque."""

    model = Library
    template_name = "libraries/library_detail.html"
    context_object_name = "library"
    pk_url_kwarg = "pk"

    def get_queryset(self) -> QuerySet[Library]:
        """Optimise la requête avec l'annotation du nombre d'utilisateurs."""
        return Library.objects.annotate(user_count=Count("users"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Ajoute des informations au contexte."""
        from typing import cast

        context = cast(dict[str, Any], super().get_context_data(**kwargs))
        context["breadcrumb_items"] = [
            {"label": "Médiathèques", "url": reverse_lazy("libraries:list")},
            {"label": self.object.name, "url": None},
        ]
        return context
