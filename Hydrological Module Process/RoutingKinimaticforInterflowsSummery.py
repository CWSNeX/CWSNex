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
#-------------------------------------------------------------------------------------------------
# Import  Initial Interflows 
Data  = pd.read_excel(r'D:\My Code New\DataBank\Interflow.xlsx')
qInter = pd.DataFrame(Data,columns = ['Interflow1','Interflow2','Interflow3']).to_numpy()
[m,u] = qInter.shape
#-------------------------------------------------------------------------------------------------
# Import River Constants
Data  = pd.read_excel(r'D:\My Code New\DataBank\RiverInformations.xlsx')
n = pd.DataFrame(Data,columns = ['ManingCoefficient']).to_numpy()
s = pd.DataFrame(Data,columns = ['Slope']).to_numpy()
b = pd.DataFrame(Data,columns = ['Width']).to_numpy()
L = pd.DataFrame(Data,columns = ['RiverLength']).to_numpy()

# kinematic wave parameter: 0.6 is for broad sheet flow
beta = 0.6
#-------------------------------------------------------------------------------------------------
# Define dx and dt to routing
Data  = pd.read_excel(r'D:\My Code New\DataBank\DisInterflows.xlsx')
DisInterInter = pd.DataFrame(Data,columns = ['DisInterInter1','DisInterInter2','DisInterInter3']).to_numpy()
Data  = pd.read_excel(r'D:\My Code New\DataBank\DisConsumers.xlsx')
DisConsumer = pd.DataFrame(Data,columns = ['DisConsumer1','DisConsumer2','DisConsumer3']).to_numpy()


dt = 3*60
#--------------------------------------------------------------------------------------------------
# Define k( the place which is neccesary to calculate qOut)
k1 = 6
k2 = 4
k3 = 8
k = 18

# #--------------------------------------------------------------------------------------------------
# Define Predicted Matrix for Interflow1
yInt = np.zeros((m,k))
pInt = np.zeros((m,k))
alphaInt = np.zeros((m,k)) 
qOutInt = np.zeros((m,k))
t = np.linspace(0,120,41)
# #--------------------------------------------------------------------------------------------------
# ***** CHANNEL ALPHA (KIN. WAVE)*****************************
# ************************************************************
# Following calculations are needed to calculate Alpha parameter in kinematic wave. 
############# ***** For Interflow1 **** ################    
for ii in range(0,u):
    
    for i in range(0,k):
        if ii == 0:
            for j in range(0,m):
                if i == 0 and j>=0:
                    qOutInt[j,0] = qInter[j,ii]
                    yInt[j,i] = (( qOutInt[j,i]*n[ii,0])/(1.49 * b[ii,0] * sqrt(s[ii,0])))**(3/5)
                    pInt[j,i]= b[ii,0] + 2 * yInt[j,i]
                    alphaInt[j,i] = ((n[ii,0] * pInt[j,i]**(2/3))/sqrt(s[ii,0]))**beta
                elif j == 0 and i>0: 
                    qOutInt[0,i]= 2000
                                              
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
# #------------------------------------------------------------------------------------------------------------
# Calculate the point which there discharged will be calculated 
# Define dx for each interflow
 
dx = np.concatenate((DisInterInter, DisConsumer))
dx = np.sort(dx, axis=0)

                                                
# #---------------------------------------------------------------------------------------------------------         
# following loop is used to calculate routed discharge for each i,j 


############# ***** For Interflow1 **** ################
# ii index for each interflow and dx which related to each interflow and jj index for max number of disconsumer or disinterflow
for ii in range(0,u):  
    for jj in range(0,3):
        for i in range(0,k-1):
            if  ii == 0 and i <6:
                if DisInterInter[jj,ii] >  DisConsumer[jj,ii] and DisInterInter[jj,ii] < DisConsumer[jj+1,ii] :
                    for j in range(0,m-1):
        # Update qOut respect to new Interflow
                        qOutInt[j+1,i] = interflow(qOutInt[j+1,i],qInter[j,ii])
                        qOutInt[j+1,i+1] = routing(alphaInt[j,i],beta,qOutInt[j+1,i],qOutInt[j,i+1],dx[jj,ii],dt)
                        yInt[j,i+1] = (( qOutInt[j+1,i+1]*n[ii,0])/(1.49 * b[ii,0] * sqrt(s[ii,0])))**(3/5)
                        pInt[j,i+1]= b[ii,0] + 2 * yInt[j,i+1]
                        alphaInt[j,i+1] = ((n[ii,0] * pInt[j,i+1]**(2/3))/sqrt(s[ii,0]))**beta
            
            
                else:
                    for j in range(0,m-1):
                        qOutInt[j+1,i+1] = routing(alphaInt[j,i],beta,qOutInt[j+1,i],qOutInt[j,i+1],dx[jj,ii],dt)
                        yInt[j,i+1] = (( qOutInt[j+1,i+1]*n[ii,0])/(1.49 * b[ii,0] * sqrt(s[ii,0])))**(3/5)
                        pInt[j,i+1]= b[ii,0] + 2 * yInt[j,i+1]
                        alphaInt[j,i+1] = ((n[ii,0] * pInt[j,i+1]**(2/3))/sqrt(s[ii,0]))**beta
                        
                        
            if ii == 1 and 6<= i <10:
                qOutInt[j+1,7] = qInter[j,ii]
                if DisInterInter[jj,ii] >  DisConsumer[jj,ii] and DisInterInter[jj,ii] < DisConsumer[jj+1,ii] :
                    for j in range(0,m-1):
        # Update qOut respect to new Interflow
                        qOutInt[j+1,i] = interflow(qOutInt[j+1,i],qInter[j,ii])
                        qOutInt[j+1,i+1] = routing(alphaInt[j,i],beta,qOutInt[j+1,i],qOutInt[j,i+1],dx[jj,ii],dt)
                        yInt[j,i+1] = (( qOutInt[j+1,i+1]*n[ii,0])/(1.49 * b[ii,0] * sqrt(s[ii,0])))**(3/5)
                        pInt[j,i+1]= b[ii,0] + 2 * yInt[j,i+1]
                        alphaInt[j,i+1] = ((n[ii,0] * pInt[j,i+1]**(2/3))/sqrt(s[ii,0]))**beta
            
            
                else:
                    for j in range(0,m-1):
                        qOutInt[j+1,7] = qInter[j,ii]
                        qOutInt[j+1,i+1] = routing(alphaInt[j,i],beta,qOutInt[j+1,i],qOutInt[j,i+1],dx[jj,ii],dt)
                        yInt[j,i+1] = (( qOutInt[j+1,i+1]*n[ii,0])/(1.49 * b[ii,0] * sqrt(s[ii,0])))**(3/5)
                        pInt[j,i+1]= b[ii,0] + 2 * yInt[j,i+1]
                        alphaInt[j,i+1] = ((n[ii,0] * pInt[j,i+1]**(2/3))/sqrt(s[ii,0]))**beta
                        
                        
            if ii == 2 and i>=10:
                qOutInt[j+1,11] = qInter[j,ii]
                if DisInterInter[jj,ii] >  DisConsumer[jj,ii] and DisInterInter[jj,ii] < DisConsumer[jj+1,ii] :
                    for j in range(0,m-1):
        # Update qOut respect to new Interflow
                        qOutInt[j+1,i] = interflow(qOutInt[j+1,i],qInter[j,ii])
                        qOutInt[j+1,i+1] = routing(alphaInt[j,i],beta,qOutInt[j+1,i],qOutInt[j,i+1],dx[jj,ii],dt)
                        yInt[j,i+1] = (( qOutInt[j+1,i+1]*n[ii,0])/(1.49 * b[ii,0] * sqrt(s[ii,0])))**(3/5)
                        pInt[j,i+1]= b[ii,0] + 2 * yInt[j,i+1]
                        alphaInt[j,i+1] = ((n[ii,0] * pInt[j,i+1]**(2/3))/sqrt(s[ii,0]))**beta
            
            
                else:
                    for j in range(0,m-1):
                        qOutInt[j+1,11] = qInter[j,ii]
                        qOutInt[j+1,i+1] = routing(alphaInt[j,i],beta,qOutInt[j+1,i],qOutInt[j,i+1],dx[jj,ii],dt)
                        yInt[j,i+1] = (( qOutInt[j+1,i+1]*n[ii,0])/(1.49 * b[ii,0] * sqrt(s[ii,0])))**(3/5)
                        pInt[j,i+1]= b[ii,0] + 2 * yInt[j,i+1]
                        alphaInt[j,i+1] = ((n[ii,0] * pInt[j,i+1]**(2/3))/sqrt(s[ii,0]))**beta

# qInter  = [qOutInt1,qOutInt2,qOutInt3]        
plt.plot(t,qOutInt)
# # plt.plot(t2,qOutInt2)
# # plt.plot(t3,qOutInt3)
plt.legend(["Section1", "Section2","Section3","Section4","Section5"], loc ="upper right") 
plt.xlabel('time(min)')
plt.ylabel('qOutInterflow(CFC)')
plt.show()