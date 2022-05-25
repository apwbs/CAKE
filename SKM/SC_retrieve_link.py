import json
from web3 import Web3
import base64

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/ce66ac4ce92a4e92a7fde9d33efced63"))

compiled_contract_path = '../Blockchain/build/contracts/Guai.json'
deployed_contract_address = '0x2D9EAe20E1E7515d47fBB9A5d454Ce7Be59cA03f'


def retrieve_link(case_id):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    message = contract.functions.getHash(int(case_id)).call()
    message_bytes = base64.b64decode(message)
    message = message_bytes.decode('ascii')
    return message


# if __name__ == "__main__":
#     retrieve_link()