"""
URLs de l'app libraries.
"""

from django.urls import path

from .views import (
    LibraryCreateView,
    LibraryDetailView,
    LibraryListView,
    LibraryUpdateView,
)

app_name = "libraries"

urlpatterns = [
    path("", LibraryListView.as_view(), name="list"),
    path("create/", LibraryCreateView.as_view(), name="create"),
    path("<int:pk>/", LibraryDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", LibraryUpdateView.as_view(), name="update"),
]
