import pytest
from brownie import accounts, config, Contract
from eth_account import Account
from eth_account.messages import encode_structured_data


@pytest.fixture
def gov(accounts):
    yield accounts[0]


@pytest.fixture
def affiliate(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[2]


@pytest.fixture
def rewards(accounts):
    yield accounts[3]


@pytest.fixture
def rando(accounts):
    yield accounts[3]


@pytest.fixture
def token(pm, gov):
    Token = pm(config["dependencies"][0]).Token
    yield gov.deploy(Token, 18)


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


@pytest.fixture
def vault(create_vault, token):
    yield create_vault(token=token)


@pytest.fixture
def create_vault(pm, gov, rewards, guardian, management):
    def create_vault(token, releaseDelta=0, governance=gov):
        liveRegistry = Contract("0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804")
        Vault = pm(config["dependencies"][0]).Vault

        tx = liveRegistry.newExperimentalVault(
            token,
            governance,
            guardian,
            rewards,
            "vault",
            "token",
            releaseDelta,
            {"from": governance},
        )
        vault = Vault.at(tx.return_value)

        vault.setDepositLimit(2 ** 256 - 1, {"from": governance})
        return vault

    yield create_vault


@pytest.fixture
def registry(pm, gov):
    Registry = pm(config["dependencies"][0]).Registry
    yield gov.deploy(Registry)


@pytest.fixture
def new_registry(pm, gov):
    Registry = pm(config["dependencies"][0]).Registry
    yield gov.deploy(Registry)


@pytest.fixture
def sign_token_permit():
    def sign_token_permit(
        token,
        owner: Account,  # NOTE: Must be a eth_key account, not Brownie
        spender: str,
        allowance: int = 2 ** 256 - 1,  # Allowance to set with `permit`
        deadline: int = 0,  # 0 means no time limit
        override_nonce: int = None,
    ):
        chain_id = 1  # ganache bug https://github.com/trufflesuite/ganache/issues/1643
        if override_nonce:
            nonce = override_nonce
        else:
            nonce = token.nonces(owner.address)
        data = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                "Permit": [
                    {"name": "owner", "type": "address"},
                    {"name": "spender", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "nonce", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"},
                ],
            },
            "domain": {
                "name": token.name(),
                "version": "1",
                "chainId": chain_id,
                "verifyingContract": str(token),
            },
            "primaryType": "Permit",
            "message": {
                "owner": owner.address,
                "spender": spender,
                "value": allowance,
                "nonce": nonce,
                "deadline": deadline,
            },
        }
        permit = encode_structured_data(data)
        return owner.sign_message(permit)

    return sign_token_permit
