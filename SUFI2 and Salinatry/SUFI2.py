# Name:       SUFI2 Calibration Madule  
# Purpose:    Determine Optimum Values of Model 
#
# Author:      Hossein Akbari
#samplingmatrix
# Created:     04/17/2021
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import itertools as it
from scipy.stats import t
        



def sufi2(OBJECTIVEFUNCTION, SAMPLINGMATRIX , VARF, XSTAR, OBSERVATION,SIMULATEDTDS, LB, UB, LABSB, UABSB,NOS, NOP,NOO,TIMESTEP):
    
    """
    :param nop:
    :param nos:
    :param objectivefunction: List of objective functions calculated for each sampling round -> pd.DataFrame()
    :param samplingmatrix: Matrix of nos*nop calculated by LHS -> pd.DataFrame([], index=nos, columns=parameters)
    :param varf: Variance of objective function values -> np.float64
    :param xstar: The sampling round which has the smallest(depending on type of objective function)
                     -> pd.Series([], name=simulation step #)
    :param observation: Matrix of observed values red from an excel file-> pd.DataFrame()
    :param lb: Lower bound of parameters
    :param ub: Upper bound of parameters
    :param labsb: Lower absolute bound
    :param uabsb: Upper absolute bound
    :return: pfactor, dfactor, cl, cu, bjmin, bjmax -> pd.Series()
    """
    zOBJECTIVEFUNCTION1=OBJECTIVEFUNCTION
    zSAMPLINGMATRIX1=SAMPLINGMATRIX
    zVAR1=VARF
    zXSTAR1=XSTAR
    zOBSERVATION1=OBSERVATION
    zSIMULATEDTDS1=SIMULATEDTDS
    zLB1=SIMULATEDTDS
    zUB1=UB
    zLABSB1=LABSB
    zUABSB1=UABSB
    zNOS1=NOS
    zNOP1=NOP
    zNOO1=NOO
    zTIMESTEP1=TIMESTEP


    # Delta(g(i)) values: # tabe 1 n 
    of_comb_diffs = combs_diffs(OBJECTIVEFUNCTION)

    # Delta(b(j)) values: # tabe n m 
    s_comb_diffs = np.apply_along_axis(combs_diffs, 0, SAMPLINGMATRIX)
    
    # J matrix (Sensivity matrix): # tekrar rmse baraye hamkhani bod matris ha 
    rep_g = np.tile(of_comb_diffs, (NOP,1)).T
    j = rep_g/s_comb_diffs

    # Hessian matrix:
    h = (j.T).dot(j)

    # Cramer-Rao matrix: ////////???????????
    # cc = VARF * np.linalg.pinv(h)
    c = VARF * np.linalg.inv(h)
    
    
    
    zFFFFFFFFFFFF=np.dot(h,np.linalg.inv(h))
    # a=FFFFFFFFFFFFFFFF
    

    # a3 = np.array([[1., 2.], [3., 4.]])
    # # take a 3x3 matrix
    # A = [[12, 7, 3],
    #      [4, 5, 6],
    #      [7, 8, 9]]
  
    # # take a 3x4 matrix
    # B = [[5, 8, 1, 2],
    #      [6, 7, 3, 0],
    #      [4, 5, 9, 1]]
  
    # # result will be 3x4
  
    # result= [[0,0,0,0],
    #          [0,0,0,0],
    #          [0,0,0,0]]
    
    # result = np.dot(a3,np.linalg.inv(a3))
    # # result = np.dot(A,B)
  
    # for r in result:
    #     print(r)
    
    
    
    
    
    
    
    
    # Main diagonal values of matrix 'c':
    diag = np.diag(c)

    # T-Stident value(can be calculated later for each degree of freedom): ???????????????
    t_student = t.ppf(0.975, NOS - NOP)

    # New bounds:
    sj = np.sqrt(diag)
    blower = (XSTAR - (t_student * sj))
    bupper = (XSTAR + (t_student * sj))

# Preallocation for Producing 95 ppu and calculation p and d factor
    cl = np.empty((TIMESTEP,NOO))
    cu = np.empty((TIMESTEP,NOO))
    cl[:],cu[:]=0,0 #???????
    
# Each Simulation has one RMSE,Pfactor and dfactor
    pfactor = np.zeros(NOO)
    average = np.zeros(NOO)
    std = np.zeros(NOO)
    dfactor= np.zeros(NOO)

# Extract Non-Zero Observation
    for nooi in range(NOO):
        # nonzero_indice = np.nonzero(OBSERVATION[:,nooi])[0].tolist() #????????
        1==1
        # Create Upper and Lower Bound for 95 ppu
        for month in range(0,TIMESTEP):
        # for month in range(0,TIMESTEP):
            # Calculate Upper and Lower Bound for Each River 
            cl[month,nooi] = np.quantile(SIMULATEDTDS[:,month,nooi], 0.025) # matris TDS SImulated baraye har sarshakhe
            cu[month,nooi] = np.quantile(SIMULATEDTDS[:,month,nooi], 0.975)


        z = ((cl[:,nooi] <= OBSERVATION[:,nooi]) & (cu[:,nooi] >=OBSERVATION[:,nooi])).sum()
        pfactor[nooi] = z/TIMESTEP
        
        std[nooi] = np.std(OBSERVATION[:,nooi], ddof=1) 

        average[nooi] = (cu[:,nooi] - cl[:,nooi]).mean()


        dfactor[nooi] = (average[nooi] / std[nooi])

    bjmin = blower - np.maximum((blower - LB[0,:]) / 2, (UB[0,:] - bupper) / 2)
    bjmax = bupper + np.maximum((blower - LB[0,:]) / 2, (UB[0,:] - bupper) / 2)

    bjmin=np.where(bjmin < LABSB, LABSB,bjmin)
    bjmax=np.where(bjmax > UABSB, UABSB, bjmax)
    best = (bjmin + bjmax) / 2


    return pfactor, dfactor, cl, cu, bjmin, bjmax, best


def subtract(tup):
    return np.abs(tup[0] - tup[1])
# dektag momken khoroji mishavad delta g 
def combs_diffs(array):
    array1d = np.ndarray.flatten(array)
    rhdth=it.combinations(array1d, 2)    
    combs = list(it.combinations(array1d, 2)) # faghat tarkib mide g ha 
    diffs = np.array(list(map(subtract, combs))) 
    #diffs = combs.apply(subtract, convert_dtype=True)
    return diffs






