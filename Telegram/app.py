import json
from web3 import Web3

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))


# Validate provided address
def validate_address(_address):
    if _address not in w3.eth.accounts:
        raise Exception(f"Address {_address} not found in the list of accounts")


def get_balance(_address):
    balance = w3.fromWei(w3.eth.getBalance(_address), "ether")
    return balance


def to_ether(_amount):
    return Web3.toWei(_amount, 'ether')


# Read the data from the EtherTransfer contract's JSON file
with open('../build/contracts/Transfer.json', "r") as file:
    data = json.load(file)

# Extract the ABI, bytecode, and contract address from the JSON file
abi = data["abi"]
bytecode = data["bytecode"]

# The address of the account that will send the Ethereum
sender_address = Web3.toChecksumAddress(input("Enter the sender's address: "))
validate_address(sender_address)
w3.eth.defaultAccount = sender_address

private_key = input("Enter the sender's private key: ")

contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Get the contract address
contract_address = tx_receipt.contractAddress
print(f"Contract address: {contract_address}")

# Create a contract instance
my_contract = w3.eth.contract(address=contract_address, abi=abi)

receiver_address = Web3.toChecksumAddress(input("Enter the receiver's address: "))
validate_address(receiver_address)

amount = to_ether(int(input("Enter the amount of ether to send: ")))

tx_hash = my_contract.functions.transfer(receiver_address).transact({'from': sender_address, 'value': amount})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Check the transaction status
if tx_receipt.status == 1:
    print("Transaction successful!")
    logs = my_contract.events.ETransfer().processReceipt(tx_receipt)
    if len(logs) > 0:
        print(f"Transfer event emitted: {logs[0]['args']}")
    else:
        print("No transfer event emitted")
else:
    print("Transaction failed with error:", tx_receipt['status'])
