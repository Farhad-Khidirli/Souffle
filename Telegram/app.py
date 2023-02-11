import json
from web3 import Web3

# Connect to the Ethereum network
w3 = Web3(Web3.HTTPProvider("http://localhost:7545"))


# Validate provided address
def validate_address(_address):
    if _address not in w3.eth.accounts:
        raise Exception(f"Address {_address} not found in the list of accounts")


def get_balance(_address):
    balance = w3.fromWei(w3.eth.getBalance(_address), "ether")
    return balance


def to_ether(_amount):
    return Web3.toWei(_amount, 'ether')


# The address of the account that will send the Ethereum
sender_address = Web3.toChecksumAddress(input("Enter the sender's address: "))
validate_address(sender_address)
w3.eth.defaultAccount = sender_address

# The private key of the sender account
private_key = input("Enter the sender's private key: ")

# The address of the account that will receive the Ethereum
receiver_address = Web3.toChecksumAddress(input("Enter the receiver's address: "))
validate_address(receiver_address)

# The amount of Ethereum to send
amount = to_ether(int(input("Enter the amount of ether to send: ")))

# The nonce (number of transactions sent by an account)
nonce = w3.eth.getTransactionCount(sender_address)

# The transaction parameters
transaction = {
    'to': receiver_address,
    'value': amount,
    'gas': 21000,
    'gasPrice': w3.eth.gasPrice,
    'nonce': nonce,
    'chainId': w3.eth.chainId
}

# Sign the transaction with the private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# Broadcast the transaction to the network
w3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Get the transaction hash
tx_hash = Web3.toHex(signed_txn.hash)
print(f'Transaction hash: {tx_hash}')

# Read the data from the Greeter contract's JSON file
with open('../build/contracts/SendEther.json', "r") as file:
    data = json.load(file)

# Extract the ABI, bytecode, and contract address from the JSON file
abi = data["abi"]
bytecode = data["bytecode"]

# Create a contract object from the ABI and bytecode
SendEther = w3.eth.contract(abi=abi, bytecode=bytecode)

# Deploy the contract to the Ethereum network
tx_hash = SendEther.constructor().transact()

# Wait for the transaction to be processed and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

contract = w3.eth.contract(abi=abi, address=tx_receipt.contractAddress)

print(get_balance(w3.eth.accounts[0]))
