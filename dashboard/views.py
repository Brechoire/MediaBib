"""
Vues du dashboard.
"""

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render
from django.views.generic import TemplateView

from libraries.models import Library


User = get_user_model()


class DashboardAccessMixin(LoginRequiredMixin):
    """Mixin de base pour les vues du dashboard."""

    def dispatch(self, request, *args, **kwargs):
        """Redirige les lecteurs vers la page en construction."""
        # Vérifie d'abord si l'utilisateur est authentifié (par LoginRequiredMixin)
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # Puis vérifie si c'est un lecteur
        if hasattr(request.user, "is_reader") and request.user.is_reader:
            return render(request, "dashboard/reader_placeholder.html")
        return super().dispatch(request, *args, **kwargs)


class SuperAdminRequiredMixin(LoginRequiredMixin):
    """Mixin qui vérifie que l'utilisateur est un superadmin."""

    def dispatch(self, request, *args, **kwargs):
        """Vérifie si l'utilisateur est un superadmin."""
        if not request.user.is_superadmin:
            # Redirige vers le dashboard library si c'est un admin de médiothèque
            if request.user.is_library_admin:
                return render(
                    request,
                    "dashboard/library_admin.html",
                    self.get_library_context(request),
                )
            # Redirige les lecteurs
            if request.user.is_reader:
                return render(request, "dashboard/reader_placeholder.html")
        return super().dispatch(request, *args, **kwargs)

    def get_library_context(self, request):
        """Prépare le contexte pour le dashboard library admin."""
        library = request.user.library
        readers = User.objects.filter(library=library, role="reader")

        return {
            "page_title": "Ma Médiathèque",
            "breadcrumb_items": [{"label": "Dashboard", "url": None}],
            "total_readers": readers.count(),
            "readers": readers[:10],
        }


class DashboardIndexView(DashboardAccessMixin, TemplateView):
    """Vue principale du dashboard qui redirige selon le rôle."""

    template_name = "dashboard/superadmin.html"

    def get_template_names(self) -> list[str]:
        """Retourne le template approprié selon le rôle."""
        user = self.request.user

        if user.is_superadmin:
            return ["dashboard/superadmin.html"]
        elif user.is_library_admin:
            return ["dashboard/library_admin.html"]
        else:
            return ["dashboard/reader_placeholder.html"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Prépare le contexte selon le rôle."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_superadmin:
            context.update(self._get_superadmin_context())
        elif user.is_library_admin:
            context.update(self._get_library_context())

        return context

    def _get_superadmin_context(self) -> dict[str, Any]:
        """Prépare le contexte superadmin avec optimisation des requêtes."""
        # Requête unique pour toutes les statistiques utilisateurs
        user_stats = User.objects.aggregate(
            total_users=Count("id"),
            active_users=Count("id", filter=Q(is_active=True)),
            total_readers=Count("id", filter=Q(role="reader")),
            total_library_admins=Count("id", filter=Q(role="library_admin")),
        )

        # Requête unique pour les statistiques bibliothèques
        library_stats = Library.objects.aggregate(
            total_libraries=Count("id"),
            active_libraries=Count("id", filter=Q(is_active=True)),
        )

        return {
            "page_title": "Tableau de bord",
            "page_subtitle": "Vue d'ensemble de votre réseau de médiathèques",
            "breadcrumb_items": [{"label": "Dashboard", "url": None}],
            **user_stats,
            **library_stats,
            "recent_libraries": Library.objects.order_by("-created_at")[:5],
        }

    def _get_library_context(self) -> dict[str, Any]:
        """Prépare le contexte pour le dashboard library admin avec optimisation."""
        library = self.request.user.library
        # Requête unique avec annotation pour le compteur et la liste
        readers_qs = User.objects.filter(library=library, role="reader")
        readers_list = list(readers_qs[:10])

        return {
            "page_title": "Ma Médiathèque",
            "breadcrumb_items": [{"label": "Dashboard", "url": None}],
            "total_readers": len(readers_list),
            "readers": readers_list,
        }


@login_required
def reader_placeholder_view(request):
    """Vue pour les lecteurs (pas de dashboard)."""
    return render(request, "dashboard/reader_placeholder.html")
