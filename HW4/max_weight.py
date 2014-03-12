# -*- coding: utf-8 -*-
"""
Created on Mar 1
@author: sibelius seraphini
"""
import numpy as np
import math
from itertools import product

# The normalization factor is the same for all w and same function
def calc_zstar(fun, size):
    z_star = sum([math.exp(fun(wi))
                    for wi in product(np.arange(0,1.01, 0.01), repeat=size)
                        if sum(wi)==1])
    return z_star

# Calculate a function of probability
def fun_prob(w, fun, z_star):
    return 1 / z_star * math.exp(fun(w))

# Maximize a function of probability
def max_fun_prob(fun_name, fun):
    z_star = calc_zstar(fun, 3)

    # Generate the probabilities for all set of w that satisfaties
    # w1 + w2 + w3 == 1
    probs = np.array([[w, fun_prob(w, fun, z_star)]
                for w in product(np.arange(0, 1.01, 0.01), repeat=3)
                    if sum(w) == 1 ])
    [w, prob] = max(probs, key = lambda item: item[1])
    # List of weigths that maximize the function
    weights = probs[probs[:,1] == prob,0]
    print fun_name,': Max value:', prob
    print 'Possibly weighted values: '
    for w in weights:
        print w

def main():
    # Define the function for the pr = 1 and pr = 2
    fun_pr1 = lambda w: -2.0*w[0] - 2.0*w[1] - 4.0*w[2]
    fun_pr2 = lambda w: -4.0*w[0] - 4.0*w[1] - 8.0*w[2]

    max_fun_prob('pr1', fun_pr1)
    max_fun_prob('pr2', fun_pr2)

if __name__ == '__main__':
    main()


