#-------------------------------------------------------------------------
# Name:        Mass Balance Method to Rout TDS in (Root Zone)
# Purpose:
#
# Author:     Hossein Akbari
#
# Created:     04/10/2021
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt
# -------------------------------------------------------------------------
# Import Data for Balance Method on Root Zone  and Return flow Node 
Data  = pd.ExcelFile(r'C:\0el\MassBalanceforFood\Data.xlsx')
rd = pd.read_excel(Data, 'RD',usecols='B:BX').to_numpy()
# In  soil moisture module use the syntax to write soil humidity in Data module
soilh = pd.read_excel(Data, 'SoilHumidity',usecols='B:BX').to_numpy()
# Link to water model and use Routed TDS( in  Mass Balance module in water system Routed Tds was written to Data Module)
cIrr = pd.read_excel(Data, 'CIrrigation',usecols='B:BX').to_numpy()
# Water Demand for Irrigation is calculated in food modle
Irr = pd.read_excel(Data, 'Inflitrated Irrigation',usecols='B:BX').to_numpy()
# Deep perculation is calculated in food modle
dp = pd.read_excel(Data, 'DeepPerculation',usecols='B:BX').to_numpy()
[m , n] = rd.shape
# -------------------------------------------------------------------------
# Preallocation 
csoil = np.zeros((m,n))
creturn = np.zeros((m,n))
################ Following Functions Route TDS in Root Zone  #################
def ROOTZONE(RD,SOILH1,SOILH2,CIRR,IRR,DP,CSOIL1):
             CSOIL = 0
             CSOIL = ((CIRR * IRR - CSOIL1 * DP )/RD + CSOIL1 * SOILH1)/SOILH2
             return CSOIL
         
            
def CRETURN(CIRR,SR,CSOIL,INT):
            CRETURN = 0
            CRETURN = (CIRR * SR + CSOIL * INT )/ (SR + INT)
            return CRETURN
        
for i in range(0,n):
    for j in range(0,m):
        if cIrr[0,i] == 5:
            csoil[0,i] = cIrr[0,i]
            csoil[j,i] = ROOTZONE(rd[j,i],soilh[j,i],soilh[j+1,i],cIrr[j,i],dp[j,i],csoil[j,i])
# ---------------------------------------------------------------------------
# Send cReturn to Water Module Based on the Location Which Return Flow Inter to River           
app = xw.App(visible=True)
wb = xw.Book(r'C:\0el\DataforSalinatary\NodesData.xlsx')
sht = wb.sheets['CReturnflow']
sht.range('B3').options(transpose=True).value = creturn[:,0]
sht.range('F3').options(transpose=True).value = creturn[:,1]
sht.range('BH3').options(transpose=True).value = creturn[:,2]
sht.range('BV3').options(transpose=True).value = creturn[:,3]
# ---------------------------------------------------------------------------         
# Assign Numbers to each section to recognize Root Zone Area or Return Flow Node
# Number 5 shows Root Zone Area 
# Number 6 Shows Agriculture Return FLow Node(Start point)
# Number 7 Shows Agriculture Return FLow Node(End point)
# ---------------------------------------------------------------------------