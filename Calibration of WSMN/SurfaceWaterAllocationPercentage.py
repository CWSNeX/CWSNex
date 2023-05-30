# -------------------------------------------------------------------------
# Name:        Surface Water Allocation Percentage
# Purpose:     This madule allocate Water to variaty of Consumer
#
# Author:      Elham Soleimanian
#
# Created:     05/26/2021
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
# -------------------------------------------------------------------------
# Assumption for Priority of Allocation
# 1 is belonged to Enviorment 
# 2 is Belonged to Min Demand for Energy
# 3 is belonged to AGriculture Area
#-------------------------------------------------------------------------
# Import Demands from Main River 
data = pd.ExcelFile(r'D:\My Code New\DataBank\AllocationDemandPercentage.xlsx')
DEP =  pd.read_excel(data, 'EnviormentalDemandP',usecols='B').to_numpy()
EnergyDemandMinP =  pd.read_excel(data, 'EnergyMinDemandP',usecols='B').to_numpy()
EnergyDemandMaxP =  pd.read_excel(data, 'EnergyMaxDemandP',usecols='B').to_numpy()
AgrDemandP =  pd.read_excel(data, 'AgrMainP',usecols='B').to_numpy()
TDP =  pd.read_excel(data, 'TotalDemandMainP',usecols='B').to_numpy()
[m,n] = TDP.shape
# Import Reservior Release 
qResOutP =  pd.read_excel(data, 'QresOutMainP',usecols='B').to_numpy()
timestep = 120
# -----------------------------------------------------------------------
# Import Demands from Interflow  
data = pd.ExcelFile(r'D:\My Code New\DataBank\AllocationDemandPercentage.xlsx')
DEInterP = pd.read_excel(data, 'EnviormentalDemandPInt',usecols='B').to_numpy()
EnergyDemandMinIntP = pd.read_excel(data, 'EnergyMinDemandPInt',usecols='B').to_numpy()
EnergyDemandMaxIntP = pd.read_excel(data, 'EnergyMaxDemandPInt',usecols='B').to_numpy()
AgrInterflowP = pd.read_excel(data, 'AgrMainPInt',usecols='B').to_numpy()
TDInterP = pd.read_excel(data, 'TotalDemandMainPInt',usecols='B').to_numpy()
[mm,nn] = TDInterP.shape
# -----------------------------------------------------------------------
# Preallocation for Main River 
qAllocationEnvP = np.zeros((m,n))
qAllocationAgrP = np.zeros((m,n))
qAllocationEnergyP = np.zeros((m,n))
qAllocationAll = np.zeros((m,n))
# ------------------------------------------------------------------------
# Preallocation for Interflow
qAllocationEnvPInt = np.zeros((mm,nn))
qAllocationAgrPInt = np.zeros((mm,nn))
qAllocationEnergyPInt = np.zeros((mm,nn))
qAllocationAllInt = np.zeros((mm,nn))
# --------------------------------------------------------------------------
# Following Fucnction Determine Amount of Water Which should be exisit on the River 
def ENVIORMENALLOCATION(QRESOUT,TOTALDEMAND,ENVIORMENTDEMAND):
                        QALLOCATEDENV = 0
                        if QRESOUT < ENVIORMENTDEMAND:
                             QALLOCATEDENV = QRESOUT
                        if QRESOUT > ENVIORMENTDEMAND and QRESOUT < TOTALDEMAND:
                             QALLOCATEDENV = ENVIORMENTDEMAND
                        if QRESOUT > TOTALDEMAND:
                            QALLOCATEDENV = QRESOUT - TOTALDEMAND + ENVIORMENTDEMAND
                         
                        return  QALLOCATEDENV
                    
# 
def AGRICULTUREALLOCATION(QRESOUT,ENVIORMENTDEMAND,ENERGYDEMANDMIN,TOTALDEMAND,AGRDEMAND):
                        QALLOCATEDAGR = 0 
                        if ENVIORMENTDEMAND + ENERGYDEMANDMIN > QRESOUT:
                             QALLOCATEDAGR = 0
                        if QRESOUT < TOTALDEMAND and QRESOUT > ENERGYDEMANDMIN + ENVIORMENTDEMAND:
                            MAGR = AGRDEMAND/(TOTALDEMAND - ENVIORMENTDEMAND - ENERGYDEMANDMIN)
                            QALLOCATEDAGR = MAGR * QRESOUT - MAGR * (ENERGYDEMANDMIN + ENVIORMENTDEMAND)
                        if QRESOUT > TOTALDEMAND :
                            QALLOCATEDAGR = AGRDEMAND
                        return  QALLOCATEDAGR
                    
                    
def ENERGYALLOCATION(QRESOUT,ENVIORMENTDEMAND,ENERGYDEMANDMIN,TOTALDEMAND,ENERGYDEMANDMAX):
                    QALLOCATEDENERGY = 0 
                    if QRESOUT < ENERGYDEMANDMIN + ENVIORMENTDEMAND :
                        QALLOCATEDENERGY = 0
                    if  QRESOUT < ENERGYDEMANDMIN + ENVIORMENTDEMAND and QRESOUT > ENVIORMENTDEMAND:
                        QALLOCATEDENERGY = QRESOUT - ENVIORMENTDEMAND 
                    if QRESOUT < TOTALDEMAND and QRESOUT > ENVIORMENTDEMAND + ENERGYDEMANDMIN :
                        MENERGY = ( ENERGYDEMANDMAX - ENERGYDEMANDMIN)/(TOTALDEMAND-ENVIORMENTDEMAND-ENERGYDEMANDMIN)
                        QALLOCATEDENERGY =  MENERGY * QRESOUT -  MENERGY * (ENVIORMENTDEMAND + ENERGYDEMANDMIN) + ENERGYDEMANDMIN
                    if QRESOUT > TOTALDEMAND:
                        QALLOCATEDENERGY = ENERGYDEMANDMAX
                    return  QALLOCATEDENERGY


for i in range(0,n):
    for j in range(0,m):
        qAllocationEnvP[j,i] =  ENVIORMENALLOCATION(qResOutP[j,0],TDP[j,i],DEP[j,i])
        qAllocationEnergyP[j,i] =  ENERGYALLOCATION(qResOutP[j,0],DEP[j,i],EnergyDemandMinP[j,i],TDP[j,i],EnergyDemandMaxP[j,i])
        qAllocationAgrP[j,i] = AGRICULTUREALLOCATION(qResOutP[j,0],DEP[j,i],EnergyDemandMinP[j,i],TDP[j,i],AgrDemandP[j,i])
        qAllocationAll[j,i] = qAllocationEnvP[j,i] + qAllocationEnergyP[j,i] + qAllocationAgrP[j,i]  
        
        
# Detemine The Supplied Percentage of Each Demand in One Location to Use in 40 Section
EnvPFinall = qAllocationEnvP / qAllocationAll
EnergyPFinall = qAllocationEnergyP / qAllocationAll
AgrPFinall =  qAllocationAgrP / qAllocationAll  

for i in range(0,nn):
    for j in range(0,mm):
        qAllocationEnvPInt[j,i] =  ENVIORMENALLOCATION(qResOutP[j,0],TDInterP[j,i],DEInterP[j,i])
        qAllocationEnergyPInt[j,i] =  ENERGYALLOCATION(qResOutP[j,0],DEInterP[j,i],EnergyDemandMinIntP[j,i],TDInterP[j,i],EnergyDemandMaxIntP[j,i])
        qAllocationAgrPInt[j,i] = AGRICULTUREALLOCATION(qResOutP[j,0],DEInterP[j,i],EnergyDemandMinIntP[j,i],TDInterP[j,i],AgrInterflowP[j,i])
        qAllocationAllInt[j,i] = qAllocationEnvPInt[j,i] + qAllocationEnergyPInt[j,i] + qAllocationAgrPInt[j,i]       

EnvPFinallInt = qAllocationEnvPInt /qAllocationAllInt
EnergyPFinallInt = qAllocationEnergyPInt / qAllocationAllInt
AgrPFinallInt =  qAllocationAgrPInt / qAllocationAllInt


        
# Write Water Withdrawal to WSMN Module 
# FoodWRiver
# EnergyWRiver 
# FoodWRiverInt
# EnergyWRiverInt  