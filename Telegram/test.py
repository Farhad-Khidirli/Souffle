from web3 import Web3
import json

# Connect to local blockchain (e.g. Ganache)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Set the address of the sender
sender_address = input("Enter sender's public address: ")
sender_private_key = input("Enter sender's private key: ")
sender = web3.eth.account.privateKeyToAccount(sender_private_key)
web3.eth.default_account = sender.address

# Get the address of the receiver and the amount to transfer
receiver_address = input("Enter receiver's public address: ")
amount = input("Enter the amount to transfer: ")

# Create an instance of the contract and call the transfer function
contract_address = input("Enter the address of the Transfer contract: ")

# Read the data from the Greeter contract's JSON file
with open('../build/contracts/Transfer.json', "r") as file:
    data = json.load(file)

# Extract the ABI, bytecode, and contract address from the JSON file
abi = data["abi"]
bytecode = data["bytecode"]

amount_wei = Web3.toWei(amount, 'ether')

contract = web3.eth.contract(address=contract_address, abi=abi)
tx_hash = contract.functions.transfer(receiver_address, amount_wei).transact()

# Wait for the transaction to be mined
web3.eth.waitForTransactionReceipt(tx_hash)
print("Transaction complete!")
