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

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/ce66ac4ce92a4e92a7fde9d33efced63"))


def get_nonce(ETH_address):
    return web3.eth.get_transaction_count(ETH_address)


receipts = []


def blockchain_interaction(item):
    web3.eth.defaultAccount = '0x405EFF715C40093b7bb1a4B19f4b7880935A89b2'
    private_key = 'c7ea15d89ce6732b8d80aeec48cc5d3aef9d91b5ef1090c10b46706f1dfbaace'

    compiled_contract_path = '../Blockchain/build/contracts/Guai.json'
    deployed_contract_address = '0x2D9EAe20E1E7515d47fBB9A5d454Ce7Be59cA03f'

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
    tx_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash, timeout=800)
    print(tx_receipt)
    receipts.append(tx_receipt)
    with open('receipts.txt', 'a') as fp:
        fp.write(str(tx_receipt) + '\n\n\n')


def get_blockchain_data(param):
    compiled_contract_path = '../Blockchain/build/contracts/Guai.json'
    deployed_contract_address = '0x2D9EAe20E1E7515d47fBB9A5d454Ce7Be59cA03f'

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
    # print(receipts)
    # print(type(receipts))
    # with open('receipts.txt', 'w') as fp:
    #     for item in receipts:
    #         fp.write(str(item) + '\n\n\n')


# dict_users = {
#     '0x6B6E4913eF67a7611De6157CfCaa782F57670d7F': [16, 3, 86],
#     '0xC869a3B0Aed8121c95d2F0016E7F4bBe2a5B9754': [4, 77],
#     '0x243a9E153aD3eb20853cfdb84f6c1AfdFE1849AD': [52]
# }

dict_users = {
    # '0xA5dfE42d5BE39A3aE6c45ED7aBbCD77F8647D54B': [1621, 3142, 862341],
    # '0xFc5c63e8Cbac5a7D9AcD1Ec1480c0ebb5b610518': [4342342, 7712341232, 12, 9128, 981312],
    # '0xE2C818cB638e72790a15204314F8B639031A2810': [52, 92341, 18234, 91478, 9128],
    # '0x1A8dE038A87A8D4e40D3824AA7E35Bc980f08B86': [7676, 1123, 62156],
    # '0x8807ffEfB3Bf55983ee20A592CBac96eF5C43885': [10293, 308472, 7123, 173432, 7071342, 1384192, 128371238, 941728],
    # '0x9D2e04426555A246340ead3F64f6882C997d209a': [7712341232, 12, 12973],
    # '0x94DB0822e13565FA96ea101872D1eFe11e02B6Fd': [91298, 91727711, 192837, 4128, 213297842, 98122198634],
    # '0xB58d94bdD84A5814726C4Ae0C669eB208dEcAe36': [1283120, 1293, 71239714, 721083, 18742734],
    # '0xe756474e595863Be9B18fA619C22c3b408d6b927': [12832, 12328, 821, 831, 213, 29, 471, 72, 4712, 971, 12341, 24],
    '0x1EB869698F7237FFCeB72EE394C484Fc8DC02a9D': [812, 82, 29, 824219, 7234, 124432, 7381, 563442]
}

# address = '0x6B6E4913eF67a7611De6157CfCaa782F57670d7F'
if __name__ == "__main__":
    # store_default_attributes()
    give_attributes()
    # retrieve_attributes(address)
