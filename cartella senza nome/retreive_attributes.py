from email import message
import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/9859e0e845644e878a0306d58fc0f31b"))

compiled_contract_path = '../build/contracts/Plus.json'
deployed_contract_address = '0x56fa32F2306608D7d587D624F46192d279707305'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

message = contract.functions.getUserInfo('0x0DeF95a6f7E59AEE81836810A37f969b2D83249b').call()
print(message)
#print(type(message))
#print(type(message[0]))
