import sys
import random
import string
from collections import defaultdict
from collections import Counter
from itertools import product


def Load(filename):
    data = ''
    fp = open(filename, 'r')
    return fp.read()


def Train(filename, order = 3, lid = 0.001):
    # make set of chars
    data = Load(filename)
    data = data.replace(' ', '_')
    chars = set([c for c in data])# if c != '\n'])
    #chars.add('*')
    data = string.lower(data)
    data = (order - 1) * '#' + data

    # set up ngram dictionary with no nonzero values
    ngram = {}
    count = 0
    pre = [''.join([x for x in p]) for p in product(chars, repeat = order - 1)]
    pre += (order - 1) * '#'
    for i in range(1, order):
        pre += [i * '#' +
            ''.join([x for x in p]) for p in product(chars, repeat = order - 1 - i)]
    
    for p in pre:
        ngram[p] = {x : lid for x in chars}
        count += len(chars)

    # count occurrences
    for i in range(len(data) - order - 1):
        sequence = data[i : i + order - 1]
        nextChar = data[i + order - 1]
        ngram[sequence][nextChar] += 1
    
    # calculate probabilities
    for seq, char_count in ngram.items():
         n = sum(char_count.values()) + count * lid
         for char, count in char_count.items():
             ngram[seq][char] = float(count) / n

    return ngram

    #model = {}
    #for seq, char_count in ngram.items():
    #    n = sum(char_count.values()) + count * lid
    #    if seq not in model:
    #        model[seq] = {}
    #    for char, count in char_count.items():
    #        model[seq][char] = float(count) / n
    #return model


def MakeFSA(ngram, order, startSymbol = '<s>'):
    fsa = 'F\n'
    for seq, char_prob in ngram.items():
        for char, prob in char_prob.items():
            # if all chars are start symbol
            if seq[-1] == '#':
                fsa += '(F ({0} {1} {2}))\n'.format(
                    seq + '_' + char, char, prob
                )
            else:
                fsa += '({0} ({1} {2} {3}))\n'.format(
                    seq, seq[1 :] + char, char, prob
                )
    return fsa

    


    
    #for seq, lp in ngram.items():
    #    for letter, prob in lp.items():
    #        fsa += '(s{0} ({1} {2} {3}))\n'.format(
    #            seq, seq,
    #        )


def generate_letter(ngram, history, order):
    history = history[-(order - 1) : ]
    dist = ngram[history]
    x = random.random()
    while True:
        for c, v in dist.items():
            x = x - v
            if x <= 0:
                return c


def generate_text(ngram, order = 3, nletters = 1000):
    history = '#' * (order - 1)
    out = []
    for i in xrange(nletters):
        c = generate_letter(ngram, history, order)
        history = history[-(order - 1) : ] + c
        out.append(c)
    return ''.join(out)


if __name__ == "__main__":
    order = int(sys.argv[2])
    filename = sys.argv[1]
    model = Train(filename, order)

    #for seq, char_prob in model.items():
    #    if seq.count('#') > 0:
    #        print seq + ' :'
    #        for c, p in char_prob.items():
    #            print '\t{0} / {1}'.format(c, p)

    #print generate_text(model, order)

    print MakeFSA(model, order)
