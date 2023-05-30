# -------------------------------------------------------------------------
# Name:        Routing module - Kinematic wave
# Purpose:
#
# Author:      Elham Soleimanian
#
# Created:     10/19/2020
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt
from math import sqrt


# Impoert Initial Hydrogeraph
Data  = pd.read_excel(r'D:\My Code New\DataBank\Hydrogheraph.xlsx')
qInitialInput = pd.DataFrame(Data,columns = ['Discharge1']).to_numpy()
[m,u] = qInitialInput.shape  
#------------------------------------------------------------------------------------
# Define Constants 
Data  = pd.read_excel(r'D:\My Code New\DataBank\MainRiverInformation.xlsx')
n = pd.DataFrame(Data,columns = ['ManingCoefficient']).to_numpy()
s = pd.DataFrame(Data,columns = ['Slope']).to_numpy()
b = pd.DataFrame(Data,columns = ['Width']).to_numpy()
L = pd.DataFrame(Data,columns = ['RiverLength']).to_numpy()
      
# kinematic wave parameter: 0.6 is for broad sheet flow
beta =  0.6
# number of substep per day
#------------------------------------------------------------------------------------
# Corresponding sub-timestep (month) and place
dx = 1000
dt = 30*24 * 3600
kk = int(L/dx)
# salhaye 47 48 49 
tfinal = 36
#------------------------------------------------------------------------------------
# Preallocation
y = np.zeros((m,kk))
p = np.zeros((m,kk))
qOut = np.zeros((m,kk))
alpha = np.zeros((m,kk))
t = np.linspace(0,120,120)      


#------------------------------------------------------------------------------------
#***** CHANNEL ALPHA (KIN. WAVE)*****************************
#************************************************************
#Following calculations are needed to calculate Alpha parameter in kinematic
#wave. Alpha currently fixed at half of bankful depth
#Update qInitial
    
# for i in range(0,kk):
#     for j in range(0,m):
#         if i == 0 and j>=0:
#             qOut[j,0] = qInitialInput[j,0]
#             y[j,i] = (( qOut[j,i]*n)/( b * sqrt(s)))**(3/5)
#             p[j,i]= b + 2 * y[j,i]
#             alpha[j,i] = ((n * p[j,i]**(2/3))/sqrt(s))**beta
#         elif j == 0 and i>0: 
#             qOut[0,i]= 0.5
#             y[j,i] = (( qOut[j,i]*n)/( b * sqrt(s)))**(3/5)
#             p[j,i]= b + 2 * y[j,i]
#             alpha[j,i] = ((n * p[j,i]**(2/3))/sqrt(s))**beta
            
        
def routing(ALPHA,BETA,QINITIAL,QBOUNDARY,DX,DT):
            detafact=2
            q=np.min(QINITIAL+QBOUNDARY)
            deltaq = np.min(QINITIAL+QBOUNDARY)/detafact
            telp = 0
            tolerance = 0.000001
            
            while True:
                F = (DT/DX)* q + ALPHA* (q**BETA)- ( (DT/DX)* QINITIAL + ALPHA * (QBOUNDARY** BETA) )
                if abs(F) < tolerance:
                    break
                elif F>0 and telp>=0:
                    q = q - deltaq
                elif F<0 and telp<=0:
                    q = q + deltaq
                elif F>0 and telp<=0:
                    deltaq = deltaq/2
                    q = q - deltaq
                elif F<0 and telp>=0:
                    deltaq = deltaq/2
                    q = q  + deltaq
                if q<0 :
                    q=0
                    telp=0
                    deltaq = deltaq/detafact
                telp = F
                    
            return q
            

# for i in range(0,kk-1):
#     for j in range(0,m-1):
        
#         qOut[j+1,i+1] = routing(alpha[j,i],beta,qOut[j+1,i],qOut[j,i+1],dx,dt)
        
#         y[j,i+1] = (( qOut[j+1,i+1]*n)/(1.49 * b * sqrt(s)))**(3/5)
#         p[j,i+1]= b + 2 * y[j,i+1]
#         alpha[j,i+1] = ((n * p[j,i+1]**(2/3))/sqrt(s))**beta#         
             

# Pass River Discharge to Reservior Module as QRESIN to Run 2D Model
# app = xw.App(visible=True)
# wb = xw.Book('D:\My Code New\DataBank\QRESIN.xlsx')
# wb1 = xw.Book('D:\My Code New\DataBank\WaterLevel.xlsx')
# sht = wb.sheets['Sheet1']
# sht1 = wb1.sheets['Sheet1']
# sht.range('B2').clear()
# sht.range('B2').options(transpose=True).value = qOut[:,2]

# sht1.range('B2').clear()
# sht1.range('B2').options(transpose=True).value = y[:,7] + 1410

# sht1.range('C2').clear()
# sht1.range('C2').options(transpose=True).value = y[:,24] + 1296

# sht1.range('D2').clear()
# sht1.range('D2').options(transpose=True).value = y[:,31] + 1314

# sht1.range('E2').clear()
# sht1.range('E2').options(transpose=True).value = y[:,38] + 1278
# app.kill()


               
# Define How to Plot
# plt.plot(t,qOut)
# plt.legend(["Section1", "Section2","Section3","Section4","Section5"], loc ="upper left") 
# plt.xlabel('time(month)')
# plt.ylabel('qOut(m3/s)')
# plt.show()
               
                             
            

