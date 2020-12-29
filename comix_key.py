import base64
import binascii
import hashlib

def hash(a):
    return binascii.hexlify(hashlib.md5(a).digest()).decode("utf-8").lower()


def reverse(a):
    i = 0
    for l in range(len(a) - 1, i, -1):
        b = a[l]
        a[l] = a[i]
        a[i] = b
        i += 1
    return a


def expand(a):
    l = len(a) * 2
    k = len(a)
    b = bytearray(l)
    b[:k] = a[:k]
    for j in range(len(a), l, 1):
        k -= 1
        b[j] = b[k]
    return b


def calculate_key(digest, item_id, version, publisher_id, index):
    i = int(publisher_id) + 1

    if item_id % 2 == 0:
        i += 1
    
    data_to_hash = str(index % 10).encode() + version[::-1].encode() + str(item_id % 10).encode() + str(index * i).encode() + digest + version.encode() + str(int(publisher_id) % 10).encode()

    e = expand(data_to_hash)

    b = index % 256
    for j in range(0, len(e), 1):
        e[j] = e[j] ^ b
    a = hash(e)
    e = reverse(e)

    return base64.b64encode((a + hash(e)).encode())[:50]