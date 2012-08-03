from random import random

def check_roll(prob):
    return random() <= prob

# choice stuff

def make_pdf_from_choices(choices):
    
    # create factors
    factors = []
    prev = choices[0][1]
    for c in choices[1:]:
        v = c[1]
        factors.append(float(v) / prev)
        prev = v

    def rec(factors, weight):
        if len(factors) == 0:
            return [1.0 / weight]
        else:
            pn = rec(factors[1:], weight * factors[0] + 1)
            pn.insert(0, factors[0] * pn[0])
            return pn

    probs = rec(factors, 1)
    pdf = []
    for n in zip(choices, probs):
        pdf.append((n[0][0], n[1]))

    return pdf

def make_cdf_from_pdf(pdf):
    sort = sorted(pdf, key = lambda a: a[1], reverse = True)
    cdf_total = 0
    cdf = []
    for v in sort:
        cdf_total += v[1]
        cdf.append((v[0], cdf_total))
    return cdf

class Choices ():
    def __init__(self, *args):
        self.weights = args
        self.cdf = make_cdf_from_pdf(make_pdf_from_choices(self.weights))

    def random_choice(self):
        choice = random()
        for c in self.cdf:
            if choice <= c[1]:
                return c[0]

    
