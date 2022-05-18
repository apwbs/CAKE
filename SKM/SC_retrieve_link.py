import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/4a2091f61d304fd5b55251050b1fbe61"))

compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
deployed_contract_address = '0x491AC91F473E5B78A0476179Ad4072926d7DD4AD'


def retrieve_link(case_id):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    message = contract.functions.getIPFSInfo(int(case_id)).call()
    # print(message)
    # print(type(message))
    return message
