import hashlib


def read_private_keys():
    try:
        with open('keys.json', 'rb') as f:
            _private_keys = f.read()
    except FileNotFoundError:
        print('Password store not initialized.')
        return None

    return _private_keys


def is_found(public_address, private_key):
    private_keys = read_private_keys()
    hash_object = hashlib.sha256((public_address + private_key).encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    print(hash_hex)
    if hash_hex.encode() in private_keys:
        return True
    else:
        return False
