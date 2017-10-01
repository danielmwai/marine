"""Main configurations information."""
from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Details for authentication module."""

    name = 'auth'
    verbose_name = 'User Management'
