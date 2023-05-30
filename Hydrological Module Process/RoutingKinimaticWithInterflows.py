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
import matplotlib.pyplot as plt
from math import sqrt
#--------------------------------------------------------------------------
# Impoert Initial Hydrogeraph for Main River
Data  = pd.read_excel(r'D:\My Code New\DataBank\Hydrogheraph.xlsx')
qInitialInput = pd.DataFrame(Data,columns = ['Discharge1']).to_numpy()
[m,u] = qInitialInput.shape  
#--------------------------------------------------------------------------
# Import  Routed Interflows 
Data1 = pd.ExcelFile(r'D:\My Code New\DataBank\RoutedInterflow.xlsx')
qInter = pd.read_excel(Data1, 'Sheet1',usecols='B:I').to_numpy()
#--------------------------------------------------------------------------
# Define Constants for Coding
# K is the Number  of dx (sections) in this module dx is equal to disInterflow
k = 4
# -------------------------------------------------------------------------
# Where we have Interflow in watershed
disInter = [50,600,1000,1500]
#--------------------------------------------------------------------------
# Corresponding sub-timestep (min) and place
dt = 3*60
tfinal = 120
#--------------------------------------------------------------------------------------------------
# Define Main River Constants 
# River bottom width [meters]
b = 200
# River gradient (fraction, dy/dx)
s = 0.01 
# River Manning's n
n = 0.035
# River length [meters]
L_MainRiver = 24000
# kinematic wave parameter: 0.6 is for broad sheet flow
beta =  0.6      
#--------------------------------------------------------------------------------------------------
# Prealocation
y = np.zeros((m,k))
p = np.zeros((m,k))
alpha = np.zeros((m,k))
# routed discharge on main river 
qOut = np.zeros((m,k))
dx = [50,600,1000,1500]
t = np.linspace(0,120,41)      
#--------------------------------------------------------------------------------------------------

# ***** CHANNEL ALPHA (KIN. WAVE)*****************************
# ************************************************************
# Following calculations are needed to calculate Alpha parameter in kinematic wave. 
    
for i in range(0,k):
    for j in range(0,m):
        if i == 0 and j>=0:
            qOut[j,0] = qInitialInput[j,0]
            y[j,i] = (( qOut[j,i]*n)/(1.49 * b * sqrt(s)))**(3/5)
            p[j,i]= b + 2 * y[j,i]
            alpha[j,i] = ((n * p[j,i]**(2/3))/sqrt(s))**beta
        elif j == 0 and i>0: 
            qOut[0,i]= 2000
            
# Following def calculate routed discharge using try and error method     
def routing(ALPHA,BETA,QINITIAL,QBOUNDARY,DX,DT):
            q= 0
            deltaq = 1
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
                telp = F     
            return q
            
# Following def update discharge where there is Interflow       
def interflow(QOUT,QINTER):
    
             q = QOUT + QINTER
             return q

#------------------------------------------------------------------                   
# following loop is used to calculate routed discharge for each i,j            
for i in range(0,k-1):    
    for j in range(0,m-1):
        # Update qOut respect to new Interflow
        qOut[j+1,i] = interflow(qOut[j+1,i],qInter[j,i])
        qOut[j+1,i+1] = routing(alpha[j,i],beta,qOut[j+1,i],qOut[j,i+1],dx[i],dt)
            
        # y[j,i+1] = (( qOut[j+1,i+1]*n)/(1.49 * b * sqrt(s)))**(3/5)
        # p[j,i+1]= b + 2 * y[j,i+1]
        # alpha[j,i+1] = ((n * p[j,i+1]**(2/3))/sqrt(s))**beta
          
        if i >= 0:
            qOut[j+1,i+1] = qOut[j+1,i+1].copy()
            y[j,i+1] = (( qOut[j+1,i+1]*n)/(1.49 * b * sqrt(s)))**(3/5)
            p[j,i+1]= b + 2 * y[j,i+1]
            alpha[j,i+1] = ((n * p[j,i+1]**(2/3))/sqrt(s))**beta
        if j >= 0:
            qOut[j+1,i+1] = qOut[j+1,i+1].copy()
        

plt.plot(t,qOut)
plt.legend(["Section1", "Section2","Section3","Section4","Section5"], loc ="upper right") 
plt.xlabel('time(min)')
plt.ylabel('qOut(CFC)')
plt.show()
               
                             
            












 
























        
     
    
