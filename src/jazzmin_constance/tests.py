from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ConstanceTemplateOverrideTests(TestCase):
    """The constance admin page must render through jazzmin_constance's template."""

    def setUp(self):
        user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.client.force_login(user)

    def test_constance_changelist_uses_jazzmin_constance_template(self):
        response = self.client.get(reverse("admin:constance_config_changelist"))

        self.assertEqual(response.status_code, 200)
        template_origins = [
            t.origin.name for t in response.templates if t.origin is not None
        ]
        self.assertTrue(
            any("jazzmin_constance" in origin and "admin/constance/change_list.html" in origin
                for origin in template_origins),
            f"constance change_list not served by jazzmin_constance: {template_origins}",
        )
        self.assertContains(response, 'id="jazzmin-constance"')

    def test_constance_changelist_renders_fieldsets_and_fields(self):
        response = self.client.get(reverse("admin:constance_config_changelist"))

        self.assertContains(response, "General")
        self.assertContains(response, "Feature Flags")
        self.assertContains(response, 'name="SITE_NAME"')
        self.assertContains(response, 'name="MAINTENANCE_MODE"')
        self.assertContains(response, 'name="MAX_UPLOAD_SIZE_MB"')

    def test_saving_the_form_updates_constance_values(self):
        from constance import config

        url = reverse("admin:constance_config_changelist")
        response = self.client.get(url)
        payload = {
            name: value
            for name, value in response.context["form"].initial.items()
        }
        payload.update({
            "MAINTENANCE_MODE": "on",
            "SITE_NAME": "Renamed Site",
            "MAX_UPLOAD_SIZE_MB": "25",
        })
        payload.pop("ALLOW_SIGNUPS", None)  # unchecked checkbox is omitted from POST
        payload.pop("FEATURE_NEW_DASHBOARD", None)
        payload["_save"] = "Save"

        response = self.client.post(url, payload)

        self.assertRedirects(response, url)
        self.assertTrue(config.MAINTENANCE_MODE)
        self.assertEqual(config.SITE_NAME, "Renamed Site")
        self.assertEqual(config.MAX_UPLOAD_SIZE_MB, 25)
        self.assertFalse(config.ALLOW_SIGNUPS)
