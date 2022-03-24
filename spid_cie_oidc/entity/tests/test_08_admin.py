
from django.test import TestCase

from spid_cie_oidc.entity.models import FetchedEntityStatement, TrustChain
from spid_cie_oidc.entity.admin import TrustChainAdmin
from spid_cie_oidc.entity.tests.settings import TA_SUB
from spid_cie_oidc.entity.utils import (
    datetime_from_timestamp, 
    exp_from_now,
    iat_now
)
from spid_cie_oidc.authority.tests.settings import RP_CONF_AS_JSON

class AdminTest(TestCase):

    def setUp(self):
        self.ta_fes = FetchedEntityStatement.objects.create(
            sub=TA_SUB,
            iss=TA_SUB,
            exp=datetime_from_timestamp(exp_from_now(33)),
            iat=datetime_from_timestamp(iat_now()),
        )

        self.sub_tc = TrustChain.objects.create(
            sub=RP_CONF_AS_JSON["sub"],
            exp=datetime_from_timestamp(exp_from_now(33)),
            metadata=RP_CONF_AS_JSON["metadata"],
            status="valid",
            trust_anchor=self.ta_fes,
            is_active=True,
        )
    def test_update_trust_chain(self):
        TrustChainAdmin.update_trust_chain({},[], queryset = [self.sub_tc])