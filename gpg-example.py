"""
NOMES: RODRIGO BISSO
       GUSTAVO CARDOZO
REQUISITOS:
    sudo apt install gpg
    pip3 install python-gnupg

diretorio precisa ter permissao 700 (chmod 700 <nome_dir>)
criar um diretorio com essa permissão dentro do diretorio .gnupg (/home/<usr>/.gnupg/)

TUTORIAL SEGUIDO:
    https://gnupg.readthedocs.io/en/latest/
    https://gist.github.com/ryantuck/56c5aaa8f9124422ac964629f4c8deb0
    https://pymotw.com/2/argparse/
    http://zetcode.com/python/argparse/

"""

import gnupg
import os
import sys
import argparse

def export_keys(gpg, key): #local -> to file
    
    ascii_armored_public_keys = gpg.export_keys(key.fingerprint)
    ascii_armored_private_keys= gpg.export_keys(
            keyids=key.fingerprint,
            secret='True',
            passphrase='passphrase'
    )
    
    with open('mykeyfile.asc', 'w') as f:
        f.write(ascii_armored_public_keys)
        f.write(ascii_armored_private_keys)

def import_keys(): #local
    with open('mykeyfile.asc', 'r') as f:
        key_data = f.read()

    import_result = gpg.import_keys(key_data)
    for k in import_result.results:
        print(k)

    return import_result

def import_keys_server():
    
    import_result = gpg.recv_keys('server-name', 'keyid')


def export_keys_server(gpg, keys): #Sending keys
    #gpg.send_keys(SERVER, PRIVATE_KEY_ID)

def help() 
    parser = argparse.ArgumentParser(description="gerenciador de chaves gpg")
    parser.add_argument("--name", action="store", dest="name_usr")
    parser.add_argument("--email", action="store", dest="email_usr")
    parser.add_argument("--passphrase", action="store", dest="passphrase")

    args = parser.parse_args()
    
    return args

if __name__ == "__main__":

    
    """
    if len(sys.argv) < 2 :
        print("Uso: pyhton3 " +sys.argv[0]+ " <arquivo_mensagem>")
        sys.exit(0) 

    file_message = sys.argv[1]
    """
    args = help()
    gpg = gnupg.GPG(gnupghome=os.getcwd())
    imput_data = gpg.gen_key_input(
            name_email='my@email.com',
            passphrase='passphrase',
    )

    key = gpg.gen_key(imput_data)
    print(key)
    
    """
    print(status.ok)
    print(status.status)
    print(status.stderr)
    """
