from bs4 import UnicodeDammit
import sys
import argparse

def chr_shift(c, key):
    if 'A' <= c <= 'Z':
        first = 'A'
        last = 'Z'
    elif 'a' <= c <= 'z':
        first = 'a'
        last = 'z'
    elif 'А' <= c <= 'Я':
        first = 'А'
        last = 'Я'
    elif 'а' <= c <= 'я':
        first = 'а'
        last = 'я'
    else:
        return c
    power = ord(last) - ord(first) + 1
    return chr((ord(c) - ord(first) + key) % power + ord(first))


def cesar_crypt(in_file, key, out_file=None, to_crypt=True):
    key = int(key)
    if not to_crypt:
        key *= -1
    with open(in_file, 'r') as rf:
        text = rf.read()
        data = list(UnicodeDammit.detwingle(text))
        for i in range(len(data)):
            data[i] = chr_shift(data[i], key)

    prefix = 'cesar_crypt_' if to_crypt else 'cesar_decrypt_'

    if out_file is None:
        out_file = prefix + in_file

    with open(out_file, 'w') as wf:
        wf.write(''.join(data))


def vigenere_crypt(in_file, key, out_file=None, to_crypt=True):
    with open(in_file, 'r') as rf:
        text = rf.read()
        data = list(UnicodeDammit.detwingle(text))
        key = key * (len(data) // len(key))
        key = key + key[:len(data) - len(key)]
        for i in range(len(data)):
            if 'A' <= key[i] <= 'Z':
                k = ord(key[i]) - ord('A')
            elif 'a' <= key[i] <= 'z':
                k = ord(key[i]) - ord('a')
            elif 'А' <= key[i] <= 'Я':
                k = ord(key[i]) - ord('А')
            elif 'а' <= key[i] <= 'я':
                k = ord(key[i]) - ord('а')

            if not to_crypt:
                k *= -1

            data[i] = chr_shift(data[i], k)

    prefix = 'vigenere_crypt_' if to_crypt else 'vigenere_decrypt_'

    if out_file is None:
        out_file = prefix + in_file

    with open(out_file, 'w') as wf:
        wf.write(''.join(data))


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', required=True)
    parser.add_argument('--type', required=True)
    parser.add_argument('--key', required=True)
    parser.add_argument('--out_file')

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    if namespace.type == 'cesar':
        cesar_crypt(namespace.in_file, namespace.key, namespace.out_file, True)
    elif namespace.type == 'vigenere':
        vigenere_crypt(namespace.in_file, namespace.key, namespace.out_file, True)
