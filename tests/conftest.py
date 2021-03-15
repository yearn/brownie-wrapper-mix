from pathlib import Path

import pytest



@pytest.fixture
def affiliate(management):
    yield management  # NOTE: Not necessary for these tests


@pytest.fixture
def affiliate_token(token, affiliate, registry, AffiliateToken):
    # Affliate Wrapper
    yield affiliate.deploy(
        AffiliateToken,
        token,
        registry,
        f"Affiliate {token.symbol()}",
        f"af{token.symbol()}",
    )
