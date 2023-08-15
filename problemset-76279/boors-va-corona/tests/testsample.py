from django.contrib.admin.sites import AdminSite

from rest_framework.test import APITestCase

from apps.guard.models import SecurityConfig, ViewDetail


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


class TestSamples(APITestCase):

    def setUp(self) -> None:
        self.request = MockRequest()
        self.request.user = MockSuperUser()

    def test_security_config_admin_add_permission(self):
        try:
            from apps.guard.admin import SecurityConfigAdmin
        except ImportError as e:
            self.fail(e)
        admin = SecurityConfigAdmin(SecurityConfig, AdminSite)

        self.assertFalse(admin.has_add_permission(self.request))

    def test_view_detail_admin_delete_permission(self):
        try:
            from apps.guard.admin import ViewDetailAdmin
        except ImportError as e:
            self.fail(e)
        admin = ViewDetailAdmin(ViewDetail, AdminSite)

        self.assertFalse(admin.has_delete_permission(self.request))
