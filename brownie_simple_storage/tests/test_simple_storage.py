from lib2to3.pgen2.literals import simple_escapes
from brownie import SimpleStorage, accounts


def test_deploy():
    # testing is divided basically into 3 categories.
    # 1. Arranging
    account = accounts[0]
    # 2. Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # 3. Assert
    assert starting_value == expected


def test_updating_storage():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    expected = 15
    simple_storage.store(expected, {"from": account})

    assert expected == simple_storage.retrieve()
