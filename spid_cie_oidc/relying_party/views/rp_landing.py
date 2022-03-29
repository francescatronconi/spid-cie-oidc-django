import logging
import random
from copy import deepcopy
from django.conf import settings
from django.shortcuts import render
from spid_cie_oidc.entity.models import TrustChain

logger = logging.getLogger(__name__)


def oidc_rp_landing(request):
    spid_providers = {
        k: {"sub": v} for k, v in 
        settings.OIDCFED_IDENTITY_PROVIDERS.get("spid", {}).items()
    }
    cie_providers = {
        k: {"sub": v} for k, v in 
        settings.OIDCFED_IDENTITY_PROVIDERS.get("cie", {}).items()
    }
    
    tc_spid = TrustChain.objects.filter(
        sub__in = spid_providers.keys(),
        metadata__openid_provider__isnull=False,
        is_active=True
    )

    for i in tc_spid:
        spid_providers[i.sub] = {
            "sub": i.sub,
            "logo_uri" : i.metadata.get("openid_provider", {}).get("logo_uri", ""),
            "organization_name": i.metadata.get("openid_provider", {}).get("organization_name","")
        }

    tc_cie = TrustChain.objects.filter(
        sub__in = cie_providers.keys(),
        metadata__openid_provider__isnull=False,
        is_active=True
    )

    for i in tc_cie:
        cie_providers[i.sub] = {
            "sub": i.sub,
            "logo_uri" : i.metadata.get("openid_provider", {}).get("logo_uri", ""),
            "organization_name": i.metadata.get("openid_provider", {}).get("organization_name","")
        }

    s_spid_providers = list(spid_providers.items())
    random.shuffle(s_spid_providers)
    content = {
        "spid_providers": dict(s_spid_providers),
        "cie_providers" : cie_providers
    }
    return render(request, "rp_landing.html", content)
