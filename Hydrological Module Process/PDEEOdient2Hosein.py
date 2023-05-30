
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
k = 10
# tfinal = 120
dx = 3000
dt =3 *60
# dtRouting = 3 
        
        
#------------------------------------------------------------------------------------
#Define Predicted Matrix
y = np.zeros((m,k))
p = np.zeros((m,k))
q = np.zeros((m,k))
alpha = np.zeros((m,k))
qOut = np.zeros((m,k))
qBoundary = np.zeros((m,k))
F = np.zeros((m,k))
II = np.zeros((m,k))
# t = np.arange(0, tfinal, dt)
t = np.linspace(0,120,41)      


#------------------------------------------------------------------------------------
# ***** CHANNEL ALPHA (KIN. WAVE)*****************************
# ************************************************************
# Following calculations are needed to calculate Alpha parameter in kinematic
# wave. Alpha currently fixed at half of bankful depth
  

tolerance = 1    


# Update q
for j in range(0,m):
    q[j,0] = qInitialInput[j,0]
for i in range(1,k):
    q[0,i] = 2000
    

for i in range(0,k-1):
    for j in range(0,m-1):
        q[j+1,i+1]= 0
        deltaq = 1000
        telp = 0
        while True:
            
            # qInitial = q[j+1,i].copy()
            # qBoundary= q[j,i+1].copy()
            
            y[j,i] = (( q[j+1,i+1] * n)/(1.49 * b * sqrt(s)))**(3/5)
            p[j,i] = b + 2 * y[j,i]
            alpha[j,i] = ((n * p[j,i]**(2/3))/sqrt(s))**beta      
            
            # dt=dx/(5*1.49*sqrt(s)*y[j,i]**(2/3)/3/n)
            
            # a = alpha[j,i]
            # II = q[j+1,i]
            # BB = q[j,i+1]
            # T = q[j+1,i+1]
            Right = (dt/dx)*q[j+1,i]+alpha[j,i]*q[j,i+1]**beta
            LEFT = (dt/dx)*q[j+1,i+1]+alpha[j,i]*q[j+1,i+1]**beta
            tel = (dt/dx)*q[j+1,i+1]+alpha[j,i]*q[j+1,i+1]**beta-( (dt/dx)*q[j+1,i]+alpha[j,i]*q[j,i+1]**beta )

            if abs(tel) < tolerance:
                # print(a)
                # print(II)
                # print(BB)
                # print(T)
                # print(Right)
                # print(LEFT)
                break
            elif tel>0 and telp>=0:
                q[j+1,i+1]=q[j+1,i+1]-deltaq
            elif tel<0 and telp<=0:
                q[j+1,i+1]=q[j+1,i+1]+deltaq
            elif tel>0 and telp<=0:
                deltaq=deltaq/2
                q[j+1,i+1]=q[j+1,i+1]-deltaq
            elif tel<0 and telp>=0:
                deltaq=deltaq/2
                q[j+1,i+1]=q[j+1,i+1]+deltaq
            telp=tel     
            
plt.plot(t,q)
plt.legend(["Section1", "Section2","Section3","Section4","Section5","Section6","Section7","Section8","Section9"], loc ="upper left") 
# plt.plot(t,q, 'r--', t,q, 'bs', t,q,'g^' )
plt.xlabel('time(min)')
plt.ylabel('qOut(cfc)')
plt.show()
               

