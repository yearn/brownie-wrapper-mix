import brownie
import pytest

from eth_account import Account

AMOUNT = 100


def test_config_live(gov, live_token, live_vault, live_registry, live_affiliate_token):
    assert live_affiliate_token.token() == live_token
    assert live_affiliate_token.name() == "Affiliate " + live_token.symbol()
    assert live_affiliate_token.symbol() == "af" + live_token.symbol()
    assert (
        live_affiliate_token.decimals()
        == live_vault.decimals()
        == live_token.decimals()
    )
    assert live_registry.numVaults(live_token) > 0
    assert live_affiliate_token.bestVault() == live_vault
    assert live_affiliate_token.allVaults() == [live_vault]


def test_setAffiliate_live(affiliate, live_affiliate_token, rando):
    new_affiliate = rando
    # No one can set affiliate but affiliate
    with brownie.reverts():
        live_affiliate_token.setAffiliate(new_affiliate, {"from": new_affiliate})
    # Affiliate doesn't change until it's accepted
    live_affiliate_token.setAffiliate(new_affiliate, {"from": affiliate})
    assert live_affiliate_token.affiliate() == affiliate
    # Only new affiliate can accept a change of affiliate
    with brownie.reverts():
        live_affiliate_token.acceptAffiliate({"from": affiliate})
    # Affiliate doesn't change until it's accepted
    live_affiliate_token.acceptAffiliate({"from": new_affiliate})
    assert live_affiliate_token.affiliate() == new_affiliate
    # No one can set affiliate but affiliate
    with brownie.reverts():
        live_affiliate_token.setAffiliate(new_affiliate, {"from": affiliate})
    # Only new affiliate can accept a change of affiliate
    with brownie.reverts():
        live_affiliate_token.acceptAffiliate({"from": affiliate})


def test_setRegistry_live(
    rando, affiliate, live_gov, live_affiliate_token, new_registry, gov
):
    with brownie.reverts():
        live_affiliate_token.setRegistry(rando, {"from": rando})

    with brownie.reverts():
        live_affiliate_token.setRegistry(rando, {"from": affiliate})
    # Cannot set to an invalid registry
    with brownie.reverts():
        live_affiliate_token.setRegistry(rando, {"from": live_gov})

    # yGov must be the gov on the new registry too
    new_registry.setGovernance(rando, {"from": gov})
    new_registry.acceptGovernance({"from": rando})
    with brownie.reverts():
        live_affiliate_token.setRegistry(new_registry, {"from": live_gov})
    new_registry.setGovernance(live_gov, {"from": rando})
    new_registry.acceptGovernance({"from": live_gov})

    live_affiliate_token.setRegistry(new_registry, {"from": live_gov})


def test_deposit_live(live_token, live_vault, live_affiliate_token, live_whale, rando):
    live_token.transfer(rando, 10000, {"from": live_whale})
    assert live_affiliate_token.balanceOf(rando) == live_vault.balanceOf(rando) == 0

    # NOTE: Must approve affiliate_token to deposit
    live_token.approve(live_affiliate_token, 10000, {"from": rando})
    live_affiliate_token.deposit(10000, {"from": rando})
    assert live_affiliate_token.balanceOf(rando) == 10000
    assert live_vault.balanceOf(rando) == 0


def test_deposit_max_live(
    live_token, live_vault, live_affiliate_token, live_whale, rando
):
    live_token.transfer(rando, 10000, {"from": live_whale})
    assert live_affiliate_token.balanceOf(rando) == live_vault.balanceOf(rando) == 0

    # NOTE: Must approve affiliate_token to deposit
    live_token.approve(live_affiliate_token, 10000, {"from": rando})
    live_affiliate_token.deposit({"from": rando})
    assert live_affiliate_token.balanceOf(rando) == 10000
    assert live_vault.balanceOf(rando) == 0
    assert live_affiliate_token.totalSupply() == 10000


# NOTE: This test will fail.
# NOTE: Because the live vault is already using the most recent apiVersion, we cannot deploy and endorse a new vault for this token
"""  
def test_migrate_live(live_token, live_registry, create_vault, live_affiliate_token, gov, live_gov, live_whale, rando, affiliate):
    vault1 = create_vault(releaseDelta=3, token=live_token)
    vault1.setGovernance(live_gov, {"from": gov})
    vault1.acceptGovernance({"from": live_gov})
    live_registry.newRelease(vault1, {"from": live_gov})
    live_registry.endorseVault(vault1, {"from": live_gov})
    live_token.transfer(rando, 10000, {"from": live_whale})
    live_token.approve(live_affiliate_token, 10000, {"from": rando})
    live_affiliate_token.deposit(10000, {"from": rando})
    assert live_affiliate_token.balanceOf(rando) == 10000
    assert vault1.balanceOf(live_affiliate_token) == 10000

    vault2 = create_vault(releaseDelta=0, token=live_token)
    live_registry.newRelease(vault2, {"from": live_gov})
    live_registry.endorseVault(vault2, {"from": live_gov})

    with brownie.reverts():
        live_affiliate_token.migrate({"from": rando})

    # Only affiliate can call this method
    live_affiliate_token.migrate({"from": affiliate})
    assert live_affiliate_token.balanceOf(rando) == 10000
    assert vault1.balanceOf(live_affiliate_token) == 0
    assert vault2.balanceOf(live_affiliate_token) == 10000
"""


def test_transfer_live(live_token, live_affiliate_token, live_whale, rando, affiliate):
    # NOTE: Reset balance to 0
    preTestBal = live_token.balanceOf(rando)
    if preTestBal > 0:
        live_token.transfer(live_whale, preTestBal, {"from": rando})

    live_token.transfer(rando, 10000, {"from": live_whale})
    live_token.approve(live_affiliate_token, 10000, {"from": rando})
    live_affiliate_token.deposit(10000, {"from": rando})

    # NOTE: Just using `affiliate` as a random address
    live_affiliate_token.transfer(affiliate, 10000, {"from": rando})
    assert live_affiliate_token.balanceOf(rando) == 0
    assert live_affiliate_token.balanceOf(affiliate) == 10000
    assert live_token.balanceOf(rando) == live_token.balanceOf(affiliate) == 0


def test_withdraw_live(live_token, live_affiliate_token, live_whale, rando):
    # NOTE: Reset balance to 0
    preTestBal = live_token.balanceOf(rando)
    if preTestBal > 0:
        live_token.transfer(live_whale, preTestBal, {"from": rando})

    live_token.transfer(rando, 10000, {"from": live_whale})
    live_token.approve(live_affiliate_token, 10000, {"from": rando})
    live_affiliate_token.deposit(10000, {"from": rando})

    # NOTE: Must approve affiliate_token to withdraw
    live_affiliate_token.withdraw(10000, {"from": rando})
    assert live_affiliate_token.balanceOf(rando) == 0
    # NOTE: Potential for tiny dust loss
    assert 10000 - 10 <= live_token.balanceOf(rando) <= 10000


def test_permit_live(chain, rando, live_affiliate_token, sign_token_permit):
    owner = Account.create()
    deadline = chain[-1].timestamp + 3600
    signature = sign_token_permit(
        live_affiliate_token, owner, str(rando), allowance=AMOUNT, deadline=deadline
    )
    assert live_affiliate_token.allowance(owner.address, rando) == 0
    live_affiliate_token.permit(
        owner.address,
        rando,
        AMOUNT,
        deadline,
        signature.v,
        signature.r,
        signature.s,
        {"from": rando},
    )
    assert live_affiliate_token.allowance(owner.address, rando) == AMOUNT
