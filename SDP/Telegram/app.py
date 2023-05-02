import json
from eth_account import Account
from eth_account.messages import encode_defunct, _hash_eip191_message
from data_security import encrypt, decrypt, init_key
from web3 import Web3
from validate_private_key import is_found
from email_verify import verify_email, send_email_otp
from twilio_verify import verify_number, send_verification
from postgresql import insert_into, retrieve_all, close_cursor, retrieve_by_id
from key import salt, keyword

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))


# Validate provided address
def validate_address(_address):
    if _address not in w3.eth.accounts:
        # raise Exception(f"Address {_address} not found in the list of accounts")
        print(f"Address {_address} not found in the list of accounts")
        return False
    return True


def validate_pair(_address, _key):

    # Get the public key (address) from the private key
    account = Account.from_key(_key)
    derived_public_key = account.address

    if derived_public_key.lower() == _address.lower():
        return True
    else:
        return False


def get_balance(_chat_id):
    address = get_user_by_id(_chat_id)
    balance = w3.fromWei(w3.eth.getBalance(address['public_address']), "ether")
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


def register_for_telegram(_chat_id, _public_address, _private_key, _phone_number, _email_address):
    key = init_key(keyword, salt)

    encrypted_private_key = encrypt(_private_key.encode(), key)
    encrypted_phone_number = encrypt(_phone_number.encode(), key)
    encrypted_email_address = encrypt(_email_address.encode(), key)
    encrypted_balance = encrypt(str(100).encode(), key)

    _tx_hash = my_contract.functions.registerUser(
        _chat_id, _public_address, encrypted_private_key, encrypted_phone_number, encrypted_email_address
    ).transact()

    _tx_receipt = w3.eth.waitForTransactionReceipt(_tx_hash)
    check_transaction(_tx_receipt)
    print("Registration to smart contract loaded")
    # Storing encrypted data to the database (chat_id isn't encrypted)
    insert_into(_chat_id,
                _public_address,
                encrypted_private_key,
                encrypted_phone_number,
                encrypted_email_address,
                encrypted_balance)


def registration_manual(_chat_id, _public_address, _private_key, _phone_number, _email_address):
    _tx_hash = my_contract.functions.registerUser(
        _chat_id, _public_address, _private_key, _phone_number, _email_address
    ).transact()

    print("Registration Manual...")
    _tx_receipt = w3.eth.waitForTransactionReceipt(_tx_hash)
    check_transaction(_tx_receipt)
    _balance = get_balance(_chat_id)

    # Reserved for limited purposes
    user, found = retrieve_by_id(_chat_id)
    if not found:
        # Creating a key
        key = init_key(keyword, salt)

        encrypted_private_key = encrypt(_private_key, key)
        encrypted_phone_number = encrypt(_phone_number, key)
        encrypted_email_address = encrypt(_email_address, key)
        encrypted_balance = encrypt(_balance, key)

        print("Chat id is: ", _chat_id)
        print("Encrypted Public address is: ", _public_address)
        print("Encrypted Private key is: ", encrypted_private_key)
        print("Encrypted Phone number is: ", encrypted_phone_number)
        print("Encrypted Email address is: ", encrypted_email_address)
        print("Encrypted Balance is: ", encrypted_balance)

        # Storing encrypted data to the database (chat_id isn't encrypted)
        insert_into(_chat_id,
                    _public_address,
                    encrypted_private_key,
                    encrypted_phone_number,
                    encrypted_email_address,
                    encrypted_balance)


def phone_otp(_phone_number):
    send_verification(_phone_number)
    for i in range(3):
        print(f"You have {3 - i} attempts to enter OTP, please be careful")
        otp_code = input("Please enter the OTP: ")
        response = verify_number(_phone_number, otp_code)
        if response == "approved":
            print("Success!")
            break

    if response != "approved":
        print("Number verification failed.")
        exit()


def registration(_chat_id):
    print("Processing registration...")

    verifier = False
    while not verifier:
        _public_address = input("Input your public address here: ")
        verifier = validate_address(_public_address)

    verifier = False
    while not verifier:
        _private_key = input("Enter your private key: ")
        verifier = validate_pair(_public_address, _private_key)

    _email_address = input("Please, enter your valid email address: ")
    send_email_otp(_email_address)
    _otp_email = int(input('Enter otp code:'))
    if verify_email(_otp_email) == 'approved':
        print("Success")
    else:
        print("Failed")
    _phone_number = input("Please, enter US phone number; sample: {+12507329120}: ")
    # phone_otp(_phone_number)

    _balance = get_balance(_public_address)

    # Creating a key
    key = init_key(keyword, salt)

    # Reverting data to the encrypted
    encrypted_private_key = encrypt(_private_key.encode(), key)
    encrypted_phone_number = encrypt(_phone_number.encode(), key)
    encrypted_email_address = encrypt(_email_address.encode(), key)
    encrypted_balance = encrypt(str(_balance).encode(), key)

    print("Chat id is: ", _chat_id)
    print("Encrypted Private key is: ", encrypted_private_key)
    print("Encrypted Phone number is: ", encrypted_phone_number)
    print("Encrypted Email address is: ", encrypted_email_address)
    print("Encrypted Balance is: ", encrypted_balance)
    _tx_hash = my_contract.functions.registerUser(
        _chat_id, _public_address, _private_key, _phone_number, _email_address
    ).transact()
    _tx_receipt = w3.eth.waitForTransactionReceipt(_tx_hash)
    check_transaction(_tx_receipt)
    print("Registration to smart contract loaded")
    # Storing encrypted data to the database (chat_id isn't encrypted)
    insert_into(_chat_id,
                _public_address,
                encrypted_private_key,
                encrypted_phone_number,
                encrypted_email_address,
                encrypted_balance)

    print("Successful registration!")


def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


def transfer(_chat_id, _receiver, _amount):
    user_data = my_contract.functions.getUserByChatId(_chat_id).call()
    _sender, _private_key, _phone_number = user_data[0], user_data[1], user_data[2]

    key = init_key(keyword, salt)
    _decrypted_private_key = decrypt(_private_key, key).decode()
    _decrypted_phone_number = decrypt(_phone_number, key).decode()

    #  phone_otp(_decrypted_phone_number)

    # Signature signing process
    msg = "Hello"
    hex_msg = msg.encode('utf-8').hex()
    message = encode_defunct(text=hex_msg)

    signed_message = w3.eth.account.sign_message(message, private_key=_decrypted_private_key)
    message_hash = "0x" + _hash_eip191_message(message).hex()
    v, hex_r, hex_s = signed_message.v, to_32byte_hex(signed_message.r), to_32byte_hex(signed_message.s)

    # Create transaction
    # _tx_hash = my_contract.functions.transfer(_receiver, message_hash, v, hex_r, hex_s).transact(
    #     {'from': _sender, 'value': _amount})
    _amount = to_ether(int(_amount))
    txn_dict = my_contract.functions.transfer(_receiver, message_hash, v, hex_r, hex_s).buildTransaction({
        'from': _sender,
        'value': _amount,
        'nonce': w3.eth.getTransactionCount(_sender),
        'gas': 50000,
        'gasPrice': w3.eth.gas_price
    })

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=_decrypted_private_key)
    _tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    _tx_receipt = w3.eth.waitForTransactionReceipt(_tx_hash)
    print("Checking for transfer transaction...")
    check_transaction(_tx_receipt)


def get_user_by_id(_id):
    user_data = my_contract.functions.getUserByChatId(_id).call()
    public_address, encrypted_private_key, encrypted_phone_number, encrypted_email_address = user_data[0], user_data[1], \
        user_data[2], user_data[3]

    key = init_key(keyword, salt)

    _decrypted_private_key = decrypt(encrypted_private_key, key).decode()
    _decrypted_phone_number = decrypt(encrypted_phone_number, key).decode()
    _decrypted_email_address = decrypt(encrypted_email_address, key).decode()

    decrypted_user_data = {
        'id': _id,
        'public_address': public_address,
        'private_key': _decrypted_private_key,
        'phone_number': _decrypted_phone_number,
        'email_address': _decrypted_email_address
    }
    return decrypted_user_data


def is_found_chat_id(_chat_id):
    return my_contract.functions.userExists(_chat_id).call()


def load_from_db():
    rows = retrieve_all()
    column_names = ['id', 'public_address', 'private_key', 'phone_number', 'email_address', 'balance']
    for row in rows:
        row_dict = dict(zip(column_names, row))
        if is_found_chat_id(row_dict['id']):
            continue
        else:  # Load from database to the smart contract
            registration_manual(row_dict['id'],
                                row_dict['public_address'],
                                bytes(row_dict['private_key']),
                                bytes(row_dict['phone_number']),
                                bytes(row_dict['email_address']))


# Read the data from the EtherTransfer contract's JSON file
with open('../build/contracts/Transfer.json', "r") as file:
    data = json.load(file)

# Extract the ABI, bytecode, and contract address from the JSON file
abi = data["abi"]
bytecode = data["bytecode"]

w3.eth.defaultAccount = w3.eth.accounts[0]
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Get the contract address
contract_address = tx_receipt.contractAddress
print(f"Contract address: {contract_address}")

# Create a contract instance
my_contract = w3.eth.contract(address=contract_address, abi=abi)

# Testing Application - TEMP
# / ----------------------------------- /

load_from_db()  # Encrypted data

# chat_id = -1
# while chat_id != 0:
#     print("Imitation of taking user's chat_id...")
#     chat_id = int(input("Hello! Please, enter user's id if exists: "))
#     if is_found_chat_id(chat_id):
#         print("Printing user's details based on provided chat_id...")
#         get_user_by_id(chat_id)
#         # User details should be retrieved and decrypted to proceed
#         choose = int(input("Would you like to make transfer? 1 - yes, 0 - no: "))
#         if choose == 1:
#             receiver_address = Web3.toChecksumAddress(input("Enter the receiver's address: "))
#             validate_address(receiver_address)
#             amount = to_ether(int(input("Enter the amount of ether to send: ")))
#             transfer(chat_id, receiver_address, amount)
#         else:
#             exit(0)
#     else:
#         print("Not found, please go to the registration.")
# registration(chat_id)