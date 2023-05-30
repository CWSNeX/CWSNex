# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 03:48:28 2020

@author: Elham Soleimanian
"""

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


 # Impoert Initial Hydrogeraph
Data  = pd.read_excel(r'D:\My Code New\DataBank\Hydrogheraph.xlsx')
qInitialInput = pd.DataFrame(Data,columns = ['Discharge1']).to_numpy()
[m,u] = qInitialInput.shape  
      
#------------------------------------------------------------------------------------
# Define Constants 
# Channel bottom width [meters]
b = 200
# Channel gradient (fraction, dy/dx)
s = 0.01 
# Channel Manning's n
n = 0.035
# Channel length [meters]
L = 24000
# kinematic wave parameter: 0.6 is for broad sheet flow
beta =  0.6
# number of substep per day
#------------------------------------------------------------------------------------
# Corresponding sub-timestep (min) and plac
dx = 3000
dt = 3*60
k = 8
tfinal = 120

        
        
#------------------------------------------------------------------------------------
#Define Predicted Matrix
y = np.zeros((m,k))
p = np.zeros((m,k))
qOut = np.zeros((m,k))
alpha = np.zeros((m,k))
t = np.linspace(0,120,41)      


#------------------------------------------------------------------------------------
# ***** CHANNEL ALPHA (KIN. WAVE)*****************************
# ************************************************************
# Following calculations are needed to calculate Alpha parameter in kinematic
# wave. Alpha currently fixed at half of bankful depth
# Update qInitial
    
for i in range(0,k):
    for j in range(0,m):
        if i == 0 and j>=0:
            qOut[j,0] = qInitialInput[j,0]
            y[j,i] = (( qOut[j,i]*n)/(1.49 * b * sqrt(s)))**(3/5)
            p[j,i]= b + 2 * y[j,i]
            alpha[j,i] = ((n * p[j,i]**(2/3))/sqrt(s))**beta
        elif j == 0 and i>0: 
            qOut[0,i]= 2000
            
        
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
            

for i in range(0,k-1):
    for j in range(0,m-1):
        
        qOut[j+1,i+1] = routing(alpha[j,i],beta,qOut[j+1,i],qOut[j,i+1],dx,dt)
        # Define QInitial which calulated from perevious place 
        if i >= 0:
            qOut[j+1,i+1] = qOut[j+1,i+1].copy()
            y[j,i+1] = (( qOut[j+1,i+1]*n)/(1.49 * b * sqrt(s)))**(3/5)
            p[j,i+1]= b + 2 * y[j,i+1]
            alpha[j,i+1] = ((n * p[j,i+1]**(2/3))/sqrt(s))**beta
        # Define QBoundary which calculated from perevious time
        if j >= 0: 
            qOut[j+1,i+1] = qOut[j+1,i+1].copy()
   




               
# Define How to Plot
plt.plot(t,qOut)
plt.legend(["Section1", "Section2","Section3","Section4","Section5"], loc ="upper left") 
plt.xlabel('time(min)')
plt.ylabel('qOut(CFC)')
plt.show()
               
                             
            

