# -------------------------------------------------------------------------
# Name:        Surface Water Allocation
# Purpose:     This madule allocate Water to variaty of Consumers
#
# Author:      Elham Soleimanian
#
# Created:     05/09/2021
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import pandas as pd
from SurfaceWaterAllocationPercentage import * 
import matplotlib.pyplot as plt
# -------------------------------------------------------------------------
# Assumption for Priority of Allocation
# 1 is belonged to Enviorment and Domestic
# 2 is Belonged to Min Demand for Energy and Industrial
# 3 is belonged to AGriculture Area
#-------------------------------------------------------------------------
# Import Demands from Main River 
data = pd.ExcelFile(r'D:\My Code New\DataBank\AllocationDemand.xlsx')
DE =  pd.read_excel(data, 'EnviormentalDemand',usecols='B:AO').to_numpy()

EnergyDemandMin =  pd.read_excel(data, 'EnergyMinDemand',usecols='B:AO').to_numpy()
EnergyDemandMax =  pd.read_excel(data, 'EnergyMaxDemand',usecols='B:AO').to_numpy()
AgrDemand =  pd.read_excel(data, 'AgrMain',usecols='B:AO').to_numpy()
TD =  pd.read_excel(data, 'TotalDemandMain',usecols='B:AO').to_numpy()
[m,n] = TD.shape
# Import Reservior Release 
qResOut =  pd.read_excel(data, 'QresOutMain',usecols='F').to_numpy()
# Import Factor for Each User 
# agrfactor = pd.read_excel(data, 'AgrMainFactor',usecols='B:AO').to_numpy()
# -----------------------------------------------------------------------
# Import Demands from Interflow  
DEInter = pd.read_excel(data, 'EnviormentalDemandInt',usecols='B:BA').to_numpy()
EnergyDemandMinInt = pd.read_excel(data, 'EnergyDemandIntMin',usecols='B:BA').to_numpy()
EnergyDemandMaxInt = pd.read_excel(data, 'EnergyDemandIntMax',usecols='B:BA').to_numpy()
AgrInterflow = pd.read_excel(data, 'AgrInt',usecols='B:BA').to_numpy()
TDInter = pd.read_excel(data, 'TotalDemandInt',usecols='B:BA').to_numpy()
[mm,nn] = TDInter.shape


# Preallocation for Main River
qAllocationEnv = np.zeros((m,n))
qAllocationAgr = np.zeros((m,n))
qAllocationEnergy = np.zeros((m,n))
# 
# Preallocation for Interflows
qAllocationEnvInt = np.zeros((mm,nn))
qAllocationAgrInt = np.zeros((mm,nn))
qAllocationEnergyInt = np.zeros((mm,nn))
# Following Function Determine Amount of Water Which should be exisit on the River 
def ENVIORMENALLOCATION(QRESOUT,TOTALDEMAND,ENVIORMENTDEMAND,ENVPFINALL):
                        QALLOCATEDENV = 0
                        if QRESOUT < ENVIORMENTDEMAND:
                             QALLOCATEDENV = QRESOUT
                        if QRESOUT > ENVIORMENTDEMAND and QRESOUT < TOTALDEMAND:
                             QALLOCATEDENV = ENVIORMENTDEMAND
                        if QRESOUT > TOTALDEMAND:
                            QALLOCATEDENV = QRESOUT - TOTALDEMAND + ENVIORMENTDEMAND
                        return  QALLOCATEDENV * ENVPFINALL
                    
# 
def AGRICULTUREALLOCATION(QRESOUT,ENVIORMENTDEMAND,ENERGYDEMANDMIN,TOTALDEMAND,AGRDEMAND,AGRPFINALL):
                        QALLOCATEDAGR = 0 
                        if ENVIORMENTDEMAND + ENERGYDEMANDMIN > QRESOUT:
                             QALLOCATEDAGR = 0
                        if QRESOUT < TOTALDEMAND and QRESOUT > ENERGYDEMANDMIN + ENVIORMENTDEMAND:
                            MAGR = AGRDEMAND/(TOTALDEMAND - ENVIORMENTDEMAND - ENERGYDEMANDMIN)
                            QALLOCATEDAGR = MAGR * QRESOUT - MAGR * (ENERGYDEMANDMIN + ENVIORMENTDEMAND)
                        if QRESOUT > TOTALDEMAND :
                            QALLOCATEDAGR = AGRDEMAND
                        return  QALLOCATEDAGR * AGRPFINALL 
                    
                    
def ENERGYALLOCATION(QRESOUT,ENVIORMENTDEMAND,ENERGYDEMANDMIN,TOTALDEMAND,ENERGYDEMANDMAX,ENERGYPFINALL):
                    QALLOCATEDENERGY = 0 
                    if QRESOUT < ENERGYDEMANDMIN + ENVIORMENTDEMAND :
                        QALLOCATEDENERGY = 0
                    if  QRESOUT <= ENERGYDEMANDMIN + ENVIORMENTDEMAND and QRESOUT >= ENVIORMENTDEMAND:
                        QALLOCATEDENERGY = QRESOUT - ENVIORMENTDEMAND 
                    if QRESOUT < TOTALDEMAND and QRESOUT > ENVIORMENTDEMAND + ENERGYDEMANDMIN :
                        MENERGY = ( ENERGYDEMANDMAX - ENERGYDEMANDMIN)/(TOTALDEMAND-ENVIORMENTDEMAND-ENERGYDEMANDMIN)
                        QALLOCATEDENERGY =  MENERGY * QRESOUT -  MENERGY * (ENVIORMENTDEMAND + ENERGYDEMANDMIN) + ENERGYDEMANDMIN
                    if QRESOUT > TOTALDEMAND:
                        QALLOCATEDENERGY = ENERGYDEMANDMAX
                    return  QALLOCATEDENERGY * ENERGYPFINALL


# Call Functions for Main River 

for i in range(0,n):
    for j in range(0,m):
        qAllocationEnv[j,i] =  ENVIORMENALLOCATION(qResOut[j,0],TD[j,i],DE[j,i],EnvPFinall[j,0])
        qAllocationAgr[j,i] = AGRICULTUREALLOCATION(qResOut[j,0],DE[j,i],EnergyDemandMin[j,i],TD[j,i],AgrDemand[j,i],AgrPFinall[j,0])
        qAllocationEnergy[j,i] =  ENERGYALLOCATION(qResOut[j,0],DE[j,i],EnergyDemandMin[j,i],TD[j,i],EnergyDemandMax[j,i],EnergyPFinall[j,0])
    
       
# Call Functions for Interflows
# Should Define QresOut for Interflow
for i in range(0,nn):
    for j in range(0,mm):
        qAllocationEnvInt[j,i] =  ENVIORMENALLOCATION(qResOut[j,0],TDInter[j,i],DEInter[j,i],EnvPFinallInt[j,0])
        qAllocationAgrInt[j,i] = AGRICULTUREALLOCATION(qResOut[j,0],DEInter[j,i],EnergyDemandMinInt[j,i],TDInter[j,i],AgrInterflow[j,i],AgrPFinallInt[j,0])
        qAllocationEnergyInt[j,i] =  ENERGYALLOCATION(qResOut[j,0],DEInter[j,i],EnergyDemandMinInt[j,i],TDInter[j,i],EnergyDemandMaxInt[j,i],EnergyPFinallInt[j,0])
       
        
        
