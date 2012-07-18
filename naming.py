from collections import defaultdict
from random import random, randint

def total_word(totals, word):
    prev = None
    for a in word.strip().lower():
        if prev:
            tot = totals[prev].get(a, 0)
            totals[prev][a] = tot + 1
        prev = a

def cdf_ify(d):
    cdf = {}
    for k1 in d:
        tot = 0
        for k2 in d[k1]:
            tot += d[k1][k2]
        pdf = []
        for k2 in d[k1]:
            pdf.append([k2, float(d[k1][k2]) / tot])
        pdf_2 = sorted(pdf, key=lambda a: a[1], reverse=True)
        tot = pdf_2[0][1]
        for p in pdf_2[1:]:
            tot += p[1]
            p[1] = tot
        cdf[k1] = pdf_2
    return cdf

def random_next(cdf, cur):
    r = random()
    for x in cdf[cur]:
        if r <= x[1]:
            return x[0]

def random_word(cdf, min=4, max=10):
    word = ''
    keys = cdf.keys()
    cur = keys[randint(0,len(keys)-1)]
    for i in range(randint(min,max)):
        a = random_next(cdf, cur)
        word += a
        cur = a
    return word

def read_from_file(file):
    import cPickle
    try:
        f = open(file)
    
        if file.endswith('.cdf'):
            cdf = cPickle.load(f)
        else:
            words = f.readlines()
            
            totals = defaultdict(dict)
    
            for word in words:
                total_word(totals, word)

            cdf = cdf_ify(totals)

            fout = open(file + '.cdf', 'w')
            cPickle.dump(cdf, fout)
            fout.close()
    finally:
        f.close()

    return cdf

if __name__ == '__main__':
    cdf = read_from_file('planet-name.cdf')
    
    for i in range(20):
        print random_word(cdf)
