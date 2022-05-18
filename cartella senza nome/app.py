import json
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/9859e0e845644e878a0306d58fc0f31b"))

# truffle development blockchain address
#blockchain_address = 'http://127.0.0.1:7545'
# Client instance to interact with the blockchain
#web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
#web3.eth.defaultAccount = web3.eth.accounts[0]
#web3.eth.defaultAccount = '0x7C6896714508572c056C8316FD69604eF1BA2bCD'

# Path to the compiled contract JSON file
compiled_contract_path = 'build/contracts/HelloWorld.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0xe6d6AD78d6EF78efb083325a413b5B7E204b0150'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    # fetch contract's abi - necessary to call its functions
    contract_abi = contract_json['abi']

# Fetch deployed contract reference
contract = w3.eth.contract(
    address=deployed_contract_address, abi=contract_abi)

# Call contract function (this is not persisted to the blockchain)
message = contract.functions.sayHello().call()
print('sono qui')
print(message)
print('ora sono qui')

# executes setPayload function
#tx_hash = contract.functions.setPayload('abc').transact()
# waits for the specified transaction (tx_hash) to be confirmed
# (included in a mined block)
#tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
#print('tx_hash: {}'.format(tx_hash.hex()))
