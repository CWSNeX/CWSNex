# -------------------------------------------------------------------------
# Name:        Evaporation from water body
# Purpose:     This madule calculate evaporation from rivers and reserviors
#
# Author:      Elham Soleimanian
#
# Created:     12/26/2020
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#-------------------------------------------------------------------------
# Import Weather Station Data 

data = pd.ExcelFile(r'D:\My Code New\DataBank\WeatherStation.xlsx')
Wvelocity =  pd.read_excel(data, 'windvelocity',usecols='B').to_numpy()
Ssp =  pd.read_excel(data, 'saturatedsteampressure',usecols='B').to_numpy()
Sp =  pd.read_excel(data, 'steampressure',usecols='B').to_numpy()
Sradiation=  pd.read_excel(data, 'solarradiation',usecols='B').to_numpy()
Temp=  pd.read_excel(data, 'avetemprature',usecols='B').to_numpy()
data = pd.ExcelFile(r'D:\My Code New\DataBank\EvaporationConstant.xlsx')
# Calibration Parameter
c = pd.read_excel(data, 'Sheet1',usecols='A').to_numpy()
[m,uE] = Wvelocity.shape
#------------------------------------------------------------------------
# Import time step 
t = np.linspace(0,120,120)
#------------------------------------------------------------------------
# Preallocation Matrix
E = np.zeros((m,uE)) 
############# ***** Following Function can calculate Evaporation *****##############
# This function is based on Mayer Method to calculate evaporation(Unit mm/day)
def MayerEvaporation(WVELOCITY,C,SSP,SP):
                    E = 0
                    E = (1+WVELOCITY/16) * C * (SSP - SP )
                    return E
                
# for i in range(0,uE):
#     for j in range(0,m):
#         E[j,i] = MayerEvaporation(Wvelocity[j,i],c,Ssp[j,i],Sp[j,i])
                
                
############# ***** Following Function can calculate Evaporation *****##############
# This function is based on Jensen Heiz Method to calculate evaporation( Unit mm/day)
def JensenEvaporation(SRADIATION,TEMPRATURE):
                     E = 0
                     E = SRADIATION *  (0.025 * TEMPRATURE + 0.08)
                     return E
                 
# for i in range(0,u):
#     for j in range(0,m):
#         E[j,i] = JensenEvaporation(Sradiation[j,i],Temp[j,i])


############# ***** Following Function can calculate Evaporation *****##############
# This function is based on Hamon  Method to calculate evaporation( Unit mm/day )
def Hamon(TEMPRATURE):
         E = 4.95 * 10**(-2) * np.exp(0.062 * TEMPRATURE)
         return E 
#---------------------------------------------------------------------------------   
# Run This Module       
# for i in range(0,uE):
#     for j in range(0,m):
#         E[j,i] = Hamon(Temp[j,i])
        
# plt.plot(t,E)
# plt.legend(["EvaInStation1", "EvaInStation2","EvaInStation3"], loc ="upper right") 
# plt.xlabel('time(month)')
# plt.ylabel('Evaporation(mm/day)')
# plt.show()
    

