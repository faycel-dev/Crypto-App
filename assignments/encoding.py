import sys
from Crypto.Hash import SHA256

enc = ''
for i in sys.argv[1]:
    enc += str(ord(i))
hash_object = SHA256.new(data=bytes(enc, encoding='utf-8'))
enc = hash_object.hexdigest()
enc = bin(int(enc, 16))[3:]

print(enc)
