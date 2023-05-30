# Name:       Main Module   
# Purpose:    SUFI2 Calibration  
#
# Author:     Elham Soleimanian
#
# Created:     04/17/2021
# -------------------------------------------------------------------------
# Import Libraries 
import numpy as np
import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt
# -------------------------------------------------------------------------
# Import Developed Madules 
import LatinSampling 
import MassBalance
import SUFI2
# ------------------------------------------------------------------------
# chizaeii k dar madol haye mokhtaled niaz hast ro to main vared mikonim mesle parameter ha ya matris nemone giri
# Number of Sampling in Each Round(it Should be Between 1000-2000) 
nos = 1200
# Number of Parameters
nop = 8
# Number of SUFI2 Rounds 
rounds = 6

# Number of Observation Station
noo = 2
timeStep=120
pfactor_desired = 0.7
dfactor_desired = 3 

# Import Observation Data for TDS 
Data  = pd.ExcelFile(r'D:\My Code New\DataforSalinatary\ObservedTDS.xlsx')
observation  = pd.read_excel(Data, 'Sheet1',usecols='B:C').to_numpy()
observation = observation.astype('float')
# observation[observation == 0] = np.nan
# Import Weights of Stations 
w = pd.read_excel(Data, 'Weights',usecols='B:C').to_numpy()

# Import Guessed Boundries for All Parametes 
Data2  = pd.ExcelFile(r'D:\My Code New\DataforSalinatary\CalibrationParameters.xlsx')
lb= pd.read_excel(Data2, 'Sheet1',usecols='B:I').to_numpy()         
ub= pd.read_excel(Data2, 'Sheet2',usecols='B:I').to_numpy() 
labsb = pd.read_excel(Data2, 'Sheet3',usecols='B:I').to_numpy()
uabsb = pd.read_excel(Data2, 'Sheet4',usecols='B:I').to_numpy() 

# Call Every thing Which is Needed in each SUFI2 Round
for eachround in range(rounds):
    # Create sampling Matrix for each round
    samplingmatrix = LatinSampling.PUTBETWEENBOUNDS(LatinSampling.LHSSAMPLING(nop, nos),lb,ub)
    
    
    # Simulate WSMN for Each Number of simulation and Get Simulated Discharge, Reservoir Interflow
    
    
    # TDS routing simulation(Call TDS Routing Function)
    objectivefunc,objective_functionW,objective_functionWS, varf, xstar,c,tdssimulated,CqInter = MassBalance.find_mass(timeStep,nos, samplingmatrix,observation,w)
    
    # Sufi-2 calibration process 
    pfactor, dfactor, cl, cu, bjmin, bjmax, best = SUFI2.sufi2(objective_functionWS,samplingmatrix,varf,xstar,observation,tdssimulated,lb, ub, labsb, uabsb,nos, nop,noo,timeStep)
                                                                
                                                                
    lb, ub=bjmin, bjmax                                                      
                                                              
                                                             
   
                       
    if (np.float(pfactor.mean()) > pfactor_desired) & (np.float(dfactor.mean()) < dfactor_desired):
        break