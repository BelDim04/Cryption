import argparse

from bs4 import UnicodeDammit

import crypt

FREQ = {
    u'A': 0.08167,
    u'B': 0.01492,
    u'C': 0.02782,
    u'D': 0.04253,
    u'E': 0.12702,
    u'F': 0.02228,
    u'G': 0.02015,
    u'H': 0.06094,
    u'I': 0.06966,
    u'J': 0.00153,
    u'K': 0.00772,
    u'L': 0.04025,
    u'M': 0.02406,
    u'N': 0.06749,
    u'O': 0.07507,
    u'P': 0.01929,
    u'Q': 0.00095,
    u'R': 0.05987,
    u'S': 0.06327,
    u'T': 0.09056,
    u'U': 0.02758,
    u'V': 0.00978,
    u'W': 0.0236,
    u'X': 0.0015,
    u'Y': 0.01974,
    u'Z': 0.00074,
    u'А': 0.080129951,
    u'Б': 0.0159356724,
    u'В': 0.045383383,
    u'Г': 0.0169507261,
    u'Д': 0.0297904325,
    u'Е': 0.0844924082,
    u'Ё': 0.0003660007,
    u'Ж': 0.0093948692,
    u'З': 0.0164861478,
    u'И': 0.0735317227,
    u'Й': 0.0120852219,
    u'К': 0.034938902,
    u'Л': 0.0439968978,
    u'М': 0.0320683219,
    u'Н': 0.0669722958,
    u'О': 0.109673692,
    u'П': 0.0281070725,
    u'Р': 0.0473350368,
    u'С': 0.054678117,
    u'Т': 0.0625827124,
    u'У': 0.0262152801,
    u'Ф': 0.0026436466,
    u'Х': 0.0097061107,
    u'Ц': 0.0048267702,
    u'Ч': 0.014448193,
    u'Ш': 0.0072807824,
    u'Щ': 0.0036069574,
    u'Ъ': 0.0003670377,
    u'Ы': 0.0189918277,
    u'Ь': 0.0173860861,
    u'Э': 0.0031866468,
    u'Ю': 0.0063742852,
    u'Я': 0.0200667924
}


def guess_cesar_key(filename):
    with open(filename, 'r') as rf:
        text = rf.read().upper()
        data = list(UnicodeDammit.detwingle(text))
    counts = {}
    EN = 0
    RUS = 0
    for i in range(len(data)):
        if 'A' <= data[i] <= 'Z':
            EN += 1
        else:
            RUS += 1
        if data[i] not in counts:
            counts[data[i]] = 0
        counts[data[i]] += 1
    EN /= len(data)
    RUS /= len(data)
    DIFF = 0
    KEY = 0
    for c in FREQ:
        if c not in counts:
            counts[c] = 0
        DIFF += abs(FREQ[c] - counts[c] / len(data))
    for k in range(1, 32):
        diff = 0
        for C in FREQ:
            c = crypt.chr_shift(C, k)
            if c not in counts:
                counts[c] = 0
            if 'A' <= C <= 'Z':
                diff += abs(FREQ[C] - counts[c] / len(data)) * EN
            else:
                diff += abs(FREQ[C] - counts[c] / len(data)) * RUS
        if diff < DIFF:
            KEY = k
            DIFF = diff
    return KEY


def guess_vigenere_key(filename):
    with open(filename, 'r') as rf:
        text = rf.read().upper()
        data = list(UnicodeDammit.detwingle(text))
    EN = 0
    RUS = 0
    for i in range(len(data)):
        if 'A' <= data[i] <= 'Z':
            EN += 1
        else:
            RUS += 1
    EN /= len(data)
    RUS /= len(data)
    CI = 0
    for c, l in FREQ.items():
        CI += l * l * EN if 'A' <= c <= 'Z' else l * l * RUS
    KL = None
    DIFF = 0.1 * CI

    for kl in range(1, len(data) + 1):
        counts = {}
        ci = 0
        for c in data[::kl]:
            if c not in counts:
                counts[c] = 0
            counts[c] += 1
        for c, l in counts.items():
            ci += l * l * EN if 'A' <= c <= 'Z' else l * l * RUS
        ci /= (len(data) // kl + 1) * (len(data) // kl + 1)
        if abs(CI - ci) < DIFF:
            KL = kl
            DIFF = abs(CI - ci)

    if KL is None:
        return 'A'

    KEY_EN = ''
    KEY_RUS = ''
    for r in range(KL):
        with open('decrypt_help_' + filename, 'w') as wf:
            wf.write(''.join(data[r::KL]))
        KEY_EN += chr(ord('A') + guess_cesar_key('decrypt_help_' + filename))
        KEY_RUS += chr(ord('А') + guess_cesar_key('decrypt_help_' + filename))
    with open('decrypt_help_' + filename, 'w') as wf:
        wf.write(KEY_EN + ' ' + KEY_RUS)
    return KEY_EN


def guess_key(filename, type):
    if type == 'cesar':
        return 'cesar', guess_cesar_key(filename)
    else:
        k = guess_vigenere_key(filename)

        if len(k) == 1:
            return 'cesar', ord(k) - ord('A')

        return 'vigenere', k


def decrypt(in_file, type=None, key=None, out_file=None):
    if key is None:
        type, key = guess_key(in_file, type)
    if type == 'cesar':
        crypt.cesar_crypt(in_file, key, out_file, False)
    else:
        crypt.vigenere_crypt(in_file, key, out_file, False)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', required=True)
    parser.add_argument('--type')
    parser.add_argument('--key')
    parser.add_argument('--out_file')

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    decrypt(namespace.in_file, namespace.type, namespace.key, namespace.out_file)