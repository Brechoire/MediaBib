"""
URLs du dashboard.
"""

from django.urls import path

from .views import DashboardIndexView, reader_placeholder_view


app_name = "dashboard"

urlpatterns = [
    path("", DashboardIndexView.as_view(), name="index"),
    path("reader/", reader_placeholder_view, name="reader"),
]
