from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-alchemy"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            # toWei will change 2000 * 1000000000000000000 to 2000 ether
            # toWei(2000, "ethers")
            DECIMALS,
            STARTING_PRICE,
            {"from": get_account()},
        )
    print("Mocks Deployed!")
