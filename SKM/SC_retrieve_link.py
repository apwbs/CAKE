import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/e3f35259b98f4b33898ecc8255789dba"))

compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
deployed_contract_address = '0x4d044120a55Ee693d7cf24f3253A36AF3ca23FcA'


def retrieve_link(case_id):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    message = contract.functions.getIPFSInfo(int(case_id)).call()
    # print(message)
    # print(type(message))
    return message
