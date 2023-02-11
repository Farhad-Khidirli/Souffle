import json
from web3 import Web3

# Connect to the Ethereum network at localhost:7545
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# Set the default account to use when sending transactions
w3.eth.defaultAccount = w3.eth.accounts[0]

# Read the data from the Greeter contract's JSON file
with open('../build/contracts/Greeter.json', "r") as file:
    data = json.load(file)

# Extract the ABI, bytecode, and contract address from the JSON file
abi = data["abi"]
bytecode = data["bytecode"]
# This line is optional and only necessary if you have a deployed contract
contract_address = data["networks"]["5777"]["address"]

# Create a contract object from the ABI and bytecode
Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)

# Deploy the contract to the Ethereum network
tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be processed and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Create a contract object with the address of the deployed contract
contract = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

# Call the "greet" function and print the result
print(contract.functions.greet().call())

# Call the "setGreeting" function with the new greeting "HELLOO"
tx_hash = contract.functions.setGreeting('HELLOO').transact()

# Wait for the transaction to be processed and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Call the "greet" function again and print the result
print(contract.functions.greet().call())
