"""
NOMES: RODRIGO BISSO
       GUSTAVO CARDOZO
REQUISITOS:
    sudo apt install gpg
    pip3 install python-gnupg

diretorio precisa ter permissao 700 (chmod 700 <nome_dir>)
criar um diretorio com essa permissão dentro do diretorio .gnupg (/home/<usr>/.gnupg/)

TUTORIAL SEGUIDO:
    https://gnupg.readthedocs.io/en/latest/ *
    https://pythonhosted.org/gnupg/gnupg.html *
    https://pymotw.com/2/argparse/
    http://zetcode.com/python/argparse/
"""

import gnupg
import os
import sys
import argparse


def import_keys(): #local
    
    with open('mykeyfile.asc', 'r') as f:
        key_data = f.read()

    import_result = gpg.import_keys(key_data)
    
    return import_result

def import_keys_server():
    pass
    #import_result = gpg.recv_keys('server-name', 'keyid')


def export_keys_server(gpg, keys): #Sending keys
    pass
    #gpg.send_keys(SERVER, PRIVATE_KEY_ID)
"""
def delete_keys():
    
    public_keys = gpg.list_keys() 
    private_keys = gpg.list_keys(secret=True)
    
    for key in private_keys:
        gpg.delete_keys(key['fingerprint'], True, passphrase="disney")
    
    for key in public_keys:
        gpg.delete_keys(key['fingerprint'])
#"""    
def list_keys(gpg, user_name):
    
    public_keys = gpg.list_keys() 
    private_keys = gpg.list_keys(secret=True)
    
    print("public keys")
    for key in public_keys:
        if key['uids'][0].split(' ')[0] == user_name:
            print(key)

    print("private keys: ")
    for key in private_keys:
        if key['uids'][0].split(' ')[0] == user_name:
            print(key)    

def export_keys(gpg, key, passphrase):
    
    ascii_armored_public_keys = gpg.export_keys(key.fingerprint)
    ascii_armored_private_keys= gpg.export_keys(
            keyids = key.fingerprint,
            secret = 'True',
            passphrase = passphrase
    )

def generate_key(gpg, name, email, passphrase):
    
    user = {
        'name_real' : name,
        'name_email' : email,
        #'expire_date' : '2019-09-10',
        'key_type': 'RSA',
        'key_length': 4096,
        'key_usage': '',
        #'subkey_type':'RSA',
        #'subkey_length' : "encrypt,sign,auth",
        'passphrase': passphrase }

    user_input = gpg.gen_key_input(**user)
    #print(user_input)
    user_key = gpg.gen_key(user_input)
    export_keys(gpg, user_key, user['passphrase'])
    

def help(): 
    parser = argparse.ArgumentParser(description="gerenciador de chaves gpg")
#    subparsers = parser.add_subparsers()
    
    parser.add_argument("--email", action="store", dest="email", 
                         help= """Needed by the arguments --generate key and --list-key""")

    group_generate = parser.add_argument_group("Generate pair keys")
    group_generate.add_argument("--generate-keys", action="store_true", 
                                 help="""Need the arguments --name, --email and --passphrase 
                                       to generate the pair key""")
    group_generate.add_argument("--name", action="store", dest="name")
    group_generate.add_argument("--passphrase", action="store", dest="passphrase")
    
    group_list = parser.add_argument_group("List keys")
    group_list.add_argument("--list-keys", action="store_true", 
                                 help="""Need the arguments --email to list the keys""")

    group_delete = parser.add_argument_group("Delete pair keys")
    group_delete.add_argument("--delete-keys", action="store_true", 
                                 help="""Need the argumentes --email and --passphrase 
                                         to delete the keys""")
    args = parser.parse_args()
    
    return args

if __name__ == "__main__":

    args = help()
    
    #print(args)
    #print(args.user_name) 
    gpg = gnupg.GPG(gnupghome=os.getcwd())
    if args.generate_key == True:
        generate_key(gpg, args.user_name, args.user_email, args.user_passphrase)
     
    #delete_keys()
    #list_keys(gpg, args.user_name)
    if args.list_keys == True:
        list_keys(gpg, args.user_name)

