# this file shows you how to interact with a script running remotely
# especially if you want to interact multiple times, this is much easier than doing it by hand
# for example, in Assignment 3, exercise 3

# this package is required for everything, you can install it with 'pip install pwntools'
from pwn import *

# we need to connect to the remote server (this requires us to be in the Radboud network)
# we do so by setting up a remote process
r = remote('appliedcrypto.cs.ru.nl', 4145)

# this allows us to read the bits we've received
output = r.recv()
print(output)

# we can also send bits just as easy. For exercise 3 we want to send either '0' or '1'
r.sendline('0')

# what did we get back?
output = str(r.recv())
result = output.rfind("The challenge was")
print(output[2:result])

# in exercise 1 you need to apply a hash function, you can take it from PyCryptodome
from Crypto.Hash import SHA3_256
hash_function = SHA3_256.new()
hash_function.update(b'Here we are hashing some bytestring')
print(hash_function.hexdigest())

# to make your life easier, here is the modulus and exponent for exercise 1
modulus = int("""
155DCEBC 04BD2F5E BE9E85B3 BD3B4C00 DB8FFD13 2460EFB4
9CCC075B CE16D9DD E73F5579 0A3C2787 A4444D23 53286320
86827E70 72AC1BF7 02904EF0 25A4A6FD EEF0E482 C5F76D29
3774F3AE 9E6B5DA4 7B09FD3C D713AE6C A9AADA25 3CDB15FB
1EA14F94 6E1A5DE5 FE922A1D 3FB9B733 8F738A6D A0AEAA36
ADCAD991 DE84537C 2A399BC9 65BBEE58 689BE4C2 6DBDBF89
A2CC80D2 3A28B35D 8249B26A 870190CB E6B875DC 51FD4FE5
886AFA97 BDD98E2E FEC332B2 96E56F69 61C73BD8 BFE6CE64
DABFE02E 749004D8 D4157E5D 70FA0D1F B37F9891 0EAE1B59
3D15C924 31D8821D E683626C 3C125D84 B5E90B0D 87BA3977
2F407841 76B96E2F 42988B13 E210A0FB B
""".replace('\n', '').replace(' ', ''), 
16)
public_key = 65533

# and I copied the prime for exercise 3 too
prime = int("""
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF""".replace('\n', '').replace(' ', ''), 
16)