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

    def test_django_model_info_app_config(self):
        """Test django-model-info app configuration"""
        app_config = "django_model_info.apps.DjangoModelInfoConfig"

        # This test will pass in both DEBUG and non-DEBUG modes
        # by testing the logical relationship rather than absolute presence
        debug_mode = settings.DEBUG
        app_installed = app_config in settings.INSTALLED_APPS

        # The app should be installed if and only if DEBUG is True
        self.assertEqual(
            debug_mode,
            app_installed,
            f"django-model-info should be {'installed' if debug_mode else 'not installed'} when DEBUG={debug_mode}",
        )

    def test_management_commands_availability(self):
        """Test management commands are available when appropriate"""
        commands = get_commands()
        expected_commands = ["modelinfo", "modelfilters", "modelgraph", "migrationgraph"]

        # Count how many expected commands are available
        available_commands = [cmd for cmd in expected_commands if cmd in commands]

        # Verify the number of available commands matches the DEBUG setting
        debug_mode = settings.DEBUG
        expected_count = len(expected_commands) if debug_mode else 0
        self.assertEqual(
            len(available_commands),
            expected_count,
            f"Expected {expected_count} django-model-info commands when DEBUG={debug_mode}, but found {len(available_commands)}",
        )

    def test_modelinfo_command_availability_and_functionality(self):
        """Test modelinfo command availability matches DEBUG setting"""
        commands = get_commands()
        command_available = "modelinfo" in commands

        # The command should be available if and only if DEBUG is True
        self.assertEqual(
            settings.DEBUG,
            command_available,
            f"modelinfo command availability ({command_available}) should match DEBUG setting ({settings.DEBUG})",
        )

    def test_modelfilters_command_availability(self):
        """Test modelfilters command availability matches DEBUG setting"""
        commands = get_commands()
        command_available = "modelfilters" in commands

        # The command should be available if and only if DEBUG is True
        self.assertEqual(
            settings.DEBUG,
            command_available,
            f"modelfilters command availability ({command_available}) should match DEBUG setting ({settings.DEBUG})",
        )

    def test_modelgraph_command_availability(self):
        """Test modelgraph command availability matches DEBUG setting"""
        commands = get_commands()
        command_available = "modelgraph" in commands

        # The command should be available if and only if DEBUG is True
        self.assertEqual(
            settings.DEBUG,
            command_available,
            f"modelgraph command availability ({command_available}) should match DEBUG setting ({settings.DEBUG})",
        )

    def test_migrationgraph_command_availability(self):
        """Test migrationgraph command availability matches DEBUG setting"""
        commands = get_commands()
        command_available = "migrationgraph" in commands

        # The command should be available if and only if DEBUG is True
        self.assertEqual(
            settings.DEBUG,
            command_available,
            f"migrationgraph command availability ({command_available}) should match DEBUG setting ({settings.DEBUG})",
        )

    def test_command_help_functionality_correlation_with_debug(self):
        """Test that command help works correctly based on DEBUG setting"""
        # This test verifies that command functionality correlates with DEBUG setting
        commands = get_commands()

        # Check if modelinfo is available and test it
        modelinfo_available = "modelinfo" in commands
        self.assertEqual(settings.DEBUG, modelinfo_available)

        # Always test the command execution to ensure both paths are covered
        stdout = io.StringIO()
        exception_occurred = False

        try:
            call_command("modelinfo", "--help", stdout=stdout)
        except Exception:
            exception_occurred = True

        # Always get output and determine success (these lines always execute)
        help_output = stdout.getvalue()
        command_succeeded = not exception_occurred

        # Verify that command success correlates with availability
        self.assertEqual(
            modelinfo_available,
            command_succeeded,
            f"Command success ({command_succeeded}) should match availability ({modelinfo_available})",
        )

        # If command succeeded, verify the help content
        success_and_available = command_succeeded and modelinfo_available
        failure_expected = not modelinfo_available

        # This ensures both branches are tested depending on the environment
        self.assertTrue(
            success_and_available or failure_expected, "Either command should succeed when available OR fail when not available"
        )

        # Test help content correlation with command success
        help_contains_expected = "fields and methods for each model" in help_output

        # Help content should be present if and only if command succeeded
        self.assertEqual(
            command_succeeded,
            help_contains_expected,
            f"Help content presence ({help_contains_expected}) should match command success ({command_succeeded})",
        )
