"""
NOMES: RODRIGO BISSO

REQUISITOS:
    sudo apt install gpg
    pip3 install python-gnupg

diretorio precisa ter permissao 700 (chmod 700 <nome_dir>)
criar um diretorio com essa permissão dentro do diretorio .gnupg (/home/<usr>/.gnupg/)

TUTORIAL SEGUIDO:
    https://gnupg.readthedocs.io/en/latest/
    https://gist.github.com/ryantuck/56c5aaa8f9124422ac964629f4c8deb0


"""

import gnupg
import os
import sys

if len(sys.argv) < 2 :
    print("Uso: pyhton3 " +sys.argv[0]+ " <arquivo_mensagem>")
    sys.exit(0) 

file_message = sys.argv[1]

gpg = gnupg.GPG(gnupghome=os.getcwd())
imput_data = gpg.gen_key_input(
        name_email='my@email.com',
        passphrase='passphrase',
)

key = gpg.gen_key(imput_data)
print(key)

ascii_armored_public_keys = gpg.export_keys(key.fingerprint)
ascii_armored_private_keys= gpg.export_keys(
        keyids=key.fingerprint,
        secret='True',
        passphrase='passphrase'
)

# exporting keys
with open('mykeyfile.asc', 'w') as f:
    f.write(ascii_armored_public_keys)
    f.write(ascii_armored_private_keys)

with open('mykeyfile.asc', 'r') as f:
    key_data = f.read()

import_result = gpg.import_keys(key_data)
for k in import_result.results:
    print(k)

#encrypting file

with open(file_message,'rb') as f:
    status=gpg.encrypt_file(
        file=f,
        recipients=['my@email.com'],
        output='encrypted.txt.gpg',
    )

print(status.ok)
print(status.status)
print(status.stderr)
print('~'*50)

#decrypting file
with open('encrypted.txt.gpg', 'rb') as f:
    status = gpg.decrypt_file(
        file=f,
        passphrase='passphrase',
        output='decrypted.txt',
    )
    
#Sending keys
#gpg.send_keys(SERVER, PRIVATE_KEY_ID)

#remote import keys
#import_result = gpg.recv_keys('server-name', 'keyid1', 'keyid2', ...)

print(status.ok)
print(status.status)
print(status.stderr)
