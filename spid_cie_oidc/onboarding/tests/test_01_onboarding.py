from django.test import TestCase, Client
from django.urls import reverse
import json

from spid_cie_oidc.entity.jwks import serialize_rsa_key
from spid_cie_oidc.entity.jwks import new_rsa_key


class OnboardingTest(TestCase):

    def setUp(self):
        self.data = {"organization_name" : "","url_entity" : "",
            "authn_buttons_page_url" : "","public_jwks" : ""
        }

    def test_onboarding_registration(self):
        url = reverse("oidc_onboarding_registration")
        c = Client()
        res = c.get(url, self.data)
        self.assertEqual(res.status_code, 200)
        res = c.post(url, self.data)
        self.assertFormError(res, 'form', 'organization_name', 'Enter your organization name')
        self.assertFormError(res, 'form', 'url_entity', 'Enter your url of the entity')
        self.assertFormError(res, 'form', 'authn_buttons_page_url', 'Enter the url of the page where the SPID/CIE button is available')
        self.assertFormError(res, 'form', 'public_jwks', 'Enter the public jwks of the entities')
        self.assertEqual(res.status_code, 200)
        self.data["organization_name"] = "test name"
        self.data["url_entity"] = "https://test.it"
        self.data["authn_buttons_page_url"] = "https://authnurl.com"
        self.data["public_jwks"] = {"key":"ciao"}
        res = c.post(url, self.data)
        self.assertContains(res, "Inserisci un JSON valido.")
        self.assertEqual(res.status_code, 200)
        jwk = serialize_rsa_key(new_rsa_key().pub_key)
        self.data["public_jwks"] = json.dumps(jwk)
        res = c.post(url, self.data)
        self.assertEqual(res.status_code, 302)
        res = c.get(res.url)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.data["organization_name"], res.content.decode())
        self.assertIn("aquired", res.content.decode())
    
        