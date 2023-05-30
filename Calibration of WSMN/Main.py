# Name:       Main Module   
# Purpose:    SUFI2 Calibration  and WSMN Run
#
# Author:     Elham Soleimanian
#
# Created:     05/1/2021
# -------------------------------------------------------------------------
# Import Libraries 
import numpy as np
import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt
# -------------------------------------------------------------------------
# Import Developed Madules 
import LatinSampling 
import WSMN02
import SUFI2
# -------------------------------------------------------------------------
# Import Fixed Parameters of SUFI2
# Number of Sampling in Each Round(it Should be Between 1000-2000) 
nos = 500
 

# Number of Parameters
nop = 46
# Number of SUFI2 Rounds 
rounds = 10
# Number of Observation Station
nood = 1
nooh = 4
pfactor_desired = 0.6
dfactor_desired = 3.5
# -------------------------------------------------------------------------
# Import time step in WSMN Model
timeStep = 120 
# -------------------------------------------------------------------------
# Import Observation Data for Discharge in River 
Data  = pd.ExcelFile(r'D:\My Code New\DataforCalibrationWSMN\ObservedDischargeinRiver.xlsx')
observation  = pd.read_excel(Data, 'Sheet1',usecols='B').to_numpy()
observation = observation.astype('float')
# observation[observation == 0] = np.nan
# -------------------------------------------------------------------------
# Import Observation Head in each part of groundwater
Data1  = pd.ExcelFile(r'D:\My Code New\DataforCalibrationWSMN\ObservedHead.xlsx')
observationhead  = pd.read_excel(Data1, 'Sheet1',usecols='B:E').to_numpy()
observationhead = observationhead.astype('float')
# observationhead[observationhead == 0] = np.nan
# -------------------------------------------------------------------------
# Import Weights of  Observation Stations 
w = pd.read_excel(Data, 'Weights',usecols='B:F').to_numpy()
# -------------------------------------------------------------------------
# Import Guessed Boundries for All Parametes 
Data2  = pd.ExcelFile(r'D:\My Code New\DataforCalibrationWSMN\CalibrationParameters.xlsx')       
lb= pd.read_excel(Data2, 'Sheet1',usecols='B:AU').to_numpy() 
ub= pd.read_excel(Data2, 'Sheet2',usecols='B:AU').to_numpy() 
labsb = pd.read_excel(Data2, 'Sheet3',usecols='B:AU').to_numpy()
uabsb = pd.read_excel(Data2, 'Sheet4',usecols='B:AU').to_numpy() 
# -------------------------------------------------------------------------


# Call Every thing Which is Needed in each SUFI2 Round
for eachround in range(rounds):
    # Create sampling Matrix for each round
    samplingmatrix = LatinSampling.PUTBETWEENBOUNDS(LatinSampling.LHSSAMPLING(nop, nos),lb,ub,nop,nos)
    samplingmatrix
    
    # WSMN Model 
    objectivefunc,objective_functionW,objective_functionWS, varf, xstar,qOutFinall,dischargesimulated,headsimulated,samplingmatrix = WSMN02.WSMN(timeStep,nos,nop, samplingmatrix,observation,observationhead,w)
    
    # Sufi-2 calibration process 
    pfactor, dfactor, DischargeL, DischargeU,HeadL,HeadU, bjmin, bjmax, best = SUFI2.sufi2(objective_functionWS,samplingmatrix,varf,xstar,observation,observationhead,dischargesimulated,headsimulated,lb, ub, labsb, uabsb,nos, nop,nood,nooh,timeStep)
                                                                
                                                                
    lb, ub=bjmin, bjmax                                                      
                                                              
                                                             
   
                       
    if (np.float(pfactor.mean()) > pfactor_desired) & (np.float(dfactor.mean()) < dfactor_desired):
        break
    
    
