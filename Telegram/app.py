import json
from web3 import Web3
from validate_private_key import is_found
from email_verify import verify_email
from twilio_verify import verify_number
# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))


# Validate provided address
def validate_address(_address):
    if _address not in w3.eth.accounts:
        raise Exception(f"Address {_address} not found in the list of accounts")


def validate_pair(_address, _key):
    if not is_found(_address, _key):
        raise Exception(f"Address {_address} \n Key {_key} \n does not match")


def get_balance(_address):
    balance = w3.fromWei(w3.eth.getBalance(_address), "ether")
    return balance


def to_ether(_amount):
    return Web3.toWei(_amount, 'ether')


def check_transaction(_tx_receipt):
    if _tx_receipt.status == 1:
        print("Transaction successful!")
        logs = my_contract.events.ETransfer().processReceipt(_tx_receipt)
        if len(logs) > 0:
            print(f"Transfer event emitted: {logs[0]['args']}")
        else:
            print("No transfer event emitted")
    else:
        print("Transaction failed with error:", _tx_receipt['status'])


def registration(_chat_id, _public_address, _encrypted_private_key, _phone_number, _email_address):
    _tx_hash = my_contract.functions.registerUser2(
        _chat_id, _public_address, _encrypted_private_key, _phone_number, _email_address
    ).transact()

    _tx_receipt = w3.eth.waitForTransactionReceipt(_tx_hash)
    check_transaction(_tx_receipt)


def transfer(_chat_id, _receiver, _amount):
    _sender = my_contract.functions.getUserByChatId(_chat_id).call()[0]
    _tx_hash = my_contract.functions.transfer2(_chat_id, _receiver).transact({'from': _sender, 'value': _amount})
    _tx_receipt = w3.eth.waitForTransactionReceipt(_tx_hash)
    print("Checking for transfer transaction...")
    check_transaction(_tx_receipt)


def get_user_by_id(_id):
    result = my_contract.functions.getUserByChatId(_id).call()

    public_address = result[0]
    encrypted_private_key = result[1]
    phone_number = result[2]
    email_address = result[3]

    # Print the user data
    print(f"Public Address: {public_address}")
    print(f"Encrypted Private Key: {encrypted_private_key}")
    print(f"Phone Number: {phone_number}")
    print(f"Email Address: {email_address}")


# Read the data from the EtherTransfer contract's JSON file
with open('../build/contracts/Transfer.json', "r") as file:
    data = json.load(file)

# Extract the ABI, bytecode, and contract address from the JSON file
abi = data["abi"]
bytecode = data["bytecode"]

email = input("Please, enter your valid email address: ")
verify_email(email)

number = input("Please, enter US phone number; sample: {+12507329120}: ")
for i in range(3):
    print(f"You have {3-i} attempts to enter OTP, please be careful")
    response = verify_number(number)
    if response == "approved":
        print("Success!")
        break

if response != "approved":
    exit()


# The address of the account that will send the Ethereum
sender_address = Web3.toChecksumAddress(input("Enter the sender's address: "))
validate_address(sender_address)
w3.eth.defaultAccount = sender_address

private_key = input("Enter the sender's private key: ")
validate_pair(sender_address, private_key)

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

registration(3,
             "0xC93A80673EB401f363eA247875d0f45FAdB00A33",
             "31da11b1f176e5e78d21fb9f90c314ed30f89c604aa9f1c6a2122d6aee1cded1",
             "123456",
             "far@gmail.com")

registration(2,
             "0x1aFAb0A962DEB2b5034F23706d7D736D85251213",
             "12222e5b6ee326e0ed4e8a027bf17bf9b9e41652e7a429caf9481663f88b109e",
             "654321",
             "lol@gmail.com")

transfer(2, receiver_address, amount)

# tx_hash = my_contract.functions.transfer(receiver_address).transact({'from': sender_address, 'value': amount})
# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

temp_id = -1
while temp_id != 0:
    temp_id = int(input("Please, enter user's id: "))
    get_user_by_id(temp_id)
