import sys
import random
from collections import defaultdict
from collections import Counter


def Load(filename):
    data = ''
    fp = open(filename, 'r')
    return fp.read()


def Train(filename, order = 3, lid = 0.001):
    data = order * '#' + Load(filename)
    
    # count occurrences of each n-gram
    ngram = {}
    for i in range(len(data) - order):
        sequence = data[i : i + order]
        nextChar = data[i + order]
        if sequence not in ngram:
            ngram[sequence] = {nextChar : 1}
        else:
            if nextChar not in ngram[sequence]:
                ngram[sequence][nextChar] = 1
            else:
                ngram[sequence][nextChar] += 1
    
    # calculate probabilities
    model = {}
    for seq, char_count in ngram.items():
        n = sum(char_count.values())
        if seq not in model:
            model[seq] = {}
        for char, count in char_count.items():
            model[seq][char] = float(count) / n
    return model


def generate_letter(ngram, history, order):
    history = history[-order:]
    dist = ngram[history]
    x = random.random()
    while True:
        for c, v in dist.items():
            x = x - v
            if x <= 0:
                return c

def generate_text(ngram, order = 3, nletters = 1000):
    history = '#' * order
    out = []
    for i in xrange(nletters):
        c = generate_letter(ngram, history, order)
        history = history[-order:] + c
        out.append(c)
    return ''.join(out)



if __name__ == "__main__":
    order = int(sys.argv[2])
    filename = sys.argv[1]
    model = Train(filename, order)
    print generate_text(model, order)

