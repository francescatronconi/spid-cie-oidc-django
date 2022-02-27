# Openid Connect Relying Party Relying Party

A SPID/CIE implementation of a OpenID Connect Relying Party fully compliant to
AgID SPID guidelines and CIE id guidelines.

To date there are many libraries that enable OAuth2 and OIDC in a Django project,
this project instead born to be lightweight and simple.

What is available today represents the bare essentials to manage an authorization flow and requests
for token acquisition and user information, processing of attributes and identity reunification functions.

## Features

Regarding OAuth2

 - Authorization Code Grant: [rfc6749](https://tools.ietf.org/html/rfc6749#section-4.1)
 - PKCE: [rfc7636](https://tools.ietf.org/html/rfc7636)

Regarding OIDC

 - CodeFlowAuth: [openid-connect-core-1_0](https://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth)
 - OIDC Federation 1.0: [openid-connect-federation-1_0](https://openid.net/specs/openid-connect-federation-1_0.html)
 - UserInfo endpoint: [UserInfo](https://openid.net/specs/openid-connect-core-1_0.html#UserInfo)

TODO:
 - Token Revocation / RP Initiated logout: [openid-connect-rpinitiated-1_0](https://openid.net/specs/openid-connect-rpinitiated-1_0.html)

Regarding django user management

 - user attributes processing and rewriting from OAuth2 claims
 - reunification of digital identities

## General Settings Paramenters

- `OIDCFED_FEDERATION_TRUST_ANCHOR` defines the default Trust Anchor.
- `OIDCFED_FEDERATION_TRUST_ANCHORS` defines the allowed Trust Anchors. 
- `OIDCFED_IDENTITY_PROVIDERS` defines the list of OPs to enable in Trust Chain operations.

Example
````
OIDCFED_IDENTITY_PROVIDERS = [
    "http://127.0.0.1:8000/oidc/op/",
    "http://127.0.0.1:8002/"
]
````

Please see `example/example/spid_oidc_rp_settings.py` as example.

- `RP_PREFS`: General informations, default parameters during authentication requests, like the `scope` attribute
- `RP_ATTR_MAP`: defines how oidc claims should be mapped to User model. You can even use a function to do rewrite or create new attributes (feel free to contribute with new processors in `processors.py`)
    ````
    (
     {
        'func': 'spid_oidc_rp.processors.issuer_prefixed_sub',
        'kwargs': {'sep': '__'}
     },
    )
    ````
    Otherwise a simple mapping like this: `('firstname',),`
    Otherwise a multiple OR sequence: `('firstname', 'lastname'),`. This will check for the first occourrence
- `RP_PKCE_CONF`: function and general paramenters for PKCE creation

TODO:
- `user_lookup_field`: the django user field, where the reunification lookup happens, eg: `('username'),`
- `user_create`: creates a new user if the reunification lookup fails


## OIDC Federation CLI

`fetch_openid_providers` build the Trust Chains for each `OIDCFED_IDENTITY_PROVIDERS`. 
````
examples/federation_authority/manage.py fetch_openid_providers --start -f

````

## Usage

Open your web browser and go to your debug server url, eg:

`http://localhost:8001/oidc/rp/begin?provider=http://127.0.0.1:8000/oidc/op/`

where `provider` is one of SPID/CIE OIDC providers.
Remember that you need a preexisting and valid Trust Chain, related
to that provider, before create an authorization request to it.

## Endpoints

### entity configuration (.well-known/openid-federation)

As inherited from [__spid_cie_oidc.entity__](docs/tecnhical_specifications/ENTITY.md).

### authorization

This endpoint is the starting point for OIDC SPID/CIE authentication.

the webpath is customizable in the `urls.py` file and by default it's
configured [here](https://github.com/peppelinux/spid-cie-oidc-django/blob/main/spid_cie_oidc/relying_party/urls.py#L13) 
and correspond to `spid_cie_oidc.relying_party.views.SpidCieOidcRpBeginView`.

The request is of type GET and supports the following parameters:

- __provider__, REQUIRED. To be enhanced with an http url corresponding to a subject id of a SPID/CIE OIDC Provider.
- __redirect_uri__, OPTIONAL. Selects one of the redirect_uri available in RP's metadata.
- __scope__, OPTIONAL. Selects one or more of the scopes, default is `openid`.
- __consent__, OPTIONAL. Sets SPID or CIE extended consent values.
- __trust_anchor__, OPTIONAL. Sets the Trust Anchor to resolve the Federation. Default is `settings.OIDCFED_FEDERATION_TRUST_ANCHOR`

### auth code redirect

WiP

### logout

WiP

## SPID/CIE QAD and compliances tests

WiP
