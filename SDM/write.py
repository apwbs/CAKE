import ipfshttpclient
import sqlite3
import json
import os
import SC_send_link


def main(test_list, case_id, sender, pk_dumped, mk_dumped):
    json_file_header = {
        "sender": None,
        "case_id": None,
        "pk": None,
        "mk": None,
    }
    json_file = {
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

    with open(name_file + 'test', 'a', encoding='utf-8') as f:
        json_file_header['sender'] = str(sender)
        json_file_header['case_id'] = str(case_id)
        json_file_header['pk'] = pk_dumped
        json_file_header['mk'] = mk_dumped
        json.dump(json_file_header, f, ensure_ascii=False, indent=4)
        f.write('\n' + '---\n---\n')

    for i in range(len(recipient)):
        with open(name_file + 'test', 'a', encoding='utf-8') as f:
            json_file['message_id'] = test_list[i][0]
            json_file['content'] = test_list[i][1]
            json_file['hash'] = test_list[i][2]
            json_file['salt'] = test_list[i][3]
            json.dump(json_file, f, ensure_ascii=False, indent=4)
            f.write('\n' + '--->\n')

    with open(name_file + 'test', 'rb+') as filehandle:
        filehandle.seek(-5, os.SEEK_END)
        filehandle.truncate()

    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    print(api)

    new_file = api.add(name_file + 'test')
    hash_file = new_file['Hash']
    print('ipfs hash')
    print(hash_file)

    SC_send_link.send_link(case_id, hash_file)
