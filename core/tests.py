import io

from django.conf import settings
from django.core.management import call_command, get_commands
from django.test import TestCase
from django_permissions_policy.__init__ import _FEATURE_NAMES

PERMISSIONS_POLICY = list(getattr(settings, "PERMISSIONS_POLICY", None))


def test_check_current_permission_policy_items():
    """
    Check to make sure that the keys in the current PERMISSIONS_POLICY exist
    in the version of django-permissions-policy. This will help to keep you
    from upgrading to a version that will generate 500 errors on your website
    """
    for i in PERMISSIONS_POLICY:
        assert i in _FEATURE_NAMES


class DjangoModelInfoTestCase(TestCase):
    """Test case for django-model-info integration"""

    def test_django_model_info_installed(self):
        """Test that django-model-info app is properly installed in DEBUG mode"""
        if settings.DEBUG:
            self.assertIn("django_model_info.apps.DjangoModelInfoConfig", settings.INSTALLED_APPS)

    def test_django_model_info_commands_registered(self):
        """Test that all django-model-info management commands are registered"""
        if settings.DEBUG:
            commands = get_commands()
            expected_commands = ["modelinfo", "modelfilters", "modelgraph", "migrationgraph"]
            for cmd in expected_commands:
                self.assertIn(cmd, commands, f"Command '{cmd}' should be registered")

    def test_modelinfo_command_help(self):
        """Test that modelinfo command help works properly"""
        if settings.DEBUG:
            try:
                # Capture stdout to prevent output during test
                stdout = io.StringIO()
                call_command("modelinfo", "--help", stdout=stdout)
                help_output = stdout.getvalue()
                self.assertIn("fields and methods for each model", help_output)
            except Exception as e:
                self.fail(f"modelinfo command help failed: {e}")

    def test_modelfilters_command_help(self):
        """Test that modelfilters command help works properly"""
        if settings.DEBUG:
            try:
                # Capture stdout to prevent output during test
                stdout = io.StringIO()
                call_command("modelfilters", "--help", stdout=stdout)
                help_output = stdout.getvalue()
                self.assertIn("Show the available filters for model", help_output)
            except Exception as e:
                self.fail(f"modelfilters command help failed: {e}")

    def test_modelgraph_command_help(self):
        """Test that modelgraph command help works properly"""
        if settings.DEBUG:
            try:
                # Capture stdout to prevent output during test
                stdout = io.StringIO()
                call_command("modelgraph", "--help", stdout=stdout)
                help_output = stdout.getvalue()
                self.assertIn("Create a graph of models", help_output)
            except Exception as e:
                self.fail(f"modelgraph command help failed: {e}")

    def test_migrationgraph_command_help(self):
        """Test that migrationgraph command help works properly"""
        if settings.DEBUG:
            try:
                # Capture stdout to prevent output during test
                stdout = io.StringIO()
                call_command("migrationgraph", "--help", stdout=stdout)
                help_output = stdout.getvalue()
                self.assertIn("Create a graph of migration", help_output)
            except Exception as e:
                self.fail(f"migrationgraph command help failed: {e}")

    def test_django_model_info_not_in_production(self):
        """Test that django-model-info is only enabled in DEBUG mode"""
        if not settings.DEBUG:
            self.assertNotIn("django_model_info.apps.DjangoModelInfoConfig", settings.INSTALLED_APPS)
