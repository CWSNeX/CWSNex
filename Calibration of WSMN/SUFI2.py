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
        



def sufi2(OBJECTIVEFUNCTION, SAMPLINGMATRIX , VARF, XSTAR, OBSERVATION,OBSERVATIONHEAD,SIMULATEDDISCHARGE,SIMULATEDHEAD, LB, UB, LABSB, UABSB,NOS, NOP,NOOD,NOOH,TIMESTEP):
    
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
    # zOBJECTIVEFUNCTION1=OBJECTIVEFUNCTION
    # zSAMPLINGMATRIX1=SAMPLINGMATRIX
    # zVAR1=VARF
    # zXSTAR1=XSTAR
    # zOBSERVATION1=OBSERVATION
    # zSIMULATEDTDS1=SIMULATEDTDS
    # zLB1=SIMULATEDTDS
    # zUB1=UB
    # zLABSB1=LABSB
    # zUABSB1=UABSB
    # zNOS1=NOS
    # zNOP1=NOP
    # zNOO1=NOO
    # zTIMESTEP1=TIMESTEP


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

    # Main diagonal values of matrix 'c':
    diag = np.diag(c)

    # T-Stident value(can be calculated later for each degree of freedom): ???????????????
    t_student = t.ppf(0.975, NOS - NOP)

    # New bounds:
    sj = np.sqrt(diag)
    blower = (XSTAR - (t_student * sj))
    bupper = (XSTAR + (t_student * sj))

# Preallocation for Producing 95 ppu and calculation p and d factor
    DISCHARGEL = np.empty((TIMESTEP,NOOD))
    DISCHARGEU = np.empty((TIMESTEP,NOOD))
    DISCHARGEL[:],DISCHARGEU[:]=np.nan,np.nan #???????
    HEADL = np.empty((TIMESTEP,NOOH))
    HEADU =np.empty((TIMESTEP,NOOH))
    HEADL[:],HEADU[:]=np.nan,np.nan
    
# Each Simulation has one RMSE,Pfactor and dfactor
    NOOT = NOOD + NOOH
    pfactor = np.zeros(NOOT)
    average = np.zeros(NOOT)
    std = np.zeros(NOOT)
    dfactor= np.zeros(NOOT)

# Extract Non-Zero Observation
    for nooi in range(0,NOOD):
        # nonzero_indice = np.nonzero(OBSERVATION[:,nooi])[0].tolist() #????????
        # Create Upper and Lower Bound for 95 ppu
        # for month in nonzero_indice:
        for month in range(0,TIMESTEP):
            # Calculate Upper and Lower Bound for Each River 
            DISCHARGEL[month,nooi] = np.quantile(SIMULATEDDISCHARGE[:,month,nooi], 0.025) # matris TDS SImulated baraye har sarshakhe
            DISCHARGEU[month,nooi] = np.quantile(SIMULATEDDISCHARGE[:,month,nooi], 0.975)
            # repeat

        z = ((DISCHARGEL[:,nooi] <= OBSERVATION[:,nooi]) & (DISCHARGEU[:,nooi] >=OBSERVATION[:,nooi])).sum() 
        # pfactor[nooi] = z/np.count_nonzero(OBSERVATION[:,nooi]) 
        pfactor[nooi] = z/120
        
        std[nooi] = np.std(OBSERVATION[:,nooi], ddof=1) 

        average[nooi] = (DISCHARGEU[:,nooi] - DISCHARGEL[:,nooi]).mean()


        dfactor[nooi] = (average[nooi] / std[nooi])
        # Calculate all Process for Head 
    for nooi in range(0,NOOH):
        # nonzero_indice = np.nonzero(OBSERVATION[:,nooi])[0].tolist() #????????
        # Create Upper and Lower Bound for 95 ppu
        # for month in nonzero_indice:
        for month in range(0,TIMESTEP):
            # Calculate Upper and Lower Bound for Each River 
            HEADL[month,nooi] = np.quantile(SIMULATEDHEAD[:,month,nooi], 0.025) # matris TDS SImulated baraye har sarshakhe
            HEADU[month,nooi] = np.quantile(SIMULATEDHEAD[:,month,nooi], 0.975)
            # repeat

        z = ((HEADL[:,nooi] <= OBSERVATIONHEAD[:,nooi]) & (HEADU[:,nooi] >=OBSERVATIONHEAD[:,nooi])).sum() 
        # pfactor[NOOD+nooi] = z/np.count_nonzero(OBSERVATIONHEAD[:,nooi]) 
        pfactor[NOOD+nooi] = z/120
        
        std[NOOD+nooi] = np.std(OBSERVATIONHEAD[:,nooi], ddof=1) 

        average[NOOD+nooi] = (HEADU[:,nooi] - HEADL[:,nooi]).mean()


        dfactor[NOOD+nooi] = (average[NOOD+nooi] / std[NOOD+nooi])

    bjmin = blower - np.maximum((blower - LB[0,:]) / 2, (UB[0,:] - bupper) / 2)
    bjmax = bupper + np.maximum((blower - LB[0,:]) / 2, (UB[0,:] - bupper) / 2)

    bjmin=np.where(bjmin < LABSB, LABSB,bjmin)
    bjmax=np.where(bjmax > UABSB, UABSB, bjmax)
    best = (bjmin + bjmax) / 2


    return pfactor, dfactor, DISCHARGEL, DISCHARGEU,HEADL,HEADU ,bjmin, bjmax, best


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






