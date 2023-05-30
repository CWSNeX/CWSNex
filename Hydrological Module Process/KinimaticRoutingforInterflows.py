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
# Import  Initial Interflows 
Data  = pd.read_excel(r'D:\My Code New\DataBank\Interflow.xlsx')
qInter1 = pd.DataFrame(Data,columns = ['Interflow1']).to_numpy()
qInter2 = pd.DataFrame(Data,columns = ['Interflow2']).to_numpy()
qInter3 = pd.DataFrame(Data,columns = ['Interflow3']).to_numpy()
dt = 3*60
#-------------------------------------------------------------------------------------------------
# Define Interflow1 Constant
# River bottom width [meters]
b1 = 200
# River gradient (fraction, dy/dx)
s1 = 0.01 
# River Manning's n
n1 = 0.035
# River length [meters]
L_InterRiver1 = 1000 
# kinematic wave parameter: 0.6 is for broad sheet flow
beta =  0.6 
#--------------------------------------------------------------------------------------------------
# Define Interflow2 Constant
# River bottom width [meters]
b2 = 200
# River gradient (fraction, dy/dx)
s2 = 0.01 
# River Manning's n
n2 = 0.035
# River length [meters]
L_InterRiver2 = 2000
# kinematic wave parameter: 0.6 is for broad sheet flow
beta =  0.6
#--------------------------------------------------------------------------------------------------
# Define Interflow3 Constant
# River bottom width [meters]
b3 = 200
# River gradient (fraction, dy/dx)
s3 = 0.01 
# River Manning's n
n3 = 0.035
# River length [meters]
L_InterRiver3 = 1500
# kinematic wave parameter: 0.6 is for broad sheet flow
beta =  0.6
#--------------------------------------------------------------------------------------------------
# Define Predicted Matrix for Interflow1
m1 = 20
k1 = 6
yInt1 = np.zeros((m1,k1))
pInt1 = np.zeros((m1,k1))
alphaInt1 = np.zeros((m1,k1)) 
qOutInt1 = np.zeros((m1,k1))
dx1 = []
disInterInter1 = [150,600,1000,0,0,0]
disConsumer1 = [50,250,800,0,0,0]
t1 = np.linspace(0,120,20) 
#--------------------------------------------------------------------------------------------------
# Define Predicted Matrix for Interflow2
m2 = 7
k2 = 2
yInt2 = np.zeros((m2,k2))
pInt2 = np.zeros((m2,k2))
alphaInt2 = np.zeros((m2,k2)) 
qOutInt2 = np.zeros((m2,k2))
dx2 = []
disInterInter2 = [600,2000]
disConsumer2 = [352,400]
t2 = np.linspace(0,120,7)
#--------------------------------------------------------------------------------------------------
# Define Predicted Matrix for Interflow3
m3 = 18
k3 = 5
yInt3 = np.zeros((m3,k3))
pInt3 = np.zeros((m3,k3))
alphaInt3 = np.zeros((m3,k3)) 
qOutInt3 = np.zeros((m3,k3))
dx3 = []
disInterInter3 = [800,1000,1400,1500,0]
disConsumer3 = [450,560,600,660,0]
t3 = np.linspace(0,120,18)
#--------------------------------------------------------------------------------------------------

# ***** CHANNEL ALPHA (KIN. WAVE)*****************************
# ************************************************************
# Following calculations are needed to calculate Alpha parameter in kinematic wave. 
############# ***** For Interflow1 **** ################      
for i in range(0,k1):
    for j in range(0,m1):
        if i == 0 and j>=0:
            qOutInt1[j,0] = qInter1[j,0]
            yInt1[j,i] = (( qOutInt1[j,i]*n1)/(1.49 * b1 * sqrt(s1)))**(3/5)
            pInt1[j,i]= b1 + 2 * yInt1[j,i]
            alphaInt1[j,i] = ((n1 * pInt1[j,i]**(2/3))/sqrt(s1))**beta
        elif j == 0 and i>0: 
            qOutInt1[0,i]= 2000
############# ***** For Interflow2 **** ################              
for i in range(0,k2):
    for j in range(0,m2):
        if i == 0 and j>=0:
            qOutInt2[j,0] = qInter2[j,0]
            yInt2[j,i] = (( qOutInt2[j,i]*n2)/(1.49 * b2 * sqrt(s2)))**(3/5)
            pInt2[j,i]= b2 + 2 * yInt2[j,i]
            alphaInt2[j,i] = ((n2 * pInt2[j,i]**(2/3))/sqrt(s2))**beta
        elif j == 0 and i>0: 
            qOutInt2[0,i]= 2000
############# ***** For Interflow3 **** ################              
for i in range(0,k3):
    for j in range(0,m3):
        if i == 0 and j>=0:
            qOutInt3[j,0] = qInter3[j,0]
            yInt3[j,i] = (( qOutInt3[j,i]*n3)/(1.49 * b3 * sqrt(s3)))**(3/5)
            pInt3[j,i]= b3 + 2 * yInt3[j,i]
            alphaInt3[j,i] = ((n3 * pInt3[j,i]**(2/3))/sqrt(s3))**beta
        elif j == 0 and i>0: 
            qOutInt3[0,i]= 2000
#----------------------------------------------------------------------------------------------------------            
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
#----------------------------------------------------------------------------------------------------------        
# Following def update discharge where there is Interflow       
def interflow(QOUT,QINTER):
    
             q = QOUT + QINTER
             return q
#------------------------------------------------------------------------------------------------------------
# Calculate the point which there discharged will be calculated 
############# ***** For Interflow1 **** ################  
for i in range(0,k1-1):
    if disInterInter1[i]< disConsumer1[i] :
        dx1.append(disInterInter1[i])
        dx1.append(disConsumer1[i])
    elif disConsumer1[i] < disInterInter1[i]:
         dx1.append(disConsumer1[i])
         dx1.append(disInterInter1[i])   
############# ***** For Interflow2 **** ################           
for i in range(0,k2-1):
    if disInterInter2[i]< disConsumer2[i] :
        dx2.append(disInterInter2[i])
        dx2.append(disConsumer2[i])
    elif disConsumer2[i] < disInterInter2[i]:
         dx2.append(disConsumer2[i])
         dx2.append(disInterInter2[i])
############# ***** For Interflow3 **** ################           
for i in range(0,k3-1):
    if disInterInter3[i]< disConsumer3[i] :
        dx3.append(disInterInter3[i])
        dx3.append(disConsumer3[i])
    elif disConsumer3[i] < disInterInter3[i]:
         dx3.append(disConsumer3[i])
         dx3.append(disInterInter3[i])    
         
#---------------------------------------------------------------------------------------------------------         
# following loop is used to calculate routed discharge for each i,j 


############# ***** For Interflow1 **** ################           
for i in range(0,k1-1):
        
    if disInterInter1[i] > disConsumer1[i] and disInterInter1[i] < disConsumer1[i+1] :
        for j in range(0,m1-1):
        # Update qOut respect to new Interflow
            qOutInt1[j+1,i] = interflow(qOutInt1[j+1,i],qInter1[j,0])
            qOutInt1[j+1,i+1] = routing(alphaInt1[j,i],beta,qOutInt1[j+1,i],qOutInt1[j,i+1],dx1[i],dt)
            yInt1[j,i+1] = (( qOutInt1[j+1,i+1]*n1)/(1.49 * b1 * sqrt(s1)))**(3/5)
            pInt1[j,i+1]= b1 + 2 * yInt1[j,i+1]
            alphaInt1[j,i+1] = ((n1 * pInt1[j,i+1]**(2/3))/sqrt(s1))**beta
            
            
    else:
        for j in range(0,m1-1):
            qOutInt1[j+1,i+1] = routing(alphaInt1[j,i],beta,qOutInt1[j+1,i],qOutInt1[j,i+1],dx1[i],dt)
            yInt1[j,i+1] = (( qOutInt1[j+1,i+1]*n1)/(1.49 * b1 * sqrt(s1)))**(3/5)
            pInt1[j,i+1]= b1 + 2 * yInt1[j,i+1]
            alphaInt1[j,i+1] = ((n1 * pInt1[j,i+1]**(2/3))/sqrt(s1))**beta
            
            
############# ***** For Interflow2 **** ################              
            
            
            
# following loop is used to calculate routed discharge for each i,j            
for i in range(0,k2-1):
        
    if disInterInter2[i] > disConsumer2[i] and disInterInter2[i] < disConsumer2[i+1] :
        for j in range(0,m2-1):
            # Update qOut respect to new Interflow
            qOutInt2[j+1,i] = interflow(qOutInt2[j+1,i],qInter2[j,0])
            qOutInt2[j+1,i+1] = routing(alphaInt2[j,i],beta,qOutInt2[j+1,i],qOutInt2[j,i+1],dx2[i],dt)
            yInt2[j,i+1] = (( qOutInt2[j+1,i+1]*n2)/(1.49 * b2 * sqrt(s2)))**(3/5)
            pInt2[j,i+1]= b2 + 2 * yInt2[j,i+1]
            alphaInt2[j,i+1] = ((n2 * pInt2[j,i+1]**(2/3))/sqrt(s2))**beta 
    else:
        for j in range(0,m2-1):
            qOutInt2[j+1,i+1] = routing(alphaInt2[j,i],beta,qOutInt2[j+1,i],qOutInt2[j,i+1],dx2[i],dt)
            yInt2[j,i+1] = (( qOutInt2[j+1,i+1]*n2)/(1.49 * b2 * sqrt(s2)))**(3/5)
            pInt2[j,i+1]= b2 + 2 * yInt2[j,i+1]
            alphaInt2[j,i+1] = ((n2 * pInt2[j,i+1]**(2/3))/sqrt(s2))**beta

          

############# ***** For Interflow3 **** ################      
for i in range(0,k3-1):
        
    if disInterInter3[i] > disConsumer3[i] and disInterInter3[i] < disConsumer3[i+1] :
        for j in range(0,m3-1):
        # Update qOut respect to new Interflow
            qOutInt3[j+1,i] = interflow(qOutInt3[j+1,i],qInter3[j,0])
            qOutInt3[j+1,i+1] = routing(alphaInt3[j,i],beta,qOutInt3[j+1,i],qOutInt3[j,i+1],dx3[i],dt)
            yInt3[j,i+1] = (( qOutInt3[j+1,i+1]*n3)/(1.49 * b3 * sqrt(s3)))**(3/5)
            pInt3[j,i+1]= b3 + 2 * yInt3[j,i+1]
            alphaInt3[j,i+1] = ((n3 * pInt3[j,i+1]**(2/3))/sqrt(s3))**beta    
            
    else:
        for j in range(0,m3-1):
            qOutInt3[j+1,i+1] = routing(alphaInt3[j,i],beta,qOutInt3[j+1,i],qOutInt3[j,i+1],dx3[i],dt)
            yInt3[j,i+1] = (( qOutInt3[j+1,i+1]*n3)/(1.49 * b3 * sqrt(s3)))**(3/5)
            pInt3[j,i+1]= b3 + 2 * yInt3[j,i+1]
            alphaInt3[j,i+1] = ((n3 * pInt3[j,i+1]**(2/3))/sqrt(s3))**beta

qInter  = [qOutInt1,qOutInt2,qOutInt3]
        
plt.plot(t1,qOutInt1)
# plt.plot(t2,qOutInt2)
# plt.plot(t3,qOutInt3)
plt.legend(["Section1", "Section2","Section3","Section4","Section5"], loc ="upper right") 
plt.xlabel('time(min)')
plt.ylabel('qOutInterflow(CFC)')
plt.show()