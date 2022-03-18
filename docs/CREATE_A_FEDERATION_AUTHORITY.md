## Tutorial

We can create our entity though the Admin backend or via API.

### Create a Federation Authority via web

__setup__
1. add `spid_cie_oidc.entity` and `spid_cie_oidc.authority` in settings.INSTALLED_APPS
2. do migrations `./manage.py migrate`
3. create superuser `./manage.py createsuperuser`
4. log in the `/admin` interface

__configure the federation entity__
1. Click on _Federation Entity Configuration_ and create your entity see `federation_authority` example


### Create a Federation Descendant via web

__configure descendants entities__
1. Click on _Federation Entity Descendant_ and configure a descendant
2. Click on _Federation Entity Profile_ and create the desidered profiles and trust marks template
3. Click on _Federation Entity Descendant Assigned Profile_ and assing at least a profile to the new descendant


![profile](images/profiles.png)
A profile that may be assigned to a Relying Party.


![profile](images/assigned_profile.png)
An assigned profile to a Relying Party.


### Create a Federation Authority via API

The JWKS if not submitted will be created automatically.

````
from spid_cie_oidc.entity.models import *

TA_SUB = "http://testserver/"
FA_METADATA = {
    "federation_entity": {
        "contacts": ["ops@localhost"],
        "federation_fetch_endpoint": f"{TA_SUB}/fetch",
        "homepage_uri": f"{TA_SUB}",
        "name": "example TA",
    }
}
TM_ISSUERS = {
    "https://www.spid.gov.it/certification/rp/public": [
        TA_SUB,
        "https://public.intermediary.spid.it",
    ],
    "https://www.spid.gov.it/certification/rp/private": [
        TA_SUB,
        "https://private.other.intermediary.it",
    ],
    "https://sgd.aa.it/onboarding": ["https://sgd.aa.it"],
}
FA_CONSTRAINTS = {"max_path_length": 1}

ta_conf_data = dict(
    sub=TA_SUB,
    metadata=FA_METADATA,
    constraints=FA_CONSTRAINTS,
    is_active=1,
    trust_marks_issuers=TM_ISSUERS,
)

FederationEntityConfiguration.objects.create(**ta_conf_data)
````

Using different kind of metadata we can create OpenID Relying Parties or Providers.
Just rememeber, for these latter, to add also the authority_hints value as follow

````
authority_hints = ["http://testserver/"]
````

### Create a Federation Descendant via API

see [unit tests](https://github.com/peppelinux/spid-cie-oidc-django/blob/main/spid_cie_oidc/authority/tests/test_02_trust_anchor_intermediary.py#L32).


### Create a provider in a Federation Authority

In provider configure settingslocal.py, for all provider configuration parameters see [here](https://github.com/francescatronconi/spid-cie-oidc-django/blob/newbranch/docs/technical_specifications/PROVIDER.md) 


To create a CIE or Spid provider configure `OIDCFED_PROVIDER_PROFILE` parameter in settingslocal.py as "cie" or "spid"

In exemples/provider configure a federation entity configuration as OP:

````
./manage.py runserver 0.0.0.0:8002
````
In provider admin console (http://127.0.0.1:8002/admin) the following data are required:

- sub (eg. 'http://127.0.0.1:8002/oidc/op/')
- authority hints, list of trust anchor(eg. ["http://127.0.0.1:8000/"])
- Jwks, private jwks, an example [here](https://github.com/italia/spid-cie-oidc-django/blob/dev/spid_cie_oidc/provider/tests/settings.py#L1)
- metadata, url paths in metadata need to be mapped in examples/relying_party/urls.py, [here](https://github.com/italia/spid-cie-oidc-django/blob/dev/examples/provider/provider/urls.py#L48).
An example of metadata[here]https://github.com/italia/spid-cie-oidc-django/blob/dev/spid_cie_oidc/provider/tests/settings.py#L20)

![OP federation entity](images/op_federation_entity.png)

In examples/federation_authority configure OP cie as descendant and assign it a profile::

````
./manage.py runserver
````

In federation admin console (http://127.0.0.1:8000/admin) the following data are required:

- OP name
- sub (eg. 'http://127.0.0.1:80012/oidc/rp/')
- Jwks, public jwks, an example [here](https://github.com/italia/spid-cie-oidc-django/blob/dev/spid_cie_oidc/provider/tests/settings.py#L58)

![OP as descendant](images/op_descendant.png)

Then assign a profile:

as profile select 'Identity Provider'

![OP assigned profile](images/op_assigned_profile.png)

In federation service build trust chain for OP:

````
examples/federation_authority/manage.py fetch_openid_providers --start -f
````

### Create a Relying Party in a Federation Authority

Do migrate:
 ````examples/relying_party/manage.py migrate````

In relying_party configure settingslocal.py, for more information on configuration parameters see [here](https://github.com/italia/spid-cie-oidc-django/blob/dev/docs/technical_specifications/RELYING_PARTY.md) 

In examples/relying_party configure a federation entity configuration as RP:

````
./manage.py runserver 0.0.0.0:8001
````
In relying_party admin console (http://127.0.0.1:8001/admin) the following data are required:

- sub (eg. 'http://127.0.0.1:8001/oidc/rp/')
- authority hints, list of trust anchor(eg. ["http://127.0.0.1:8000/"])
- Jwks, private jwks, an example [here](https://github.com/italia/spid-cie-oidc-django/blob/dev/spid_cie_oidc/authority/tests/settings.py#L7)
- metadata, url paths in metadata need to be mapped in examples/relying_party/urls.py, [here](https://github.com/italia/spid-cie-oidc-django/blob/dev/examples/relying_party/relying_party/urls.py#L42).
An example of metadata[here](https://github.com/italia/spid-cie-oidc-django/blob/dev/spid_cie_oidc/authority/tests/settings.py#L91)

![RP federation entity](images/rp_federation_entity.png)


In examples/federation_authority configure RP as descendant and assign it a profile:

````
./manage.py runserver
````

In federation admin console (http://127.0.0.1:8000/admin) the following data are required:

- RP name
- sub (eg. 'http://127.0.0.1:8001/oidc/rp/')
- Jwks, public jwks, an example [here](https://github.com/italia/spid-cie-oidc-django/blob/dev/spid_cie_oidc/authority/tests/settings.py#L8)

![RP as descendant](images/rp_descendant.png)

Then assign a profile:

as profile select 'SPID Private SP'

![RP assigned profile](images/rp_assigned_profile.png)


In relying_party service build trust chain for OP:

by parameter `OIDCFED_IDENTITY_PROVIDERS` in settingslocal.py define the list of OPs to enable in Trust Chain operations
````
examples/relaying_party/manage.py fetch_openid_providers --start -f
````

Connect to the login page specified in settingslocal.py by 'LOGIN_URL' parameter (eg. 'http://127.0.0.1:8000/oidc/rp/landing' where 'LOGIN_URL=/oidc/rp/landing') and start authentication.