# CPE 449/CS 485
# Homework 1, Part 2: Encryption modes - ECB vs. CBC and Padding
# Michael Agnew

from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import argparse
import io

def main():
    parser = argparse.ArgumentParser() # create argument parsing object
    parser.add_argument('-i', '--input', required=True, help="input") # add input file arg
    parser.add_argument('-o', '--output', required=True, help="output") # add output file arg
    parser.add_argument('-k', '--key', required=True, help="Encryption key is 16 bytes for AES-128") # add key arg
    parser.add_argument('-m', '--mode', required=True, choices=['ECB', 'CBC'], help="Encryption mode (ECB or CBC)") # add encryption mode arg
    args = parser.parse_args() # parse arg boys

    if len(args.key) != 32:
        raise ValueError("Encryption key must be 16 bytes") # 32 digits or 16 bytes must be the length of the key

    img = Image.open(args.input)  # load file input into img variable

    key = args.key.encode('utf-8')  # Convert key to bytes
    if args.mode == 'ECB':
        algorithm = AES.MODE_ECB
        encryption = AES.new(key, algorithm) # ECB does not use IV
    elif args.mode == 'CBC':
        algorithm = AES.MODE_CBC
        iv = get_random_bytes(16)  # acquire a random initialization vector
        encryption = AES.new(key, algorithm, iv) # make encryption algorithm

    img_bytes = img.tobytes()  # Convert image to bytes
    padded_bytes = pad(img_bytes, AES.block_size)  # Pad image bytes

    cipherdata = encryption.encrypt(padded_bytes)  # Encrypt the padded bytes
    encrypted_img = Image.frombytes(img.mode, img.size, cipherdata)  # Change the padded bytes back into an image

    # Save and display the image
    encrypted_img.save(args.output)
    #encrypted_img.show()
    
if __name__ == "__main__":
    main()
