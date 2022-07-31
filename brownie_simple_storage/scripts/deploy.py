from brownie import accounts, config, SimpleStorage, network

import os

# importing a contract in brownie is easier than manual method. In manual method, you need to open it with "with open" and read everything
# in brownie just use from brownie import "contract name" and then deploy().


def deploy_simple_storage():
    # gets the first address from ganache-cli since accounts is just an array
    account = get_account()
    print(account)
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)
    # retrieve() is a view function
    stored_value = simple_storage.retrieve()
    # whenever we are doing a transaction from someone we need to specify the account, who we are doing it from.
    transaction = simple_storage.store(15, {"from": account})
    # how many blocks we wanna wait
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)

    # using brownie
    # account = accounts.load("test1")
    # print(account)

    # env variables and brownie config
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # print(account)
    # or
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
