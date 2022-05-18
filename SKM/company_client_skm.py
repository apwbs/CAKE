import sqlite3
from web3 import Web3, HTTPProvider
import json

# Connection to SQLite3 users database
conn = sqlite3.connect('Database_SKM/users.db')
x = conn.cursor()

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
    x.execute("SELECT * FROM users_data", )
    users_data = x.fetchall()
    # print(users_data)
    y.execute("SELECT * FROM attributes", )
    attributes_data = y.fetchall()
    # print(attributes_data)
    get_blockchain_data(param)


##################################################################
##################################################################
###################### SMART CONTRACT ############################
##################################################################
##################################################################

web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/4a2091f61d304fd5b55251050b1fbe61"))


def get_nonce(ETH_address):
    return web3.eth.get_transaction_count(ETH_address)


def blockchain_interaction():
    web3.eth.defaultAccount = '0xB91c337448f841aEA90dAc0Ee5eb2B62d0435ddC'
    private_key = '74eeff4de3e90bfd7add0b30754947364d0ce43ad1c911553751b1e21ff3c39a'

    compiled_contract_path = '../Blockchain/build/contracts/Plus.json'
    deployed_contract_address = '0x491AC91F473E5B78A0476179Ad4072926d7DD4AD'

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
    deployed_contract_address = '0x491AC91F473E5B78A0476179Ad4072926d7DD4AD'

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    message = contract.functions.getUserInfo(param).call()
    print(message)
    # print(type(message))
    # print(type(message[0]))


def give_attributes(param):
    for item in param.items():
        x.execute("INSERT OR IGNORE INTO users_data VALUES (?,?)", (item[0], str(item[1])))
        conn.commit()
    blockchain_interaction()


dict_users = {
    '0xB8597f6b522FbF72F4E573a3b854Fb9220a266f4': [36, 86, 16],
    '0x1604BFF8F2378E59071f1D1E469577EEA58E93Ba': [4, 77]
}

address = '0xB8597f6b522FbF72F4E573a3b854Fb9220a266f4'
if __name__ == "__main__":
    # store_default_attributes()
    # give_attributes(dict_users)
    retrieve_attributes(address)
