import json
from web3 import Web3
from decouple import config

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/99e965c1136c4f62ab8dbd7ff52db8b6"))
sdm_ethereum_address = '0x8aeC7b57FDA27F308533cC94Fb22005b73d5Ba6c'

private_key = '5aca8cc67c51fc39fdf256394fef0a4c0bc136fade826e126f448f761e58d1f6'
compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
deployed_contract_address = '0xe272E9669c99884E1E65B67DF683175bAF70f576'


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

# case_id = 4325525822372369570
# ipfs_link = 'QmZw44QMpqRs5g5pFCrfQ1HzzDQSecKWwFhrKUCwr6hDGt'
# if __name__ == "__main__":
#     send_link(case_id, ipfs_link)
