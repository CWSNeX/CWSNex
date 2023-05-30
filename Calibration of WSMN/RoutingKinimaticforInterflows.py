#-------------------------------------------------------------------------
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
qInter = pd.DataFrame(Data,columns = ['Chekan']).to_numpy()
[mm,uu] = qInter.shape
#-------------------------------------------------------------------------------------------------
# Import River Constants
Data  = pd.read_excel(r'D:\My Code New\DataBank\RiverInformations.xlsx')
nInt = pd.DataFrame(Data,columns = ['ManingCoefficient']).to_numpy()
sInt = pd.DataFrame(Data,columns = ['Slope']).to_numpy()
bInt = pd.DataFrame(Data,columns = ['Width']).to_numpy()
LInt = pd.DataFrame(Data,columns = ['RiverLength']).to_numpy()

# kinematic wave parameter: 0.6 is for broad sheet flow
beta = 0.6
#-------------------------------------------------------------------------------------------------
# Define dx and dt to routing
# Data  = pd.read_excel(r'D:\My Code New\DataBank\DisConsumers.xlsx')
# DisConsumer = pd.DataFrame(Data,columns = ['DisConsumerEsparan','DisConsumerChekan']).to_numpy()
dt = 30 * 24 * 3600
#--------------------------------------------------------------------------------------------------
# Define k( the place which is neccesary to calculate qOut)
# k is the section that we need hydralulic head and for each interflow we have to initial the intial dishcharge
# so should updated with number of interflows
dxInt = 1000 
# Number of Sectios
k = int(sum(LInt)/dxInt) +1

# -------------------------------------------------------------------------------------------------
# Define Predicted Matrix for Interflow1
yInt = np.zeros((mm,k))
pInt = np.zeros((mm,k))
alphaInt = np.zeros((mm,k)) 
qOutInt = np.zeros((mm,k))
t = np.linspace(0,120,120)
# #--------------------------------------------------------------------------------------------------
# ***** CHANNEL ALPHA (KIN. WAVE)*****************************
# ************************************************************
# Following calculations are needed to calculate Alpha parameter in kinematic wave. 
############# ***** For All Interflows ****** #############
# for ii in range(0,uu):
#     if ii == 0:
#         for i in range(0,k):
#         # if ii == 0:
#             for j in range(0,mm):
#                 if i == 0 and j>=0:
#                     qOutInt[j,0] = qInter[j,ii]
#                     yInt[j,i] = (( qOutInt[j,i]*nInt[ii,0])/( bInt[ii,0] * sqrt(sInt[ii,0])))**(3/5)
#                     pInt[j,i]= bInt[ii,0] + 2 * yInt[j,i]
#                     alphaInt[j,i] = ((nInt[ii,0] * pInt[j,i]**(2/3))/sqrt(sInt[ii,0]))**beta
#                 elif j == 0 and i>0: 
#                     qOutInt[0,i]= 0
#                     yInt[j,i] = (( qOutInt[j,i]*nInt[ii,0])/( bInt[ii,0] * sqrt(sInt[ii,0])))**(3/5)
#                     pInt[j,i]= bInt[ii,0] + 2 * yInt[j,i]
#                     alphaInt[j,i] = ((nInt[ii,0] * pInt[j,i]**(2/3))/sqrt(sInt[ii,0]))**beta
    # If there is another intrflow which has 44 km and start from the 13 column in qOutInt
    # if ii == 1:                
    #     for i in range(13,k):
    #     # if ii == 1:
    #         for j in range(0,mm):
    #             if i == 13 and j>=0:
    #                 qOutInt[j,i] = qInter[j,ii]
    #                 yInt[j,i] = (( qOutInt[j,i]*nInt[ii,0])/( bInt[ii,0] * sqrt(sInt[ii,0])))**(3/5)
    #                 pInt[j,i]= bInt[ii,0] + 2 * yInt[j,i]
    #                 alphaInt[j,i] = ((nInt[ii,0] * pInt[j,i]**(2/3))/sqrt(sInt[ii,0]))**beta
    #             elif j == 0 and i>13: 
    #                 qOutInt[0,i]= 1
                    # yInt[j,i] = (( qOutInt[j,i]*nInt[ii,0])/( bInt[ii,0] * sqrt(sInt[ii,0])))**(3/5)
                    # pInt[j,i]= bInt[ii,0] + 2 * yInt[j,i]
                    # alphaInt[j,i] = ((nInt[ii,0] * pInt[j,i]**(2/3))/sqrt(sInt[ii,0]))**beta
                    
    
                    
# -------------------------------------------------------------------------------------------
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
        

# #---------------------------------------------------------------------------------------------------------         
# following loop is used to calculate routed discharge for each i,j 
# uu Number of Interflows

# for ii in range(0,uu):    
#     for i in range(0,k):
#         if ii == 0 and i < 52:
#             for j in range(0,mm-1):
                   
#                 qOutInt[j+1,i+1] = routing(alphaInt[j,i],beta,qOutInt[j+1,i],qOutInt[j,i+1],dxInt,dt)
#                 # Define QInitial which calulated from perevious place 
#                 if i >= 0:
#                     qOutInt[j+1,i+1] =  qOutInt[j+1,i+1].copy()
#                     yInt[j,i+1] = (( qOutInt[j+1,i+1]*nInt[ii,0])/( bInt[ii,0] * sqrt(sInt[ii,0])))**(3/5)
#                     pInt[j,i+1]= bInt[ii,0] + 2 * yInt[j,i+1]
#                     alphaInt[j,i+1] = ((nInt[ii,0] * pInt[j,i+1]**(2/3))/sqrt(sInt[ii,0]))**beta
#                 # Define QBoundary which calculated from perevious time
#                 if j >= 0: 
#                     qOutInt[j+1,i+1] = qOutInt[j+1,i+1].copy()
                    
        # If there is another intrflow which has 44 km and start from the 13 column in qOutInt
        # if ii == 1 and 12< i < 66:
        #     for j in range(0,mm-1):
        #       
        #         qOutInt[j+1,i+1] = routing(alphaInt[j,i],beta,qOutInt[j+1,i],qOutInt[j,i+1],dxInt,dt)
        #         
        #            
        #         yInt[j,i+1] = (( qOutInt[j+1,i+1]*nInt[ii,0])/( bInt[ii,0] * sqrt(sInt[ii,0])))**(3/5)
        #         pInt[j,i+1]= bInt[ii,0] + 2 * yInt[j,i+1]
        #         alphaInt[j,i+1] = ((nInt[ii,0] * pInt[j,i+1]**(2/3))/sqrt(sInt[ii,0]))**beta
  
                   
            
# har kodam az jaryanat miani dar tole khod har 1000 metr ravandyabi shode va bad mojdadan har 1000 metr vared rodkhane asli shode              
# plt.plot(t,qOutInt[:,51])
# # # # plt.plot(t2,qOutInt2)
# # # # plt.plot(t3,qOutInt3)
# plt.legend(["Finall Point"], loc ="upper right") 
# plt.xlabel('time(Month)')
# plt.ylabel('qOutInterflow(M3/s)')
# plt.show()