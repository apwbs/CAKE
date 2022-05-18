import json
from web3 import Web3
from decouple import config

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/4a2091f61d304fd5b55251050b1fbe61"))
sdm_ethereum_address = '0xD81Cbe02b50C19e01bC0931e3871963db8526B0E'
# private_key = '73c720dbc3488d4afc5912cf9d9ed90de14cce58e863abd6cce3ff9bb4b022a8'
private_key = config('private_key')
compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
deployed_contract_address = '0x491AC91F473E5B78A0476179Ad4072926d7DD4AD'


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


# case_id = 4325525822372369570
# ipfs_link = 'QmZw44QMpqRs5g5pFCrfQ1HzzDQSecKWwFhrKUCwr6hDGt'
# if __name__ == "__main__":
#     send_link(case_id, ipfs_link)
