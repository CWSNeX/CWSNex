# Name:       Water Simulation Model  
# Purpose:    Run All Developed Modules 
#
# Author:     Elham Soleimanian
#
# Created:     05/1/2021
# -------------------------------------------------------------------------
# Import Libraries 
import numpy as np
import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt
# ------------------------------------------------------------------------
# Import all Developed Modules 
import Evaporation
from Evaporation import * 
from RoutingKinimaticwithoutinterflowandConsumer1 import *
from RoutingKinimaticforInterflows import *
from ReserviorOutflow import * 
from GroundwaterRevised  import *
from SurfaceWaterAllocation import * 

def WSMN(TIMESTEP,NOS,NOP, SAMPLINGMATRIX,OBSERVATION,OBSERVATIONHEAD,W):
    
    """
    This function calculate river discharge by routing and using 5 other modules 
    : param nos: Total number of simulations
    : param samplingmatrix: LHS matrix
    : param observedtds: Observed TDS file
    
    :return: objective_function: Values of objective function for each simulation
    :return: varf: Variance of objective function values
    :return: xstar: Row of lhs values which has (minimum/maximum)
    :return: q
    """ 
    # Import Data 
    # Import Demand From Main River To Extract Shape of Modules
    data = pd.ExcelFile(r'D:\My Code New\DataBank\AllocationDemand.xlsx')
    AgrDemand = pd.read_excel(data, 'AgrMain',usecols='B:AO').to_numpy()
    [a,r] = AgrDemand.shape  
    # Import Demand From Interflows To Extract Shape of Modules 
    data1 = pd.ExcelFile(r'D:\My Code New\DataBank\AllocationDemand.xlsx')
    AgrInterflow = pd.read_excel(data1, 'AgrInt',usecols='B:BA').to_numpy()
    [aa,rr] = AgrInterflow.shape 
    # Import Return flow from Food and Energy to River 
    # ReturnFoodtoRiver = pd.read_excel(data, 'ReturnfromFoodtoRiver',usecols='B:BO').to_numpy()
    # RetuenEnergytoRiver = pd.read_excel(data, 'ReturnfromEnergytoRiver',usecols='B:BO').to_numpy()
    # # Import Return flow from Food and Energy to Interflows
    # ReturnFoodtoRiverInt = pd.read_excel(data1, 'returnflowfromFood',usecols='B:BA').to_numpy()
    # ReturnEnergytoRiverInt = pd.read_excel(data1, 'returnflowfromEnergy',usecols='B:BA').to_numpy()
    # Import Withdrawal from Groundwater for Food System
    # FoodWGW = pd.read_excel(data, 'FoodfromGW',usecols='B:BO').to_numpy()
    # Import Return flow from Food System to Groundwater 
    # ReturnFoodtoGW = pd.read_excel(data, 'ReturnfromFoodtoGW',usecols='B:BO').to_numpy()
    # ------------------------------------------------------------------------------------
    #
    # Preallocation 
    # qOutFinall Shows the finall amount of water in River( after calculating balance equation)
    # Evaporation Module
    E = np.zeros((NOS,TIMESTEP,uE))
    Eva = np.zeros((NOS,TIMESTEP,r))
    # River Routing
    y = np.zeros((NOS,TIMESTEP,r))
    p = np.zeros((NOS,TIMESTEP,r))
    alpha = np.zeros((NOS,TIMESTEP,r))
    qOut = np.zeros((NOS,TIMESTEP,r))
    WaterLevel = np.zeros((NOS,TIMESTEP,4)) 
    FoodWRiver = np.zeros((NOS,TIMESTEP,r)) 
    EnergyWRiver = np.zeros((NOS,TIMESTEP,r))
    ReturnFoodtoRiver = np.zeros((NOS,TIMESTEP,r))
    ReturnEnergytoRiver = np.zeros((NOS,TIMESTEP,r))
    # Interflow Routing
    k = 52
    uu = 1
    yInt = np.zeros((NOS,TIMESTEP,k))
    pInt = np.zeros((NOS,TIMESTEP,k))
    alphaInt = np.zeros((NOS,TIMESTEP,k)) 
    qOutInt = np.zeros((NOS,TIMESTEP,k))
    EvaInt = np.zeros((NOS,TIMESTEP,k)) 
    FoodWRiverInt = np.zeros((NOS,TIMESTEP,k)) 
    EnergyWRiverInt = np.zeros((NOS,TIMESTEP,k))
    ReturnFoodtoRiverInt = np.zeros((NOS,TIMESTEP,k))
    ReturnEnergytoRiverInt = np.zeros((NOS,TIMESTEP,k))
    
    
    # Reservior Routing
    qResOut = np.zeros((NOS,TIMESTEP,uR))
    qResOutF = np.zeros((NOS,TIMESTEP,r))
    F = np.zeros((NOS,TIMESTEP,uR))
    EvaRes = np.zeros((NOS,TIMESTEP,uR))
    st = np.zeros((NOS,TIMESTEP,uR))
    rel = np.zeros((NOS,uR))
    res = np.zeros((NOS,uR))
    vol = np.zeros((NOS,uR))
    sus = np.zeros((NOS,uR))
    h = np.zeros((NOS,TIMESTEP,uR))
    A = np.zeros((NOS,TIMESTEP,uR))
    Alpha = np.zeros((NOS,1,uR))
    
    # Groundwater Module
    
    LocGW = [0,1,2,3]
    f = 1
    qInteraction = np.zeros((NOS,TIMESTEP,u))
    qInteractionF = np.zeros((NOS,TIMESTEP,r))
    qOutGW = np.zeros((NOS,TIMESTEP,u))
    deltastorage = np.zeros((NOS,TIMESTEP,u))
    storage = np.zeros((NOS,TIMESTEP,u))
    head = np.zeros((NOS,TIMESTEP,u))
    kriv = np.zeros((NOS,1,u))
    deltaH = np.zeros((NOS,TIMESTEP,u))
    # WSMN Module
    
    qOutFinall =  np.zeros((NOS,TIMESTEP,r))
    qOutIntFinall =  np.zeros((NOS,TIMESTEP,k))
    qOutFinallCode  = np.zeros((TIMESTEP,r))
    DISCHARGESIMULATED = np.zeros((NOS,TIMESTEP,3))
    HEADSIMULATED = np.zeros((NOS,TIMESTEP,4))
    objective_function = np.zeros((NOS,1,7)) 
    objective_functionW = np.zeros((NOS,1,7))
    objective_functionWS = np.zeros((NOS,1,1))
    beta = 0.6
    dt = 30 * 24 * 3600    
    # --------------------------------------------------------------------------------------
    # **********************  Call Desiarable Function  *********************#
###############################################################################
    
    # Call Evaporation
    for jnos in range(0,NOS):
        for i in range(0,1):
            for j in range(0,TIMESTEP):
                E[jnos,j,i] = MayerEvaporation(Wvelocity[j,i],SAMPLINGMATRIX[jnos,0],Ssp[j,i],Sp[j,i])
    # # reapeat calculated Evaporation for all Locations
    # # for jnos in range(0,NOS):
    # #     for i in range(0,r):
    # #         for j in range(0,TIMESTEP): 
    # #             Eva[jnos,j,i] = E[jnos,j,0] 
    # # reapeat calculated Evaporation for all Locations
    for i in range(0,r):
        if i>=29 and i <=32:
            Eva[:,:,i] = E[:,:,0] * (1000 * 560)/(1000 * 24 * 3600)
        else:
            Eva[:,:,i] = E[:,:,0] * (1000 * 11)/(1000 * 24 * 3600)
    # Repeat Evaporation for Interflows 
    for i in range(0,k):
        EvaInt[:,:,i] = E[:,:,0] * ( 1000 * 6)/(1000 * 24 * 3600)
    # Extract Evaporation for Using in Reservoir Module
    EvaRes[:,:,0] = Eva[:,:,30]
    # m3/mon
    1 == 1 
###################################################################################       
    #Call River Routing for Main River 
    for jnos in range(0,NOS):
        for i in range(0,40):
            for j in range(0,TIMESTEP):
                if i == 0 and j>=0:
                    qOut[jnos,j,0] = qInitialInput[j,0]
                    y[jnos,j,i] = (( qOut[jnos,j,i]*SAMPLINGMATRIX[jnos,2])/( b * sqrt(SAMPLINGMATRIX[jnos,3])))**(3/5)
                    p[jnos,j,i]= b + 2 * y[jnos,j,i]
                    alpha[jnos,j,i] = ((SAMPLINGMATRIX[jnos,2] * p[jnos,j,i]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,3]))**beta
                elif j == 0 and i>0: 
                    qOut[jnos,0,i]= SAMPLINGMATRIX[jnos,1]
                    y[jnos,j,i] = (( qOut[jnos,j,i]*SAMPLINGMATRIX[jnos,2])/( b * sqrt(SAMPLINGMATRIX[jnos,3])))**(3/5)
                    p[jnos,j,i]= b + 2 * y[jnos,j,i]
                    alpha[jnos,j,i] = ((SAMPLINGMATRIX[jnos,2] * p[jnos,j,i]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,3]))**beta
                
    for jnos in range(0,NOS):            
        for i in range(0,40-1):
            for j in range(0,TIMESTEP-1): #??????????????????????????????
                qOut[jnos,j+1,i+1] = routing(alpha[jnos,j,i],beta,qOut[jnos,j+1,i],qOut[jnos,j,i+1],dx,dt)
                y[jnos,j+1,i+1] = (( qOut[jnos,j+1,i+1]*SAMPLINGMATRIX[jnos,2])/( b * sqrt(SAMPLINGMATRIX[jnos,3])))**(3/5)
                p[jnos,j+1,i+1]= b + 2 * y[jnos,j,i+1]
                alpha[jnos,j+1,i+1] = ((SAMPLINGMATRIX[jnos,2] * p[jnos,j,i+1]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,3]))**beta
    # #             ###############????????????debi update
    # # # Determine Water Level in Each Aquifer Section
    for jnos in range(0,NOS):
        WaterLevel[jnos,:,0] = y[jnos,:,7] + 1410
        WaterLevel[jnos,:,1] = y[jnos,:,24] + 1296
        WaterLevel[jnos,:,2] = y[jnos,:,31] + 1314
        WaterLevel[jnos,:,3] = y[jnos,:,38] + 1278
    1 ==1
###############################################################################         
    # # Call Interflows
    for jnos in range(0,NOS):
        for ii in range(0,uu):
            if ii == 0:
                for i in range(0,k):
                    for j in range(0,TIMESTEP):
                        if i == 0 and j>=0:
                            qOutInt[jnos,j,0] = qInter[j,ii]
                            yInt[jnos,j,i] = (( qOutInt[jnos,j,i]*SAMPLINGMATRIX[jnos,5])/( bInt[ii,0] * sqrt(SAMPLINGMATRIX[jnos,6])))**(3/5)
                            pInt[jnos,j,i]= bInt[ii,0] + 2 * yInt[jnos,j,i]
                            alphaInt[jnos,j,i] = ((SAMPLINGMATRIX[jnos,5] * pInt[jnos,j,i]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,6]))**beta
                        elif j == 0 and i>0: 
                            qOutInt[jnos,0,i]= SAMPLINGMATRIX[jnos,4]
                            yInt[jnos,j,i] = (( qOutInt[jnos,j,i]*SAMPLINGMATRIX[jnos,5])/( bInt[ii,0] * sqrt(SAMPLINGMATRIX[jnos,6])))**(3/5)
                            pInt[jnos,j,i]= bInt[ii,0] + 2 * yInt[jnos,j,i]
                            alphaInt[jnos,j,i] = ((SAMPLINGMATRIX[jnos,5] * pInt[jnos,j,i]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,6]))**beta
                            
            # if there is another Interlow
            # if ii == 1:            
            #     for i in range(13,k):
            #     # if ii == 1:
            #         for j in range(0,TIMESTEP):
            #             if i == 13 and j>=0:
            #                 qOutInt[jnos,j,i] = qInter[j,ii]
            #                 yInt[jnos,j,i] = (( qOutInt[jnos,j,i]*SAMPLINGMATRIX[jnos,8])/( bInt[ii,0] * sqrt(SAMPLINGMATRIX[jnos,9])))**(3/5)
            #                 pInt[jnos,j,i]= bInt[ii,0] + 2 * yInt[jnos,j,i]
            #                 alphaInt[jnos,j,i] = ((SAMPLINGMATRIX[jnos,8] * pInt[jnos,j,i]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,9]))**beta
            #             elif j == 0 and i>13: 
                            # qOutInt[jnos,0,i]= SAMPLINGMATRIX[jnos,4]
                            # yInt[jnos,j,i] = (( qOutInt[jnos,j,i]*SAMPLINGMATRIX[jnos,5])/( bInt[ii,0] * sqrt(SAMPLINGMATRIX[jnos,6])))**(3/5)
                            # pInt[jnos,j,i]= bInt[ii,0] + 2 * yInt[jnos,j,i]
                            # alphaInt[jnos,j,i] = ((SAMPLINGMATRIX[jnos,5] * pInt[jnos,j,i]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,6]))**beta
    1 == 1                     
    for jnos in range(0,NOS):                        
        for ii in range(0,uu):
            for i in range(0,k):
                if ii == 0 and i < k-1:
                    for j in range(0,TIMESTEP-1):
                        qOutInt[jnos,j+1,i+1] = routing(alphaInt[jnos,j,i],beta,qOutInt[jnos,j+1,i],qOutInt[jnos,j,i+1],dxInt,dt)
                        yInt[jnos,j+1,i+1] = (( qOutInt[jnos,j+1,i+1]*SAMPLINGMATRIX[jnos,5])/( bInt[ii,0] * sqrt(SAMPLINGMATRIX[jnos,6])))**(3/5)
                        pInt[jnos,j+1,i+1]= bInt[ii,0] + 2 * yInt[jnos,j,i+1]
                        alphaInt[jnos,j+1,i+1] = ((SAMPLINGMATRIX[jnos,5] * pInt[jnos,j,i+1]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,6]))**beta
   
                # if there is another Interlow
                        
                # if ii == 1 and 12< i < 66:
                #     for j in range(0,TIMESTEP-1):
                #         qOutInt[jnos,j+1,i+1] = routing(alphaInt[jnos,j,i],beta,qOutInt[jnos,j+1,i],qOutInt[jnos,j,i+1],dxInt,dt)
                #         yInt[jnos,j,i+1] = (( qOutInt[jnos,j+1,i+1]*SAMPLINGMATRIX[jnos,8])/( bInt[ii,0] * sqrt(SAMPLINGMATRIX[jnos,9])))**(3/5)
                #         pInt[jnos,j,i+1]= bInt[ii,0] + 2 * yInt[jnos,j,i+1]
                #         alphaInt[jnos,j,i+1] = ((SAMPLINGMATRIX[jnos,8] * pInt[jnos,j,i+1]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,9]))**beta
              
###############################################################################    
    # Call Outflow from Reserviors 
    # Call LISFLOOD
    # for jnos in range(0,NOS):
    #     for i in range (0,uR):
    #         for j in range(0,TIMESTEP-1):
    #             st[jnos,0,i] = SAMPLINGMATRIX[jnos,7
    #             st[jnos,j+1,i],qResOut[jnos,j,i] = Lisflood(st[jnos,j,i],Q_min[j,i],dt,F[jnos,j,i],storageR[0,i],l_c[i,0],Q_norm[j,i],l_n[i,0],l_f[i,0],qResin[j,i],Q_nonD[j,i],EvaRes[jnos,j,0])
    #             
    #             
    1 == 1       
    # Call SOP
    for jnos in range(0,NOS):
        for i in range(0,uR):
            for j in range(0,TIMESTEP-1):  #????????????????????????????
                st[jnos,0,i] =  SAMPLINGMATRIX[jnos,8 ]
                st[jnos,j+1,i],qResOut[jnos,j,i] = SOP(st[jnos,j,i],qResin[j,i],targetRelase[j,i],ka[0,i],sMin[0,i],dt,EvaRes[jnos,j,0])
                
    for jnos in range(0,NOS):
        for i in range(0,uR):
            rel[jnos,i] = ReliabilitySOP(qResOut[jnos,:,i],targetRelase[:,i],TIMESTEP)
            res[jnos,i] = RESELIENCESOP(qResOut[jnos,:,i],targetRelase[:,i],TIMESTEP)
            vol[jnos,i] = VolnurabilitySOP(qResOut[jnos,:,i],targetRelase[:,i],TIMESTEP)
            sus[jnos,i] = SUSTAINABILITY(rel[jnos,i],res[jnos,i],vol[jnos,i])
    # for LISFLOOD Method 
    #         rel[jnos,i] = ReliabilityLISFLOOD(qResOut[jnos,:,i],Q_norm[:,i],TIMESTEP)
    #         res[jnos,i] = RESELIENCELISFLOOD(qResOut[jnos,:,i],Q_norm[:,i],TIMESTEP)
    #         vol[jnos,i] = VolnurabilityLISFLOOD(qResOut[jnos,:,i],Q_norm[:,i],TIMESTEP)
    #         sus[jnos,i] = SUSTAINABILITY(rel[jnos,i],res[jnos,i],vol[jnos,i])
            
    # Calculate Head
    
    for jnos in range(0,NOS):
        for i in range(0,uR):
            for j in range(0,TIMESTEP-1):
                h[jnos,j,i]  = HEAD(st[jnos,j,i])
                 
    # # reapeat calculated Outflow for all Locations                    
    qResOutF[:,:,4] = qResOut[:,:,0]
    1 == 1        
###############################################################################                
    # Call Groundwater Storage and Head
    for jnos in range(0,NOS):  
        for i in LocGW: 
            kriv[jnos,0,i] = KRIV(f,SAMPLINGMATRIX[jnos,LocGW.index(i)+25],Lriver[0,i]) 
    # Set Initial Boundary 
        
            head[jnos,0,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+9]
            storage[jnos,0,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+13]
            qOutGW[jnos,0,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+17]
            qInteraction[jnos,0,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+21]

    for jnos in range(0,NOS):  
        for i in range(0,u):
            for j in range(0,TIMESTEP-1):
                if j == 0 :
                    deltastorage[jnos,j+1,i] = STORAGE(qReturnF[j,i],qOutGW[jnos,j,i],Rainfall[j,i], qInteraction[jnos,0,i])
                    storage[jnos,j+1,i] = deltastorage[jnos,j+1,i] + storage[jnos,j,i]
                    deltaH[jnos,j+1,i] = deltastorage[jnos,j+1,i] / (area[0,i] *1000000* SAMPLINGMATRIX[jnos,LocGW.index(i)+29])     #Calculate Groundwater head in each
                    head[jnos,j+1,i] = deltaH[jnos,j+1,i] + head[jnos,j,i]     # Calculate head of each user in different time()
                    qInteraction[jnos,j+1,i] = DARCY(kriv[jnos,0,i],head[jnos,j+1,i],WaterLevel[jnos,j,i],riverbed[i],RiverAreaPercentages[i])
                    
                
                
                if j > 0 :
                    
                    qOutGW[jnos,j,i] = SUSTAINABLEWITHDRAWAL(SAMPLINGMATRIX[jnos,LocGW.index(i)+29],area[0,i],deltaH[jnos,j,i],Rainfall[j,i],qReturnF[j,i])
                    qInteraction[jnos,j,i] = DARCY(kriv[jnos,0,i],head[jnos,j,i],WaterLevel[jnos,j,i],riverbed[i],RiverAreaPercentages[i])
                    deltastorage[jnos,j+1,i] = STORAGE(qReturnF[j,i],qOutGW[jnos,j,i],Rainfall[j,i], qInteraction[jnos,j,i])
                    storage[jnos,j+1,i] = deltastorage[jnos,j+1,i] + storage[jnos,j,i]
                    deltaH[jnos,j+1,i] = deltastorage[jnos,j+1,i] / (area[0,i] *1000000* SAMPLINGMATRIX[jnos,LocGW.index(i)+29])
                    head[jnos,j+1,i] = deltaH[jnos,j+1,i] + head[jnos,j,i]
                  
    1 == 1
    # reapeat calculated qInteraction for all Locations
    for i in range(0,r):
        
        if i < 8:                
            qInteractionF[:,:,i] = qInteraction[:,:,0]/8000*1000 
        if 8 <=i < 25:
            qInteractionF[:,:,i] = qInteraction[:,:,1]/17000*1000 
        if 25<= i < 32:
            qInteractionF[:,:,i] = qInteraction[:,:,2]/7000*1000 
        if 32 <= i < 39:
            qInteractionF[:,:,i] = qInteraction[:,:,3]/7000*1000 
###############################################################################                
    # Calculate Balance Equation for Interflows Based On Allocated Water Which Calculate on SurfaceWaterAllocation
    1 == 1
    for jnos in range(0,NOS):  
        for i in range (0,k):
            for j in range(0,TIMESTEP):
                qOutIntFinall[jnos,j,i] = qOutInt[jnos,j,i] - EvaInt[jnos,j,i]
                if qOutIntFinall[jnos,j,i] < 0 :
                    qOutIntFinall[jnos,j,i] = 0
                FoodWRiverInt[jnos,j,i] = AGRICULTUREALLOCATION(qOutIntFinall[jnos,j,i],DEInter[j,i],EnergyDemandMinInt[j,i],TDInter[j,i],AgrInterflow[j,i],AgrPFinallInt[j,0],1)
                EnergyWRiverInt[jnos,j,i] = ENERGYALLOCATION(qOutIntFinall[jnos,j,i],DEInter[j,i],EnergyDemandMinInt[j,i],TDInter[j,i],EnergyDemandMaxInt[j,i],EnergyPFinallInt[j,0])
                ReturnFoodtoRiverInt[jnos,j,i] = 0.2 * FoodWRiverInt[jnos,j,i]
                ReturnEnergytoRiverInt[jnos,j,i] = 0.15 * EnergyWRiverInt[jnos,j,i]
                qOutIntFinall[jnos,j,i:] =  qOutIntFinall[jnos,j,i:]  - FoodWRiverInt[jnos,j,i]  - EnergyWRiverInt[jnos,j,i] + ReturnFoodtoRiverInt[jnos,j,i] + ReturnEnergytoRiverInt[jnos,j,i] 
            
    1==1
    # If there is more than one Interflow they should be seprated cause different location they enter to Main River
    # for jnos in range(0,NOS):  
    #     for i in range (0,k):
    #         if i < 12:
    #             for j in range(0,TIMESTEP):
    #                 qOutIntFinall1[jnos,j,i] = qOutIntFinall[jnos,j,i]
    #         if i > 12: 
    #             for j in range(0,TIMESTEP):
    #                 qOutIntFinall2[jnos,j,i] = qOutIntFinall[jnos,j,i]
    

###############################################################################
    # Calculate Balance Equation for Main River
    for jnos in range(0,NOS):
        for i in range(0,r):
           for j in range(0,TIMESTEP):
                    # if qResOutF[jnos,j,i]>0:
                    if i >= 4:
                        qResOutF[jnos,j,i] = qResOutF[jnos,j,i] + qOutIntFinall[jnos,j,i] -  Eva[jnos,j,i]  - qInteractionF[jnos,j,i] 
                        if qResOutF[jnos,j,i] < 0:
                            qResOutF[jnos,j,i] = 0
                        FoodWRiver[jnos,j,i] = AGRICULTUREALLOCATION(qResOutF[jnos,j,i],DE[j,i],EnergyDemandMin[j,i],TD[j,i],AgrDemand[j,i],AgrPFinall[j,0],agrfactor[j,i])
                        EnergyWRiver[jnos,j,i] = ENERGYALLOCATION(qResOutF[jnos,j,i],DE[j,i],EnergyDemandMin[j,i],TD[j,i],EnergyDemandMax[j,i],EnergyPFinall[j,0])
                        ReturnFoodtoRiver[jnos,j,i] = 0.2 * FoodWRiver[jnos,j,i]
                        ReturnEnergytoRiver[jnos,j,i] =  0.1 * EnergyWRiver[jnos,j,i]
                        qOutFinall[jnos,j,i:] = qResOutF[jnos,j,i:] - FoodWRiver[jnos,j,i] - EnergyWRiver[jnos,j,i] + ReturnFoodtoRiver[jnos,j,i] + ReturnEnergytoRiver[jnos,j,i]   
                        
                    # if qResOutF[jnos,j,i] == 0 : 
                    else:
                        
                        qOutFinall[jnos,j,i] =  qOut[jnos,j,i] + qOutIntFinall[jnos,j,i] - Eva[jnos,j,i]  - qInteractionF[jnos,j,i]
                        if qOutFinall[jnos,j,i] < 0:
                            qOutFinall[jnos,j,i] = 0
                        FoodWRiver[jnos,j,i] = AGRICULTUREALLOCATION(qOutFinall[jnos,j,i],DE[j,i],EnergyDemandMin[j,i],TD[j,0],AgrDemand[j,i],AgrPFinall[j,0],agrfactor[j,i])
                        EnergyWRiver[jnos,j,i] = ENERGYALLOCATION(qOutFinall[jnos,j,i],DE[j,i],EnergyDemandMin[j,i],TD[j,i],EnergyDemandMax[j,i],EnergyPFinall[j,0])
                        ReturnFoodtoRiver[jnos,j,i] = 0.2 * FoodWRiver[jnos,j,i]
                        ReturnEnergytoRiver[jnos,j,i] =  0.1 * EnergyWRiver[jnos,j,i]
                        qOutFinall[jnos,j,i:] = qOutFinall[jnos,j,i:] - FoodWRiver[jnos,j,i] - EnergyWRiver[jnos,j,i] + ReturnFoodtoRiver[jnos,j,i] + ReturnEnergytoRiver[jnos,j,i]
    1 == 1
         
    # for jnos in range(0,NOS):
    #     for i in range(0,r):
    #        for j in range(0,TIMESTEP):
    #                 # if qResOutF[jnos,j,i]>0:
    #                 if 1 == 1:
    #                     qResOutF[jnos,j,i] = qResOutF[jnos,j,i] + qOutIntFinall[jnos,j,i] -  Eva[jnos,j,i]  - qInteractionF[jnos,j,i] 
    #                     if qResOutF[jnos,j,i] < 0:
    #                         qResOutF[jnos,j,i] = 0
    #                     FoodWRiver[jnos,j,i] = AGRICULTUREALLOCATION(qResOutF[jnos,j,i],DE[j,i],EnergyDemandMin[j,i],TD[j,i],AgrDemand[j,i],AgrPFinall[j,0],agrfactor[j,i])
    #                     EnergyWRiver[jnos,j,i] = ENERGYALLOCATION(qResOutF[jnos,j,i],DE[j,i],EnergyDemandMin[j,i],TD[j,i],EnergyDemandMax[j,i],EnergyPFinall[j,0])
    #                     ReturnFoodtoRiver[jnos,j,i] = 0.2 * FoodWRiver[jnos,j,i]
    #                     ReturnEnergytoRiver[jnos,j,i] =  0.1 * EnergyWRiver[jnos,j,i]
    #                     qOutFinall[jnos,j,i:] = qResOutF[jnos,j,i:] - FoodWRiver[jnos,j,i] - EnergyWRiver[jnos,j,i] + ReturnFoodtoRiver[jnos,j,i] + ReturnEnergytoRiver[jnos,j,i]   
                        

###############################################################################            
    
    # # Calculate Objective Function 
###############################################################################
    for jnos in range(0,NOS):
        DISCHARGESIMULATED[jnos,:,0] = qOutFinall[jnos,:,6]
        DISCHARGESIMULATED[jnos,:,1] = qOutFinall[jnos,:,8]
        DISCHARGESIMULATED[jnos,:,2] = qOutFinall[jnos,:,31]
        HEADSIMULATED[jnos,:,0 ] = head[jnos,:,0]
        HEADSIMULATED[jnos,:,1 ] = head[jnos,:,1]
        HEADSIMULATED[jnos,:,2 ] = head[jnos,:,2]
        HEADSIMULATED[jnos,:,3 ] = head[jnos,:,3]
        
    1 == 1
    
    for jnos in range(0,NOS):
        for i in range(0,3):
            # Each Station Has Equal Value on Wighted RMSE 
            objective_function[jnos,0,i] = np.sqrt((np.nansum((OBSERVATION[:,i] -DISCHARGESIMULATED[jnos,:,i]) ** 2,axis = 0))/(np.count_nonzero(~np.isnan(OBSERVATION[:,i]),axis=0)))
            
    for jnos in range(0,NOS):
        for i in range(0,4):
            # Each Location of Aquifer Has Equal Value on Wighted RMSE 
            objective_function[jnos,0,i+3] = np.sqrt((np.nansum((OBSERVATIONHEAD[:,i] - HEADSIMULATED[jnos,:,i]) ** 2,axis = 0))/(np.count_nonzero(~np.isnan(OBSERVATIONHEAD[:,i]),axis=0)))
            
    for jnos in range(0,NOS):             
        for i in range(0,7):
            objective_functionW[jnos,0,i] = W[0,i]*objective_function[jnos,0,i]
    for jnos in range(0,NOS): 
        objective_functionWS[jnos,0,0] =  objective_functionW[jnos,0,:].sum(axis=0, keepdims =True)
   
             
    1 == 1           
    ############################# axis = 2 ????????????????????????????????????????????    
    objective_function = objective_function[:,0,:]
    objective_functionW = objective_functionW[:,0,:]
    objective_functionWS = objective_functionWS[:,0,0]
  
               
    #Calculate Variance of Objective Function with Delta Degree of Freedom of 0                 
    varf = np.var(objective_functionWS, ddof=0)  
    # Recognize of Index for Min of RMSE  
    bb = objective_functionWS.argmin()

   
    # Determine Best Parametres in Sampling Matrix Rows
    xstar = SAMPLINGMATRIX[bb,:]
    
    
    # # In Following Q is calculated for TDS Routing 
    # All Nodes Which Consist AGriculture Withdrawal, Returnflow and Reserviors and Interflows
    # Are Considered In Mass Balance Madule As New Nodes, So In Balance Equation they should be Eliminated             
    for i in range(0,40):
        for j in range(0,TIMESTEP):
           
            qOutFinallCode[j,i] =  qOut[bb,j,i]  - Eva[bb,j,i] - EnergyWRiver[bb,j,i]  + ReturnEnergytoRiver[bb,j,i] - qInteractionF[bb,j,i]
    # Write In Balance Excel for TDS Routing
    app = xw.App(visible=True)
    wb = xw.Book('D:\My Code New\DataBank\BalanceEquation.xlsx')  
    # sht = wb.sheets['qOutFinall']
    sht2 = wb.sheets['qOutFinallCode'] 
    # to Write Output of Model for xstar     
    # sht.range('B2:AO2').value = Eva[bb,:,:] 
    sht2.range('B3:AO3').value = qOutFinallCode    
    
    return objective_function,objective_functionW,objective_functionWS, varf, xstar, qOutFinall,DISCHARGESIMULATED,HEADSIMULATED
    1 == 1 
# t = np.linspace(0,12,12)   
# plt.plot(t,qOutFinall)
# plt.legend(["qOutFinall1", "qOutFinall2","qOutFinall3"], loc ="upper right") 
# plt.xlabel('time(Month)')
# plt.ylabel('qOutFinall(Mm3)')
# plt.show()