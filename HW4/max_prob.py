# -*- coding: utf-8 -*-
"""
Created on Mar 1
@author: sibelius seraphini
"""
from numpy import arange
import math

# The normalization factor is the same for all x and same function
def calc_normalization(fun):
    z_star = sum([math.exp(fun(xi))
                    for xi in arange(0, 1.01, 0.01)])
    return z_star

# Calculate a function of probability
def fun_prob(x, fun, z_star):
    return 1 / z_star * math.exp(fun(x))

# Maximize a function of probability
def max_fun_prob(fun_name, fun):
    z_star = calc_normalization(fun)
    probs = [[x, fun_prob(x, fun, z_star)] for x in arange(0, 1.01, 0.01)]
    [x, prob] = max(probs, key = lambda item: item[1])
    print fun_name,': ', x, prob

def main():
    # Define the function for the pr = 1 and pr = 2
    fun_pr1 = lambda x: -2.0 + 0.4 * x
    fun_pr2 = lambda x: -2.8*x*x + 2.4*x - 1.2

    max_fun_prob('pr1', fun_pr1)
    max_fun_prob('pr2', fun_pr2)

if __name__ == '__main__':
    main()


