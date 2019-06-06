import ed25519


def generate_key():
    """
    To generate ed25519 key pair, and use verifying_key as api_token.

    :return:
    """
    signing_key, verifying_key = ed25519.create_keypair()
    # open("my-secret-key","wb").write(signing_key.to_bytes())
    vkey_hex = verifying_key.to_ascii(encoding="hex").decode()
    # print("the public key is", str(vkey_hex))
    return vkey_hex


if __name__ == "__main__":
    generate_key()
