import json
from web3 import Web3
from decouple import config
import base64

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/ce66ac4ce92a4e92a7fde9d33efced63"))
sdm_ethereum_address = '0xaBE3CFcd92e13e2103980014437ADD8091E92d85'
private_key = 'afd748c43ce14ddd555093d2d3f73254643dc3d423a71ee42d78e53f00b86257'

compiled_contract_path = '../Blockchain/build/contracts/Guai.json'
deployed_contract_address = '0x2D9EAe20E1E7515d47fBB9A5d454Ce7Be59cA03f'


def get_nonce(ETH_address):
    return web3.eth.get_transaction_count(ETH_address)


def send_link(account_address, attributes):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    tx = {
        'nonce': get_nonce(sdm_ethereum_address),
        'gasPrice': web3.eth.gas_price,
        'from': sdm_ethereum_address
    }


    message = contract.functions.setIPFSInfo(account_address, attributes).buildTransaction(tx)
    signed_transaction = web3.eth.account.sign_transaction(message, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print('tx_hash')
    print(web3.toHex(transaction_hash))
    tx_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    # print(tx_receipt)
    with open('IPFS_links.txt', 'a') as fp:
        fp.write(str(tx_receipt) + '\n\n\n')


def send_link_test(account_address, attributes):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    tx = {
        'nonce': get_nonce(sdm_ethereum_address),
        'gasPrice': web3.eth.gas_price,
        'from': sdm_ethereum_address
    }
    message_bytes = attributes.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    message = contract.functions.updateHash(account_address, base64_bytes[:32], base64_bytes[32:]).buildTransaction(tx)
    signed_transaction = web3.eth.account.sign_transaction(message, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print('tx_hash')
    print(web3.toHex(transaction_hash))
    tx_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash, timeout=600)
    print(tx_receipt)
    with open('IPFS_links.txt', 'a') as fp:
        fp.write(str(tx_receipt) + '\n\n\n')

# case_id = 4325525822372369570
# ipfs_link = 'QmZw44QMpqRs5g5pFCrfQ1HzzDQSecKWwFhrKUCwr6hDGt'
# if __name__ == "__main__":
#     send_link(case_id, ipfs_link)
