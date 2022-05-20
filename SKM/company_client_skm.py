import sqlite3
from web3 import Web3, HTTPProvider
import json

# Connection to SQLite3 attributes database
connection = sqlite3.connect('Database_SKM/attributes.db')
y = connection.cursor()


def store_default_attributes():
    dict_attributes = {
        36: 'manager',
        86: 'clerk',
        16: 'advanced',
        4: 'student',
        77: 'restricted'
    }
    for item in dict_attributes.items():
        y.execute("INSERT OR IGNORE INTO attributes VALUES (?,?)", (item[0], item[1]))
        connection.commit()


def retrieve_attributes(param):
    return get_blockchain_data(param)


##################################################################
##################################################################
###################### SMART CONTRACT ############################
##################################################################
##################################################################

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/99e965c1136c4f62ab8dbd7ff52db8b6"))


def get_nonce(ETH_address):
    return web3.eth.get_transaction_count(ETH_address)


def blockchain_interaction():
    web3.eth.defaultAccount = '0x989ab0A74915727f4e9dd7057EE7db71bA3DFeaD'
    private_key = '06e2494c0aad10e610aae10f9465becd1d961d761556d2045e9871c619e65384'

    compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
    deployed_contract_address = '0xe272E9669c99884E1E65B67DF683175bAF70f576'

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    for item in dict_users.items():
        index = list(dict_users.keys()).index(item[0])
        if index != 1:
            nonce = get_nonce(web3.eth.defaultAccount) + 1
        else:
            nonce = get_nonce(web3.eth.defaultAccount)
        tx = {
            'nonce': nonce,
            'gasPrice': web3.eth.gas_price,
            'from': web3.eth.defaultAccount
        }
        # print(item)
        message = contract.functions.setUserInfo(item[0], item[1]).buildTransaction(tx)
        signed_transaction = web3.eth.account.sign_transaction(message, private_key)
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        print(web3.toHex(transaction_hash))


def get_blockchain_data(param):
    compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
    deployed_contract_address = '0xe272E9669c99884E1E65B67DF683175bAF70f576'

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    message = contract.functions.getUserInfo(param).call()
    # print(message)
    return message


def give_attributes():
    blockchain_interaction()


dict_users = {
    '0x6B6E4913eF67a7611De6157CfCaa782F57670d7F': [16, 3, 86],
    '0xC869a3B0Aed8121c95d2F0016E7F4bBe2a5B9754': [4, 77],
    '0x243a9E153aD3eb20853cfdb84f6c1AfdFE1849AD': [52]
}

# address = '0x6B6E4913eF67a7611De6157CfCaa782F57670d7F'
# if __name__ == "__main__":
    # store_default_attributes()
    # give_attributes(dict_users)
    # retrieve_attributes(address)
