import io

from django.conf import settings
from django.core.management import call_command, get_commands
from django.test import TestCase, override_settings
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

    def test_django_model_info_app_config(self):
        """Test django-model-info app configuration"""
        app_config = "django_model_info.apps.DjangoModelInfoConfig"
        
        # This test will pass in both DEBUG and non-DEBUG modes
        # by testing the logical relationship rather than absolute presence
        debug_mode = settings.DEBUG
        app_installed = app_config in settings.INSTALLED_APPS
        
        # The app should be installed if and only if DEBUG is True
        self.assertEqual(debug_mode, app_installed,
                        f"django-model-info should be {'installed' if debug_mode else 'not installed'} "
                        f"when DEBUG={debug_mode}")

    def test_management_commands_availability(self):
        """Test management commands are available when appropriate"""
        commands = get_commands()
        expected_commands = ["modelinfo", "modelfilters", "modelgraph", "migrationgraph"]
        
        # Count how many expected commands are available
        available_commands = [cmd for cmd in expected_commands if cmd in commands]
        
        # Verify commands are available when DEBUG is True, unavailable when False
        debug_mode = settings.DEBUG
        if debug_mode:
            self.assertEqual(len(available_commands), len(expected_commands),
                           f"All {len(expected_commands)} django-model-info commands should be available in DEBUG mode")
        else:
            self.assertEqual(len(available_commands), 0,
                           "No django-model-info commands should be available in production mode")

    def test_modelinfo_command_when_available(self):
        """Test modelinfo command functionality when it should be available"""
        commands = get_commands()
        
        if "modelinfo" in commands:
            # Command is available, test it works
            stdout = io.StringIO()
            call_command("modelinfo", "--help", stdout=stdout)
            help_output = stdout.getvalue()
            self.assertIn("fields and methods for each model", help_output)
        else:
            # Command not available, verify this matches our expectation
            self.assertFalse(settings.DEBUG, "modelinfo should only be unavailable when DEBUG=False")

    def test_modelfilters_command_when_available(self):
        """Test modelfilters command functionality when it should be available"""
        commands = get_commands()
        
        if "modelfilters" in commands:
            # Command is available, test it works
            stdout = io.StringIO()
            call_command("modelfilters", "--help", stdout=stdout)
            help_output = stdout.getvalue()
            self.assertIn("Show the available filters for model", help_output)
        else:
            # Command not available, verify this matches our expectation
            self.assertFalse(settings.DEBUG, "modelfilters should only be unavailable when DEBUG=False")

    def test_modelgraph_command_when_available(self):
        """Test modelgraph command functionality when it should be available"""
        commands = get_commands()
        
        if "modelgraph" in commands:
            # Command is available, test it works
            stdout = io.StringIO()
            call_command("modelgraph", "--help", stdout=stdout)
            help_output = stdout.getvalue()
            self.assertIn("Create a graph of models", help_output)
        else:
            # Command not available, verify this matches our expectation
            self.assertFalse(settings.DEBUG, "modelgraph should only be unavailable when DEBUG=False")

    def test_migrationgraph_command_when_available(self):
        """Test migrationgraph command functionality when it should be available"""
        commands = get_commands()
        
        if "migrationgraph" in commands:
            # Command is available, test it works
            stdout = io.StringIO()
            call_command("migrationgraph", "--help", stdout=stdout)
            help_output = stdout.getvalue()
            self.assertIn("Create a graph of migration", help_output)
        else:
            # Command not available, verify this matches our expectation
            self.assertFalse(settings.DEBUG, "migrationgraph should only be unavailable when DEBUG=False")
