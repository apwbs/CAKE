import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/9859e0e845644e878a0306d58fc0f31b"))
private_key = 'be26ae4bd77cb4bf93c0549509b04541e92b60063276f208e4464752b8b16011'

compiled_contract_path = '../build/contracts/Plus.json'
deployed_contract_address = '0x56fa32F2306608D7d587D624F46192d279707305'

def get_nonce(ETH_address):
        return web3.eth.get_transaction_count(ETH_address)

def send_message(account_address, attributes):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    tx = {
        'nonce': get_nonce('0x42643D2df61Cf8C1ab11128D09c5308DA23292B5'),
        'gasPrice': web3.eth.gas_price,
        'from': '0x42643D2df61Cf8C1ab11128D09c5308DA23292B5'
    }

    message = contract.functions.setIPFSInfo(account_address, attributes).buildTransaction(tx)
    signed_transaction = web3.eth.account.sign_transaction(message, private_key)

    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(web3.toHex(transaction_hash))


if __name__ == "__main__":
    send_message(4325525822372369570, 'QmZw44QMpqRs5g5pFCrfQ1HzzDQSecKWwFhrKUCwr6hDGt')
