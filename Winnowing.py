import hashlib
import re
import sys
from cryptography.fernet import Fernet


def winnow_setup(text, k, w):
    text = text.lower()
    text = re.sub(r'\W+', '', text)
    grams = []
    for i in range(0, len(text)-k+1):
        grams.append(text[i:i+k])
    hashes = []
    for gram in grams:
        hashes.append(int(hashlib.md5(gram.encode('UTF-8')).hexdigest(), 16))
    return winnow(w, hashes)


# Algorithm taken from 'Winnowing: Local Algorithms for Document Fingerprinting'
def winnow(w, hashes):
    recorded = {}
    h2 = hashes.copy()
    h = [sys.maxsize for i in range(0, w)]
    r = 0
    minimum = 0
    global_pos = 0
    for i in range(0, len(hashes)-1):
        r = (r + 1) % w
        h[r] = h2.pop(0)
        if minimum == r:
            for ind in scan_left_ind(r, w):
                if h[ind] < h[minimum]:
                    minimum = ind
            recorded = record(recorded, h[minimum], global_pos, w)
        else:
            if h[r] <= h[minimum]:
                minimum = r
                recorded = record(recorded, h[minimum], global_pos, w)
        global_pos += 1
    return recorded


def record(recorded, minimum, global_pos, w):
    if global_pos < w and len(recorded) > 0:
        for rec in recorded:
            if minimum <= rec:
                recorded.pop(rec)
                recorded[minimum] = global_pos
    else:
        recorded[minimum] = global_pos
    return recorded


def scan_left_ind(r, w):
    inds = []
    step = (r - 1) % w
    for i in range(0,4):
        inds.append(step)
        step = (step - 1 + w) % w
    return inds


def compare_documents(file1, file2):
    f = open(file1, "r")
    txt = f.read()
    fingerprints1 = winnow_setup(txt, 10, 4)

    f2 = open(file2, "r")
    txt2 = f2.read()
    fingerprints2 = winnow_setup(txt2, 10, 4)

    common = []
    for fp in list(fingerprints1.keys()):
        if fp in list(fingerprints2.keys()):
            common.append(fp)
    print("The documents have %d fingerprint(s) in common." % len(common))


def main():
    compare_documents("test.txt", "test2.txt")


if __name__ == "__main__":
    main()
