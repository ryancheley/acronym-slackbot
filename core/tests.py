from django.conf import settings
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
