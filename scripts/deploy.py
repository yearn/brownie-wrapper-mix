  
from pathlib import Path

from brownie import AffiliateToken, Contract, accounts, config, network, project, web3
from eth_utils import is_checksum_address

# For later use
import click

def main():
    token = "xxxxx"
    registry = "0x3ee41c098f9666ed2ea246f4d2558010e59d63a0"
    tokenName = "abcxyz"
    tokenSymbol = "xxx"
    
    affiliatetoken = AffiliateToken.deploy(token, registry, tokenName, tokenSymbol, {"from": accounts[0]})
