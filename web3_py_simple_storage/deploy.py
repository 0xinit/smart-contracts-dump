import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# these are for to connect to rinkeby testchain usually from infura.io
# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4
#
# For connecting to ganache
# these datas are from ganache-cli -d
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# use export PRIVATE_KEY=whatever your private key is
# this is just ganache private key so it doesn't matter
# to access env vairable just use privatekey = os.getenv("PRIVATE_KEY")
# privatekey = os.getenv("PRIVATE_KEY")
private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
# to work with contract we need 2 things:
# 1. contract address
# 2. contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# your can interact with contract in two different ways:
# 1. call-> Simulate making the call and getting a return value (calls dont make a state change) (blue buttons on remix generally speaking)
# 2. transact-> Actually make a state change (in remix, it's the orange buttons) (usually when we build the txn and send the txn)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

# creating the txn
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        # nonce + 1 because we already used nonce = 0 above while making and deploying the contract
        "nonce": nonce + 1,
    }
)

# signing the txn
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

# sending the txn
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")

# getting the txn receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
