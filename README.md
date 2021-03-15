# Yearn Affiliate Wrapper Brownie Mix

## What you'll find here

- Basic Solidity Smart Contract for creating your own Yearn Affiliate Wrapper ([`contracts/AffiliateToken.sol`](contracts/AffiliateToken.sol))

- Sample test suite that runs on mainnet fork. ([`tests/`](tests))

This mix is configured for use with [Ganache](https://github.com/trufflesuite/ganache-cli) on a [forked mainnet](https://eth-brownie.readthedocs.io/en/stable/network-management.html#using-a-forked-development-network).

## Installation and Setup

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html) & [Ganache-CLI](https://github.com/trufflesuite/ganache-cli), if you haven't already.

2. Sign up for [Infura](https://infura.io/) and generate an API key. Store it in the `WEB3_INFURA_PROJECT_ID` environment variable.

```bash
export WEB3_INFURA_PROJECT_ID=YourProjectID
```

3. Sign up for [Etherscan](www.etherscan.io) and generate an API key. This is required for fetching source codes of the mainnet contracts we will be interacting with. Store the API key in the `ETHERSCAN_TOKEN` environment variable.

```bash
export ETHERSCAN_TOKEN=YourApiToken
```

4. Download the mix.

```bash
brownie bake yearn-affiliate
```

## Known issues

### No access to archive state errors

If you are using Ganache to fork a network, then you may have issues with the blockchain archive state every 30 minutes. This is due to your node provider (i.e. Infura) only allowing free users access to 30 minutes of archive state. To solve this, upgrade to a paid plan, or simply restart your ganache instance and redploy your contracts.

# Resources

- Yearn [Discord channel](https://discord.com/invite/6PNv2nF/)
- Brownie [Gitter channel](https://gitter.im/eth-brownie/community)
