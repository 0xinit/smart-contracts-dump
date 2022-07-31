from lib2to3.pgen2.literals import simple_escapes
from brownie import SimpleStorage, accounts, config


def read_contract():
    # basically the SimpleStorage contract is just an array, so interacting with it is easy.
    # print(SimpleStorage[0])
    # simple_storage = SimpleStorage[0]
    # -1 if we want the most recent deployment
    simple_storage = SimpleStorage[-1]
    # ABI and Address are already in brownie
    print(simple_storage.retrieve())


def main():
    read_contract()
