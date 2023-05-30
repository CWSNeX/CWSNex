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
Wvelocity =  pd.read_excel(data, 'windvelocity',usecols='B:D').to_numpy()
Ssp =  pd.read_excel(data, 'saturatedsteampressure',usecols='B:D').to_numpy()
Sp =  pd.read_excel(data, 'steampressure',usecols='B:D').to_numpy()
Sradiation=  pd.read_excel(data, 'solarradiation',usecols='B:D').to_numpy()
Temp=  pd.read_excel(data, 'avetemprature',usecols='B:D').to_numpy()
[m,u] = Wvelocity.shape
#------------------------------------------------------------------------
# Import time step and C coefficient
t = np.linspace(0,120,41)
c = 0.4
#------------------------------------------------------------------------
# Preallocation Matrix
E = np.zeros((m,u))
############# ***** Following Function can calculate Evaporation *****##############
# This function is based on Mayer Method to calculate evaporation
def MayerEvaporation(WVELOCITY,C,SSP,SP):
                    E = 0
                    E = (1+WVELOCITY/16) * C * (SSP - SP )
                    return E
                
# for i in range(0,u):
#     for j in range(0,m):
#         E[j,i] = MayerEvaporation(Wvelocity[j,i],c,Ssp[j,i],Sp[j,i])
                
                
############# ***** Following Function can calculate Evaporation *****##############
# This function is based on Jensen Heiz Method to calculate evaporation
def JensenEvaporation(SRADIATION,TEMPRATURE):
                     E = 0
                     E = SRADIATION *  (0.025 * TEMPRATURE + 0.08)
                     return E
                 
for i in range(0,u):
    for j in range(0,m):
        E[j,i] = JensenEvaporation(Sradiation[j,i],Temp[j,i])
print(__name__)
if __name__ == '__main__':
    
    print("Khar")


                
plt.plot(t,E)
plt.legend(["EvaInStation1", "EvaInStation2","EvaInStation3"], loc ="upper right") 
plt.xlabel('time(min)')
plt.ylabel('Evaporation(mm/day)')
plt.show()
    

