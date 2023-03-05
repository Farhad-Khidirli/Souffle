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


def check_transaction():
    if tx_receipt.status == 1:
        print("Transaction successful!")
        logs = my_contract.events.ETransfer().processReceipt(tx_receipt)
        if len(logs) > 0:
            print(f"Transfer event emitted: {logs[0]['args']}")
        else:
            print("No transfer event emitted")
    else:
        print("Transaction failed with error:", tx_receipt['status'])


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

chat_id = 1
public_address = sender_address
encrypted_private_key = private_key
phone_number = "123456"
email_address = "far@gmail.com"

tx_hash = my_contract.functions.registerUser2(
    chat_id, public_address, encrypted_private_key, phone_number, email_address
).transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
check_transaction()

chat_id = 2
public_address = "0xC93A80673EB401f363eA247875d0f45FAdB00A33"
encrypted_private_key = "31da11b1f176e5e78d21fb9f90c314ed30f89c604aa9f1c6a2122d6aee1cded1"
phone_number = "654321"
email_address = "lol@gmail.com"
tx_hash = my_contract.functions.registerUser2(
    chat_id, public_address, encrypted_private_key, phone_number, email_address
).transact()

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
check_transaction()
# tx_hash = my_contract.functions.transfer(receiver_address).transact({'from': sender_address, 'value': amount})
# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

temp_id = -1
while temp_id != 0:
    temp_id = int(input("Please, enter user's id: "))

    print("Checking user's account from smart contract in process...")

    result = my_contract.functions.getUserByChatId(temp_id).call()

    public_address = result[0]
    encrypted_private_key = result[1]
    phone_number = result[2]
    email_address = result[3]

    # Print the user data
    print(f"Public Address: {public_address}")
    print(f"Encrypted Private Key: {encrypted_private_key}")
    print(f"Phone Number: {phone_number}")
    print(f"Email Address: {email_address}")
    print("Checking user's account from smart contract is successfully finished")
