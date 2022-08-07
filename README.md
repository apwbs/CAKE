# Fine-grained Data Access Control for Collaborative Process Execution on Blockchain

This repository is the implementation of the Cake approach presented in paper "Fine-grained Data Access Control for
Collaborative Process Execution on Blockchain". 

## Guide to run the whole architecture
In order to run the system, the following libraries must be installed: 
python3, charm https://github.com/JHUISI/charm, rsa, web3 (python version), python-decouple, pycryptodome.
 
The first thing to do is to generate the private/public keys: 
Open a terminal and
1. move in the SDM folder and run the 'generate_keys()' 
with python3 rsa_sdm.py.
2. move in the SKM folder and run the 'generate_keys()' 
function with python3 rsa_skm.py.

Then the private/public keys of each client must be generated. To do this:
1. move in the SDM folder and run the 'generate_keys()' 
function with python3 handshake_readers.py.

After the creation of all the necessary keys, one must give the attributes to the parties involved in the process: first action of Figure 2 of the paper.
If one wants to use integers as attributes skip the following step. 
1. move in the SKM folder and modify the 'dict_attributes' 
dictionary and run the function 'store_default_attributes()' with python3 company_client_skm.py to store it in a local database. 

2. add the Ethereum addresses and the chosen attributes (string or integers) in the 'dict_users' 
dictionary and run the function 'give_attributes()' 
with python3 company_client_skm.py to upload them in the Smart Contract. 

To send a message to the SDM component the following steps must be followed:
1. move in the SDM folder
2. run python3 server.py (in a terminal window)
3. in 'client.py' send the 'Please certify signature' message (line 53) commenting all the others lines exept line 67 with python3 client.py.
5. comment line 53 and modify the 'msg' variable with the received number. Uncomment lines 57,58,59,60. 
6. modify the 'text' variable with the plaintext and the 'policy' variable with the policy to cipher the plaintext. Uncomment line 63. Run python3 client.py (in a different terminal window)

To read a message from the SKM component the first thing to do is to ask for a key:
1. move in the SKM folder
2. uncomment lines 41,42 and modify the message_id variable 
with the message_id received from the Data Owner. 
3. send the 'Please generate my key' message with python3 client.py

After receiving and saving the key, to read a message the steps are the following:
1. comment line 41,42 and uncomment lines 49,50,51
2. modify the variable slice_id with the 
slice_id that the reader wants to access
3. send the 'Please read my data' message with python3 client.py
