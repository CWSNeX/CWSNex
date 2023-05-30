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
Data1  = pd.read_excel(r'D:\My Code New\DataBank\Guess.xlsx')
qInitialInput = pd.DataFrame(Data,columns = ['Discharge1']).to_numpy()
# qGuess = pd.DataFrame(Data1,columns = ['Discharge']).to_numpy()
qGuess = 2000
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
L = 2400
# kinematic wave parameter: 0.6 is for broad sheet flow
beta =  0.6
# number of substep per day
#------------------------------------------------------------------------------------
# Corresponding sub-timestep (min) and plac
k = 5
tfinal = 120
dx = 3000
dt = 3*60
dtRouting = 10 
        
        
#------------------------------------------------------------------------------------
#Define Predicted Matrix
y = np.zeros((m,k))
p = np.zeros((m,k))
qInitial = np.zeros((m,k))
qBoundary = np.zeros((m,k))
qOut = np.zeros((m,k))
alpha = np.zeros((m,k))
# qOut = np.zeros((m,k))
F = np.zeros((m,k))
# t = np.arange(0, tfinal, dt)
t = np.linspace(0,120,41)      


#------------------------------------------------------------------------------------
# ***** CHANNEL ALPHA (KIN. WAVE)*****************************
# ************************************************************
# Following calculations are needed to calculate Alpha parameter in kinematic
# wave. Alpha currently fixed at half of bankful depth
# Update qInitial
    
for i in range(0,k):
    for j in range(0,m-1):
        if i == 0 and j>=0:
            qInitial[j+1,0] = qInitialInput[j,0]
            y[j+1,i] = (( qInitial[j+1,i]*n)/(1.49 * b * sqrt(s)))**(3/5)
            p[j+1,i]= b + 2 * y[j,i]
            alpha[j+1,i] = ((n * p[j+1,i]**(2/3))/sqrt(s))**beta
        elif j == 0 and i>0:
            qBoundary[0,i]= 2000
            
        
def routing(ALPHA,BETA,QINITIAL,QBOUNDARY,DX,DT):
            q= 0
            deltaq = 1
            telp = 0
            tolerance = 0.01
            # print(ALPHA)
            # print(BETA)
            # print(QINITIAL)
            # print(QBOUNDARY)
            # print(DX)
            
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
        

        qOut[j+1,i+1] = routing(alpha[j+1,i],beta,qInitial[j+1,i],qBoundary[j,i+1],dx,dt)
        q1=qOut[j+1,i+1]
        qi=qInitial[j+1,i]
        qb=qBoundary[j,i+1]
        print(q1)
        print(qi)
        print(qb)
        1==1
        
        if i >= 0:
            qInitial[j+1,i+1] = qOut[j+1,i+1].copy()

            y[j+1,i+1] = (( qInitial[j+1,i+1]*n)/(1.49 * b * sqrt(s)))**(3/5)
            p[j+1,i+1]= b + 2 * y[j+1,i+1]
            alpha[j+1,i+1] = ((n * p[j+1,i+1]**(2/3))/sqrt(s))**beta
        if j >= 0: 
            qBoundary[j+1,i+1] = qOut[j+1,i+1].copy()
        if j==5:
            1==1
            
        1==1




               
# Define How to Plot
# x = np.linspace(dx , L-dx/2, k)

plt.plot(t,qOut )
plt.legend(["Section1", "Section2"], loc ="lower right") 
        

plt.xlabel('time')
plt.ylabel('qOut')
plt.show()
               
                             
            

