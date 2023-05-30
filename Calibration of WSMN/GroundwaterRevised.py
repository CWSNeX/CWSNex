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
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


#-------------------------------------------------------------------------
# Data to calculate water interaction for DARCY function
# Hydraulic conductivity should import for each aquifer and for each section that there is food user
data = pd.ExcelFile(r'D:\My Code New\DataBank\AquiferConstants.xlsx')
k = pd.read_excel(data, 'hydraulic conductivity',usecols='A:D').to_numpy()
Lriver = pd.read_excel(data, 'Riverstream',usecols='A:D').to_numpy()
#-------------------------------------------------------------------------
# Data to calculate Storage and Head 
data = pd.ExcelFile(r'D:\My Code New\DataBank\AquiferConstants.xlsx')
area = pd.read_excel(data, 'area',usecols='A:D').to_numpy()
SpecificS = pd.read_excel(data, 'storgecoefficient',usecols='A:D').to_numpy()
# Import Groundwater Taraz
data1 = pd.ExcelFile(r'D:\My Code New\DataBank\TarazGW.xlsx')
Taraz = pd.read_excel(data1, 'Sheet1',usecols='B:E').to_numpy()
# UU shows number of aquifer and mm shows number of fooduser in each aquifer
[mm,uu] = SpecificS.shape
data = pd.ExcelFile(r'D:\My Code New\DataBank\RainfallGW.xlsx')
Rainfall = pd.read_excel(data, 'rainfall',usecols='B:E').to_numpy()
Cw = [0.1,0.12,0.11,0.13]
#-------------------------------------------------------------------------
# Import River Depth at disrable point which should calculate groundwater and river water Interrelation 
data1 = pd.ExcelFile(r'D:\My Code New\DataBank\WaterLevel.xlsx')
WaterLevel = pd.read_excel(data1, 'Sheet1',usecols='B:E').to_numpy() 
# -------------------------------------------------------------------------
# Import withdrawal from each aquifer for both energy and water consumer
# data2 = pd.ExcelFile(r'D:\My Code New\DataBank\GWWithdrawalforBaseYear.xlsx')
# qOutGW = pd.read_excel(data2, 'Sheet1',usecols='B:E').to_numpy()
#-------------------------------------------------------------------------
# Return flow from Food and Energy Sector
# It's assumed that there is no return flow to GW from energy 
data = pd.ExcelFile(r'D:\My Code New\DataBank\FoodreturnflowtoGW.xlsx')
qReturnF= pd.read_excel(data, 'Returnflowfromfood',usecols='B:E').to_numpy()
qRetrunrFC = [0.1,0.1,0.1,0.1]
[m,u] =qReturnF.shape
# #-------------------------------------------------------------------------
# # Preallocation Matrix
qInteraction = np.zeros((m,u))
qOutGW = np.zeros((m,u))
deltastorage = np.zeros((m,u))
storage = np.zeros((m,u))
head = np.zeros((m,u))
kriv = np.zeros((mm,u))
deltaH = np.zeros((m,u))
# f = 0.9
riverbed = [1390,1326,1290,1280]
RiverAreaPercentages = [0.002,0.003,0.003,0.002]

#--------------------------------------------------------------------------
###### ***** Following Function calculate the interaction between rivers and groundwater *****#####
# if the calculated discharge will be negative it means"Deplation" 
# if the calculated discharge will be positive it means"Recharge" in groundwater reservior
# Calculate KRiver 
def KRIV(F,K,LRIVER):
        KRIV = F * K * LRIVER
        return KRIV 
    

# ------------------------------------------------------------------------  
# TARAZ Is Groundwater Head = Ground Elevation - Water Level(Sath Ab)      
def DARCY(KRIV,TARAZ,WATERLEVEL,RIVERBED,RIVERAREAPERCENTAGE):
         QINTERACTION = 0
         if TARAZ < RIVERBED and WATERLEVEL <= RIVERBED:
             QINTERACTION = 0
         else:
             QINTERACTION  = KRIV * (TARAZ - WATERLEVEL)
         return QINTERACTION * RIVERAREAPERCENTAGE

# 
#--------------------------------------------------------------------------
###### ***** Following Function calculate the outflow of groundwater based on water system decesion maker *****#####
def SUSTAINABLEWITHDRAWAL(SPECIFICSTORAGE,AREA,DELTAH,RAINFALL,QRETURNF,CW,QRETURNFC):
                         QOUTGW = 0 
                         DT = 30 * 24 * 3600
                         QAQUIFER = (SPECIFICSTORAGE * AREA * 1000000 * DELTAH)/DT
                         QOUTGW = 0.5 * (QAQUIFER + CW * RAINFALL  + QRETURNF * QRETURNFC)
                         
                         return QOUTGW
#-------------------------------------------------------------------------
###### ****** Fllowing Function calculate storage and head of groundwater
def STORAGE(QRETURNF,QOUTGW,RAINFALL,QINTERACTION,CW,QRETURNFC,WW):
           
           DELTASTORAGE = 0
           DT = 30 * 24 * 3600
           DELTASTORAGE =  QRETURNF *QRETURNFC* DT + CW*RAINFALL * DT - WW*QOUTGW * DT + QINTERACTION * DT 
           return DELTASTORAGE
# ----------------------------------------------------------------------------
# Call Functions 
# for i in range(0,u):
#     kriv[0,i] = KRIV(f,k[0,i],Lriver[0,i]) 

        
      
# head[0,:] = [3,5,4,2]
# for i in range(0,u):
#     for j in range(0,m-1):
#         # Determine Initial Boundary
#         if j == 0 :
#             # head[0,i] = 3        # initial head of each aquifer 
#             storage[0,i] = 100000000           # initial storage
#             qOutGW[0,i] = 0                  # initial outflow from aquifer in time step 1
#             qInteraction[0,i] = 0.0
#             deltastorage[j+1,i] = STORAGE(qReturnF[j,i],qOutGW[j,i],Rainfall[j,i],qInteraction[0,i],Cw[i],qRetrunrFC[i])
#             storage[j+1,i] = deltastorage[j+1,i] + storage[j,i]
#             deltaH[j+1,i] = deltastorage[j+1,i] / (area[0,i] *1000000 * SpecificS[0,i] )     #Calculate Groundwater head in each
#             head[j+1,i] = deltaH[j+1,i] + head[j,i]     # Calculate head of each user in different time()
#             qInteraction[j+1,i] = DARCY(kriv[0,i],Taraz[j+1,i],WaterLevel[j,i],riverbed[i],RiverAreaPercentages[i])
           
            
            
#         if j > 0 :
            
#             qOutGW[j,i] = SUSTAINABLEWITHDRAWAL(SpecificS[0,i],area[0,i],deltaH[j,i],Rainfall[j,i],qReturnF[j,i],Cw[i],qRetrunrFC[i])
#             qInteraction[j,i] = DARCY(kriv[0,i],Taraz[j,i],WaterLevel[j,i],riverbed[i],RiverAreaPercentages[i])
#             deltastorage[j+1,i] = STORAGE(qReturnF[j,i],qOutGW[j,i],Rainfall[j,i], qInteraction[j,i],Cw[i],qRetrunrFC[i])
#             storage[j+1,i] = deltastorage[j+1,i] + storage[j,i]
#             deltaH[j+1,i] = deltastorage[j+1,i] / (area[0,i] *1000000* SpecificS[0,i])
#             head[j+1,i] = deltaH[j+1,i] + head[j,i] 


        
            
                    
# # --------------------------------------------------------------------------------
# Plot  head of aquifers
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# Create t and x as shape head
# t = np.arange(1, 5, 1)
# x = np.arange(0, 120, 1)
# t, x = np.meshgrid(t, x)

# Plot the surface.
# surf = ax.plot_surface(t, x,head, cmap=cm.coolwarm,
#                         linewidth=0, antialiased=False)
# Customize the z axis.
# ax.set_zlim(0,20)
# ax.zaxis.set_major_locator(LinearLocator(6))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.75, aspect=60)
# plt.show()


# Plot Head over Time
# tt = np.linspace(0,120,120)
# plt.plot(tt,head[:,3])
# plt.legend(["Head1", "Head2","Head3","Head4"], loc ="upper right") 
# plt.xlabel('time(month)')
# plt.ylabel('Head(m)')
# plt.show()
    

                    