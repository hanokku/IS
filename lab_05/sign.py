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
        help="source file"
    )
    return parser


def signature_sign(filename):
    try:
        src_file = open(filename, "rb")
    except FileNotFoundError:
        print("No such file! Try again!")
        return
    data = src_file.read()
    src_hash = SHA256.new(data)

    private_key = RSA.generate(2048)
    signature = pss.new(private_key).sign(src_hash)
    private_file = open("keys/pr_key.pem", "wb")
    private_file.write(private_key.export_key("PEM"))

    public_key = private_key.publickey()
    public_file = open("keys/pub_key.pem", "wb")
    public_file.write(public_key.exportKey("PEM"))
    public_file.close()

    sign_file = open("keys/" + "signature" + ".sign", "wb")
    sign_file.write(signature)
    sign_file.close()


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    signature_sign(args.file)