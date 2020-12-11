from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
import argparse
import sys


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        required=True, type=str,
        help="checking file"
    )
    parser.add_argument(
        "-k", "--key",
        required=True, type=str,
        help="file with public key"
    )
    return parser


def signature_check(filename, public_key):
    try:
        src_file = open(filename, "rb")
    except FileNotFoundError:
        print("No such file! Try again!")
        return
    data = src_file.read()
    src_hash = SHA256.new(data)

    try:
        public_file = open(public_key, "rb")
    except FileNotFoundError:
        print("No such file! Try again!")
        return
    key = RSA.import_key(public_file.read())
    cipher = pss.new(key)

    try:
        try:
            signature = open("keys/" + "signature" + ".sign", "rb").read()
        except FileNotFoundError:
            print("No such file! Try again!")
            return
        cipher.verify(src_hash, signature)
        print("The signature is authentic.")

    except (ValueError, TypeError):
        print("The signature is not authentic.")


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    signature_check(args.file, args.key)