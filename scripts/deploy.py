  
from pathlib import Path

from brownie import AffiliateToken, Contract, accounts, config, network, project, web3
from eth_utils import is_checksum_address

# For later use
import click

def main():
    token = "xxxxx"
    registry = get_address("Registry address,", "v2.registry.ychad.eth")
    tokenName = "abcxyz"
    tokenSymbol = "xxx"
    
    affiliatetoken = AffiliateToken.deploy(token, registry, tokenName, tokenSymbol, {"from": accounts[0]})
