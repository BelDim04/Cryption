from PIL import Image
from steganography_crypt import bits_for_crypt
import argparse


def get_characters(img_data, k):
    start = 2
    while True:
        character = 0
        for i in range(k):
            n = bits_for_crypt(k, i)
            character = character << n
            character += (img_data[start + i] % (1 << n))
        start += k
        if character == 0:
            return
        yield character


def decrypt_steganography(image_name):
    image = Image.open(image_name, 'r')
    img_data = [num for pixel in iter(image.getdata()) for num in pixel]

    k = ((img_data[0] << 4) % 256) + (img_data[1] % (1 << 4))

    byte_str = bytes(get_characters(img_data, k))

    print(byte_str.decode('utf-8'))


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', required=True)

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    decrypt_steganography(namespace.in_file)
