import ipfshttpclient
import sqlite3
import json
import os

sender_address = 'aiufhaisufhgasdoif'


def main(test_list, case_id):
    json_file = {
        "case_id": None,
        "message_id": None,
        "hash": None,
        "salt": None,
        "content": None
    }
    recipient = []
    for i in range(len(test_list)):
        recipient.append(test_list[i][0])
    recipt_string = ''
    for i in range(len(recipient)):
        recipt_string = recipt_string + recipient[i] + ',_'
    recipt_string = recipt_string[:-1]
    name_file = 'python_'+recipt_string+'.txt'

    for i in range(len(recipient)):
        with open(name_file + 'test', 'a', encoding='utf-8') as f:
            json_file['case_id'] = str(case_id)
            json_file['message_id'] = test_list[i][0]
            json_file['content'] = test_list[i][1]
            json_file['hash'] = test_list[i][2]
            json_file['salt'] = test_list[i][3]
            json.dump(json_file, f, ensure_ascii=False, indent=4)
            f.write('\n' + '--->')

    with open(name_file + 'test', 'rb+') as filehandle:
        filehandle.seek(-4, os.SEEK_END)
        filehandle.truncate()

    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    print(api)

    new_file = api.add(name_file + 'test')
    hash_file = new_file['Hash']
    print(hash_file)

    # with open(name_file, "a") as text_file:
    #     text_file.write('\n' + hash_file)

    # Connection to SQLite3 database
    conn = sqlite3.connect('Database_SDM/database.db')
    x = conn.cursor()

    x.execute(
        "UPDATE ciphertext SET ipfs_hash=? WHERE sender_address=? AND recipient_address=? AND case_id=?",
        (hash_file, sender_address, recipient[0], str(case_id)))
    conn.commit()
