import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/99e965c1136c4f62ab8dbd7ff52db8b6"))

compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
deployed_contract_address = '0xe272E9669c99884E1E65B67DF683175bAF70f576'


def retrieve_link(case_id):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    message = contract.functions.getIPFSInfo(int(case_id)).call()
    # print(message)
    # print(type(message))
    return message
