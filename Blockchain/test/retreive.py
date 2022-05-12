import json
from web3 import Web3, HTTPProvider

blockchain_address = 'http://127.0.0.1:9545'
web3 = Web3(HTTPProvider(blockchain_address))
web3.eth.defaultAccount = web3.eth.accounts[1]

compiled_contract_path = '../build/contracts/Plus.json'
deployed_contract_address = '0xBe6633F52cAE2E652C9a2Bc9DEaee492f175a9EE'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

message = contract.functions.getUserInfo(web3.eth.accounts[4]).call()
print(message)
#print(type(message))
#print(type(message[0]))
