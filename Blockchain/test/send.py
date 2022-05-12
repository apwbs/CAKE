import json
from web3 import Web3, HTTPProvider

blockchain_address = 'http://127.0.0.1:9545'
web3 = Web3(HTTPProvider(blockchain_address))
web3.eth.defaultAccount = web3.eth.accounts[4]
private_key = 'c65c69b7fd8aa3d75dcb510bf48643d83adf4a07fd209ab3e8d03aa05b2fc9ad'

compiled_contract_path = '../build/contracts/Plus.json'
deployed_contract_address = '0xBe6633F52cAE2E652C9a2Bc9DEaee492f175a9EE'

def get_nonce(ETH_address):
        return web3.eth.get_transaction_count(ETH_address)

def send_message(account_address, attributes):
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    nonce = web3.eth.getTransactionCount(web3.eth.defaultAccount)

    tx = {
        'nonce': get_nonce(web3.eth.defaultAccount),
        'gasPrice': web3.eth.gas_price,
        'from': web3.eth.defaultAccount
    }

    message = contract.functions.setUserInfo(account_address, attributes).buildTransaction(tx)
    signed_transaction = web3.eth.account.sign_transaction(message, private_key)

    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(web3.toHex(transaction_hash))


if __name__ == "__main__":
    send_message(web3.eth.accounts[4], [86,16,3])
