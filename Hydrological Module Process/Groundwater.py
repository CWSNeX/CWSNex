# -------------------------------------------------------------------------
# Name:        Groundwater Simulation
# Purpose:     This madule define head and storage of groundwater
#
# Author:      Elham Soleimanian
#
# Created:     1/3/2021
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
# import scipy as sc
import pandas as pd
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D 
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
# from scipy.ndimage.interpolation import shift

#-------------------------------------------------------------------------
# Import Distance of food consumer each column relates to each aquifer or each part of one aquifer(a uniq area)
data = pd.ExcelFile(r'D:\My Code New\DataBank\Disfoodenergy.xlsx')
disfood = pd.read_excel(data, 'DISFOOD',usecols='A:C').to_numpy()
# UU shows number of aquifer and mm shows number of fooduser in each aquifer
[mm,uu] = disfood.shape
#-------------------------------------------------------------------------
# Data to calculate water interaction for DARCY function
# Hydraulic conductivity should import for each aquifer and for each section that there is food user
data = pd.ExcelFile(r'D:\My Code New\DataBank\AquiferConstants.xlsx')
k = pd.read_excel(data, 'hydraulic conductivity',usecols='A:C').to_numpy()
 
#-------------------------------------------------------------------------
# Return flow from Food and Energy Sector
# It's assumed that there is no return flow to GW from energy 
data = pd.ExcelFile(r'D:\My Code New\DataBank\FoodreturnflowtoGW.xlsx')
qReturnF= pd.read_excel(data, 'Returnflowfromfood',usecols='B:J').to_numpy()
[m,u] =qReturnF.shape
#-------------------------------------------------------------------------
# Data to calculate Storage and Head 
data = pd.ExcelFile(r'D:\My Code New\DataBank\AquiferConstants.xlsx')
area = pd.read_excel(data, 'area',usecols='A:C').to_numpy()
SpecificS = pd.read_excel(data, 'storgecoefficient',usecols='A:C').to_numpy()
data = pd.ExcelFile(r'D:\My Code New\DataBank\RainfallGW.xlsx')
Rainfall = pd.read_excel(data, 'rainfall',usecols='B:J').to_numpy()
# #-------------------------------------------------------------------------
# # Preallocation Matrix
qInteraction = np.zeros((m,u))
qOut = np.zeros((m,u))
deltastorage = np.zeros((m,u))
storage = np.zeros((m,u))
head = np.zeros((m,u))
deltaH = np.zeros((m,u))
deltaHP = np.zeros((m,u))
deltaL = np.zeros((mm,uu))
deltaLG = np.zeros((m,u))
k_G = np.zeros((mm,uu))
#--------------------------------------------------------------------------
###### ***** Following Function calculate the interaction between rivers and groundwater *****#####
# if the calculated discharge will be negative it means"Deplation" 
# if the calculated discharge will be positive it means"Recharge" in groundwater reservior
def DARCY(K,DELTAHP,DELTAL):
         QINTERACTION = 0
         QINTERACTION  = -K * DELTAHP/DELTAL
         return QINTERACTION


#--------------------------------------------------------------------------
###### ***** Following Function calculate the outflow of groundwater based on water system decesion maker *****#####
def SUSTAINABLEWITHDRAWAL(SPECIFICSTORAGE,AREA,DELTAH,RAINFALL,QRETURNF):
                         QOUT = 0 
                         QAQUIFER = SPECIFICSTORAGE * AREA * DELTAH
                         QOUT = 0.5 * (QAQUIFER + RAINFALL + QRETURNF)
                         
                         return QOUT
#-------------------------------------------------------------------------
###### ****** Fllowing Function calculate storage and head of groundwater
def STORAGE(QRETURNF,QOUT,RAINFALL,AREA,SPECIFICSTORAGE):
           DELTASTORAGE = 0
           DELTASTORAGE =  QRETURNF + RAINFALL - QOUT
           return DELTASTORAGE
       
        
# Call Functions       
#ii index for each aquifer and jj and i indexs for user of each aquifer and j index for time
for ii in range(0,uu):
    for jj in range(0,mm-1):
        for i in range(0,u):
            if ii == 0 and i <5:
                for j in range(0,m-1):
                    if j == 0:
                        # qInteraction[0,i] = 0       
                        head[0,i] = 0                # initial head of each aquifer 
                        storage[0,i] = 0             # initial storage
                        qOut[0,i] = 0                # initial outflow from aquifer in time step 1
                        deltastorage[j+1,i] = STORAGE(qReturnF[j,i],qOut[j,i],Rainfall[j,i],area[jj,ii],SpecificS[jj,ii])
                        storage[j+1,i] = deltastorage[j+1,i] - storage[j,i]
                        head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii]      #Calculate Groundwater head in each 
                        deltaH[j+1,i] = head[j+1,i] - head[j,i]     # Calculate head of each user in different time()
                        deltaL[jj,ii] = disfood[jj+1,ii]- disfood[jj,ii]
            
                    if j >0:
                        
                        
                        # qInteraction[j,i] = DARCY(k[jj,ii] ,deltaH[j,i],deltaL[jj,ii])       
                        qOut[j,i] = SUSTAINABLEWITHDRAWAL(SpecificS[jj,ii],area[jj,ii],deltaH[j,i],Rainfall[j,i],qReturnF[j,i])
                        deltastorage[j+1,i] = STORAGE(qReturnF[j,i],qOut[j,i],Rainfall[j,i],area[jj,ii],SpecificS[jj,ii])
                        storage[j+1,i] = deltastorage[j+1,i] - storage[j,i]
                        head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii]
                        deltaH[j+1,i] = head[j+1,i] - head[j,i] 
                        deltaL[jj,ii] = disfood[jj+1,ii]- disfood[jj,ii]
                        
                     
                        
            if ii == 1 and 5 <= i <=7:
                for j in range(0,m-1):
                    if j == 0:
                        # qInteraction[0,i] = 0
                        head[0,i] = 0                 # initial head of each aquifer 
                        storage[0,i] = 0              # initial storage
                        qOut[0,i] = 0                 # initial outflow from aquifer in time step 1
                        deltastorage[j+1,i] = STORAGE(qReturnF[j,i],qOut[j,i],Rainfall[j,i],area[jj,ii],SpecificS[jj,ii])
                        storage[j+1,i] = deltastorage[j+1,i] - storage[j,i]
                        head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii]      #Calculate Groundwater head in each 
                        deltaH[j+1,i] = head[j+1,i] - head[j,i] 
                        deltaL[jj,ii] = disfood[jj+1,ii]- disfood[jj,ii]
            
                    if j >0:
                        
                        
                        # qInteraction[j,i] = DARCY(k[jj,ii] ,deltaH[j,i],deltaL[jj,ii])       
                        qOut[j,i] = SUSTAINABLEWITHDRAWAL(SpecificS[jj,ii],area[jj,ii],deltaH[j,i],Rainfall[j,i],qReturnF[j,i])
                        deltastorage[j+1,i] = STORAGE(qReturnF[j,i],qOut[j,i],Rainfall[j,i],area[jj,ii],SpecificS[jj,ii])
                        storage[j+1,i] = deltastorage[j+1,i] - storage[j,i]
                        head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii]
                        deltaH[j+1,i] = head[j+1,i] - head[j,i] 
                        deltaL[jj,ii] = disfood[jj+1,ii]- disfood[jj,ii]
                        
                
                
            if ii == 2  and i ==8 :
                for j in range(0,m-1):
                   
                    if j == 0:
                        # qInteraction[0,i] = 0
                        head[0,i] = 0                 # initial head of each aquifer 
                        storage[0,i] = 0
                        qOut[0,i] = 0
                        deltastorage[j+1,i] = STORAGE(qReturnF[j,i],qOut[j,i],Rainfall[j,i],area[jj,ii],SpecificS[jj,ii])
                        storage[j+1,i] = deltastorage[j+1,i] - storage[j,i]
                        head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii]      #Calculate Groundwater head in each 
                        deltaH[j+1,i] = head[j+1,i] - head[j,i] 
                        deltaL[jj,ii] = disfood[jj+1,ii]- disfood[jj,ii]
            
                    if j >0:
                        
                        # deltaL[j,i] =disfood[j,i+1] - disfood[j,i]
                        # qInteraction[j,i] = DARCY(k[jj,ii] ,deltaH[j,i],deltaL[jj,ii])       
                        qOut[j,i] = SUSTAINABLEWITHDRAWAL(SpecificS[jj,ii],area[jj,ii],deltaH[j,i],Rainfall[j,i],qReturnF[j,i])
                        deltastorage[j+1,i] = STORAGE(qReturnF[j,i],qOut[j,i],Rainfall[j,i],area[jj,ii],SpecificS[jj,ii])
                        storage[j+1,i] = deltastorage[j+1,i] - storage[j,i]
                        head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii]
                        deltaH[j+1,i] = head[j+1,i] - head[j,i] 
                        deltaL[jj,ii] = disfood[jj+1,ii]- disfood[jj,ii]
 
#--------------------------------------------------------------------------------
# Reshape Matrixes to calculate QInteraction
deltaL[deltaL==0] = np.nan
deltaL1 = np.reshape(deltaL,(1,15),'F')
deltaL1 = deltaL1[np.logical_not(np.isnan(deltaL1))]
deltaL1 = np.reshape(deltaL1,(1,6),'F')
deltaLG = np.repeat(deltaL1,41,axis = 0)
# -------------------------------------------------------------------------------
# Calculate average hydraulic head between to user of each aquifer
for ii in range(0,uu):
    for jj in range(0,mm-1):
        k_G[jj,ii] = (k[jj,ii] + k[jj+1,ii])/2
# -----------------------------------------------------------------------------
# Reshape Matrixes to calculate QInteraction
k_G[k_G==0] = np.nan
k_G = np.reshape(k_G,(1,15),'F')
k_G = k_G[np.logical_not(np.isnan(k_G))]
k_G = np.reshape(k_G,(1,12),'F')
k_G = np.repeat(k_G,41,axis = 0)
# --------------------------------------------------------------------------------
# Calculate Hydraulic Gradianent(Gradient can be calculated between two points, bassed on number of deltaL, gradient shoul calculated)
# u-3  shows number of coulumn which calculate interaction for the rest column aquifer head calculated previously
for ii in range(0,uu):
    for jj in range(0,mm-1):
        for i in range(0,u-3):
            if ii == 0 and i < 5:
                for j in range(0,m):
                    deltaHP[j,i] = head[j,i+1] - head[j,i]
                    qInteraction[j,i] = DARCY(k_G[j,i],deltaHP[j,i],deltaLG[j,i])
                    
            if ii == 1 and 5 <= i <=7:
                for j in range(0,m):
                    deltaHP[j,i] = head[j,i+1] - head[j,i]
                    qInteraction[j,i] = DARCY(k_G[j,i],deltaHP[j,i],deltaLG[j,i])
                                  
# --------------------------------------------------------------------------------
# Update head on the time and place                                                                               
for ii in range(0,uu):
    for jj in range(0,mm-1):
        for i in range(0,u):
            if ii == 0 and i <5:
                for j in range(0,m-1):
                    deltastorage[j+1,i] = deltastorage[j+1,i] + qInteraction[j,i]
                    head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii] 
            if ii == 1 and i == 5 :
                for j in range(0,m-1):
                    deltastorage[j+1,i] = deltastorage[j+1,i] + qInteraction[j,i]
                    head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii] 
            # if ii == 2 and i == 8:
            #     for j in range(0,m-1):
            #         deltastorage[j,i] = deltastorage[j,i] + qInteraction[j,i]
            #         head[j+1,i] = deltastorage[j+1,i] / area[jj,ii] * SpecificS[jj,ii]
                
                

                    
# --------------------------------------------------------------------------------
# Plot  head of aquifers
fig = plt.figure()
ax = fig.gca(projection='3d')
# Create t and x as shape head
t = np.arange(0, 9, 1)
x = np.arange(0, 41, 1)
t, x = np.meshgrid(t, x)

# Plot the surface.
surf = ax.plot_surface(t, x,head, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
# Customize the z axis.
ax.set_zlim(0, 2.5)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.75, aspect=10)
plt.show()


                    