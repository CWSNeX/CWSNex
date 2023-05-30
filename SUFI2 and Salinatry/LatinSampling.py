# Name:       Main Module   
# Purpose:    SUFI2 Calibration  
#
# Author:     Elham Soleimanian
#
# Created:     04/17/2021
# ----------------------------------------------------------------------------
# Import Libraries
import pyDOE
import numpy as np
from scipy.stats.distributions import uniform


def LHSSAMPLING(NOP,NOS):
    """
    :param nop: Number of parameters 
    :param nos: Number of simulations 
    """

    lhsmatrix = pyDOE.lhs(NOP,samples=NOS,criterion='corr',iterations=5)
                          
                          
    lhsmatrix = uniform(loc=0, scale=1).ppf(lhsmatrix)
    return lhsmatrix


def PUTBETWEENBOUNDS(MATRIX, LB, UB):
    """
    Creating a matrix of (nop * nos) which it's columns have sampled data
    fitted between their upper and lower bounds. Each rows indicates each
    sampling round.
    :param matrix: LHSSAMPLING returned matrix 
    :param lb:     Lower bound matrix 
    :param ub:     Upper bound matrix 
    :return:       fittedmatrix 
    """
    fittedmatrix = LB + (MATRIX * (UB - LB))
   
    return fittedmatrix

# Sampling Matrix is Changed in Each Simulation Round(SUFI2 Round)