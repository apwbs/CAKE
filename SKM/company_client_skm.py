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


receipts = []


def blockchain_interaction(item):
    web3.eth.defaultAccount = '0x989ab0A74915727f4e9dd7057EE7db71bA3DFeaD'
    private_key = '06e2494c0aad10e610aae10f9465becd1d961d761556d2045e9871c619e65384'

    compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
    deployed_contract_address = '0xe272E9669c99884E1E65B67DF683175bAF70f576'

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    # for item in dict_users.items():
    #     index = list(dict_users.keys()).index(item[0])
    #     if index != 1:
    #         nonce = get_nonce(web3.eth.defaultAccount) + 1
    #     else:
    #         nonce = get_nonce(web3.eth.defaultAccount)
    tx = {
            'nonce': get_nonce(web3.eth.defaultAccount),
            'gasPrice': web3.eth.gas_price,
            'from': web3.eth.defaultAccount
    }
    # print(item)
    message = contract.functions.setUserInfo(item[0], item[1]).buildTransaction(tx)
    signed_transaction = web3.eth.account.sign_transaction(message, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print('tx_hash')
    print(web3.toHex(transaction_hash))
    tx_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    print(tx_receipt)
    receipts.append(tx_receipt)


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
    for item in dict_users.items():
        blockchain_interaction(item)
    print(receipts)
    # print(type(receipts))
    with open('receipts.txt', 'w') as fp:
        for item in receipts:
            fp.write(str(item) + '\n\n\n')


# dict_users = {
#     '0x6B6E4913eF67a7611De6157CfCaa782F57670d7F': [16, 3, 86],
#     '0xC869a3B0Aed8121c95d2F0016E7F4bBe2a5B9754': [4, 77],
#     '0x243a9E153aD3eb20853cfdb84f6c1AfdFE1849AD': [52]
# }

dict_users = {
    '0x17E1386Fc68e22964acF3f2400Ed5d919F6ee7B6': [1621, 3142, 862341],
    '0xf58B22d0aa23b028474aAbC4058dcb01DFB8847d': [4342342, 7712341232, 12, 9128, 981312],
    '0xEa4e40ACf5a44502FE847d168004106989a28A29': [52, 92341, 18234, 91478, 9128],
    '0x8F5e1d5BfAd5f618074b56433c21a1C68eB46532': [7676, 1123, 62156],
    '0x3Ae8e94fa125caF58938442859dBC4c0C24B5714': [10293, 308472, 7123, 173432, 7071342, 1384192, 128371238, 941728],
    '0x59C49E84eCaA358FA9b8e5e4Cf8917370841beB9': [7712341232, 12, 12973],
    '0x0a00166b822b3aa06066FB64d2b1A27f50d34163': [91298, 91727711, 192837, 4128, 213297842, 98122198634],
    '0xbf49B4Cb443AA458CA94badD38330366eB39376D': [1283120, 1293, 71239714, 721083, 18742734],
    '0xFF6C1D89590b92428157Cd0a54BcFAbeE5b30AC4': [12832, 12328, 821, 831, 213, 29, 471, 72, 4712, 971, 12341, 24],
    '0x14FAAae3c58Ea15450F14E61a4eA072d8d735693': [812, 82, 29, 824219, 7234, 124432, 7381, 563442]
}

# address = '0x6B6E4913eF67a7611De6157CfCaa782F57670d7F'
# if __name__ == "__main__":
    # store_default_attributes()
    # give_attributes()
    # retrieve_attributes(address)
