"""

TUTORIAL SEGUIDO:
    https://gnupg.readthedocs.io/en/latest/
    https://gist.github.com/ryantuck/56c5aaa8f9124422ac964629f4c8deb0

"""

import gnupg
import os

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

with open('plain.txt','rb') as f:
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

print(status.ok)
print(status.status)
print(status.stderr)

"""
gpg = gnupg.GPG(gnupghome=os.getcwd())
gpg.encondig = 'utf-8'

input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
key = gpg.gen_key(input_data)

ascii_armored_public_keys = gpg.export_keys("chave-teste-publica")
ascii_armored_private_keys = gpg.export_keys("chave-teste-privada", True)
"""
