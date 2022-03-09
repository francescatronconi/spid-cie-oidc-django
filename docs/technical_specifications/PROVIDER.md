# __Openid Connect Provider__ Identity Provider with additional test suite.

A SPID/CIE implementation of a OpenID Connect Provider fully compliant to
AgID SPID guidelines and CIE id guidelines.

## General settings

All the Provider settings paramenter are available at
[spid_cie_oidc.provider.settings](spie_cie_oidc/provider/settings.py) and
can be inherited in the general settings file of your project.


`OIDCFED_PROVIDER_PROFILES` supported profiles.
````
OIDCFED_PROVIDER_PROFILES = getattr(
    settings,
    'OIDCFED_PROVIDER_PROFILES',
    {
        "spid": {
            "authentication_request": AuthenticationRequestSpid,
        },
        "cie": {
            "authentication_request": AuthenticationRequestCie,
        }
    }
)
````

````
OIDCFED_DEFAULT_PROVIDER_PROFILE = getattr(
    settings,
    "OIDCFED_PROVIDER_PROFILE",
    "Spid"
)
````

## OIDC Federation CLI

`fetch_openid_relying_parties` build the Trust Chains for a relying party. 
````
examples/federation_authority/manage.py fetch_openid_relying_parties --start -f


## Endpoints

the webpath where the provider serve its features are the followings.

### entity configuration (.well-known/openid-federation)

As inherited from [__spid_cie_oidc.entity__](docs/tecnhical_specifications/ENTITY.md).

### authorization

This endpoint is the starting point for OIDC SPID/CIE authentication.
the webpath is customizable in the `urls.py` file and by default it's
configured [here](https://github.com/peppelinux/spid-cie-oidc-django/blob/main/spid_cie_oidc/provider/urls.py#L13) 
and correspond to `spid_cie_oidc.provider.views.AuthzRequestView`.

Provider accepts a GET request and submit to the final user a login form.

After login submit, provider accepts a POST request where a redirect is made to GET function of "oidc_provider_consent" url defined in [here](https://github.com/peppelinux/spid-cie-oidc-django/blob/main/spid_cie_oidc/provider/urls.py#L13) and corresponding to `spid_cie_oidc.provider.views.ConsentPageView`

After consent submitted, provider accept a POST request and at the end sends a response to "redirect_url" specify in the initial request with this parameters:

- __code__, REQUIRED. Authorization code that will be used later within the Token Endpoint to exchange it for the OIDC tokens
- __state__, REQUIRED. The state value enclosed in the authentication request
- __iss__, REQUIRED. The issuer identifier of the OP which created the Authentication Response



WiP

### token

WiP

### token introspection

WiP

### token revocation

WiP

### userinfo endpoint

WiP


## SPID/CIE QAD and compliances tests

WiP
