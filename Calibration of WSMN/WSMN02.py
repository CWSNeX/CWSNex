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
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
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
    ert0=SAMPLINGMATRIX
    
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
    # ---------------------------------------------------------------------------------------
    #*************************************************************************#
    #*************************************************************************#
    # Import Related Data for Base Years
    # Import Withrrawal from Main River for Food and Energy in Base Years
    # ********************Turn On Below Lines *******************************#
    data2= pd.ExcelFile(r'D:\My Code New\DataBank\WithdrawalforBaseYear.xlsx')
    data3 = pd.read_excel(data2, 'Food',usecols='B:AO').to_numpy()
    data4 = pd.read_excel(data2, 'Energy',usecols='B:AO').to_numpy()
    data6= pd.ExcelFile(r'D:\My Code New\DataBank\DomesticUse.xlsx')
    domestic = pd.read_excel(data6, 'Sheet1',usecols='B:AO').to_numpy()
    data7= pd.ExcelFile(r'D:\My Code New\DataBank\IndustrialWithdrawal.xlsx')
    Indus = pd.read_excel(data7, 'Sheet1',usecols='B:AO').to_numpy()
    # RetuenEnergytoRiver = pd.read_excel(data, 'ReturnfromEnergytoRiver',usecols='B:BO').to_numpy()
    # --------------------------------------------------------------------------------------
    # Import Withdrawal from Groundwater for Food System and Industary in Base Years
    # ********************Turn On Below Lines *******************************#
    data5= pd.ExcelFile(r'D:\My Code New\DataBank\GWWithdrawalforBaseYear.xlsx')
    FoodWGW = pd.read_excel(data5, 'Food',usecols='B:E').to_numpy()
    # Attention, It is assumed that there is no withdrawal from GW for Energy
    # Import Withdrawal from Groundwater for Industerial in Base Years
    IndusWGW = pd.read_excel(data5, 'Indus',usecols='B:E').to_numpy()
    # ------------------------------------------------------------------------------------
    # Import Withrrawal from Interflow for Food and Energy in Base Years
    data8 = pd.ExcelFile(r'D:\My Code New\DataBank\WithdrawalforBaseYearInterflow.xlsx')
    data9 = pd.read_excel(data8, 'Food',usecols='B:BA').to_numpy()
    data10 = pd.read_excel(data8, 'Indus',usecols='B:BA').to_numpy()
    # ReturnEnergytoRiverInt = pd.read_excel(data1, 'returnflowfromEnergy',usecols='B:BA').to_numpy()
    
    #*************************************************************************#
    #*************************************************************************#
    # Preallocation 
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
    Domestic =  np.zeros((NOS,TIMESTEP,r))
    Induss =  np.zeros((NOS,TIMESTEP,r))
    EnergyWRiver = np.zeros((NOS,TIMESTEP,r))
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
    IndussInt = np.zeros((NOS,TIMESTEP,k))
    EnergyWRiverInt = np.zeros((NOS,TIMESTEP,k))
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
    cw = np.zeros((NOS,TIMESTEP,4))
    ww = np.zeros((NOS,TIMESTEP,4))
    qReturnFC = np.zeros((NOS,TIMESTEP,4))
    qOutGW = np.zeros((NOS,TIMESTEP,u))
    deltastorage = np.zeros((NOS,TIMESTEP,u))
    storage = np.zeros((NOS,TIMESTEP,u))
    head = np.zeros((NOS,TIMESTEP,u))
    kriv = np.zeros((NOS,1,u))
    deltaH = np.zeros((NOS,TIMESTEP,u))
    head11 = np.zeros((TIMESTEP,u))
    Tarazz = np.zeros((NOS,TIMESTEP,u))
    # WSMN
    # qOutFinall Shows the Finall Amount of Water in River( After Calculating Balance Equation)
    qOutFinall =  np.zeros((NOS,TIMESTEP,r))
    qOutIntFinall =  np.zeros((NOS,TIMESTEP,k))
    qComparative = np.zeros((TIMESTEP,2))
    headCom = np.zeros((TIMESTEP,8))
    qResin = np.zeros((NOS,TIMESTEP,uR))
    DISCHARGESIMULATED = np.zeros((NOS,TIMESTEP,1))
    HEADSIMULATED = np.zeros((NOS,TIMESTEP,4))
    objective_function = np.zeros((NOS,1,5)) 
    objective_functionW = np.zeros((NOS,1,5))
    objective_functionWS = np.zeros((NOS,1,1))
    beta = 0.6
    dt = 30 * 24 * 3600    
    # --------------------------------------------------------------------------------------
    # **********************  Call Desiarable Function  *********************#
###############################################################################
    
    # Call Evaporation 
    # Mayer Equation
    for jnos in range(0,NOS):
        for i in range(0,1):
            for j in range(0,TIMESTEP):
                E[jnos,j,i] = MayerEvaporation(Wvelocity[j,i],SAMPLINGMATRIX[jnos,0],Ssp[j,i],Sp[j,i])
                
    # Hamon Equation 
    # for jnos in range(0,NOS):
    #     for i in range(0,1):
    #         for j in range(0,TIMESTEP):
    #             E[jnos,j,i] = Hamon(Temp[j,i])
   
    # # reapeat calculated Evaporation for all Locations and Change Its Unit from mm/day to m3/s ]
    # 1000 * 560 Area of Reservoir
    # 1000 * 6 Area of Each River Section
    # 3 Is the Start Point of Reservior 5 Is the End point of Reservoir
    for i in range(0,r):
        if i>=3 and i <=5:
            Eva[:,:,i] = E[:,:,0] * (1000 * 560)/(1000 * 24 * 3600)
        else:
            Eva[:,:,i] = E[:,:,0] * (1000 * 6)/(1000 * 24 * 3600)
    # Repeat Evaporation for Interflows 
    for i in range(0,k):
        EvaInt[:,:,i] = E[:,:,0] * ( 1000 * 3)/(1000 * 24 * 3600)
    # Extract Evaporation for Using in Reservoir Module
    EvaRes[:,:,0] = Eva[:,:,4]
    # m3/s
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
            if i < (4 - 1):
                for j in range(0,TIMESTEP-1): 
                    qOut[jnos,j+1,i+1] = routing(alpha[jnos,j,i],beta,qOut[jnos,j+1,i],qOut[jnos,j,i+1],dx,dt)
                    y[jnos,j+1,i+1] = (( qOut[jnos,j+1,i+1]*SAMPLINGMATRIX[jnos,2])/( b * sqrt(SAMPLINGMATRIX[jnos,3])))**(3/5)
                    p[jnos,j+1,i+1]= b + 2 * y[jnos,j,i+1]
                    alpha[jnos,j+1,i+1] = ((SAMPLINGMATRIX[jnos,2] * p[jnos,j,i+1]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,3]))**beta
            elif i == (4 - 1):
                # Call Inflow from Reserviors 
                qResin[:,:,0] = qOut[:,:,3]
                
                # Call LISFLOOD to Determine Reservior Outflow
               
                    
                # for jnosr in range(0,NOS):
                #     for ir in range (0,uR):
                #         for jr in range(0,TIMESTEP):
                #             if jr <119:
                
                #                 st[jnosr,0,ir] = SAMPLINGMATRIX[jnosr,7]
                #                 st[jnosr,jr+1,ir],qResOut[jnosr,jr,ir] = Lisflood(st[jnosr,jr,ir],Q_min[jr,ir],dt,F[jnosr,jr,ir],storageR[0,ir],l_c[0,ir],Q_norm[jr,ir],l_n[0,ir],l_f[0,ir],qResin[jnosr,jr,ir],Q_nonD[jr,ir],EvaRes[jnosr,jr,0])
                #             else:
                #                 _,qResOut[jnosr,jr,ir] = Lisflood(st[jnosr,jr,ir],Q_min[jr,ir],dt,F[jnosr,jr,ir],storageR[0,ir],l_c[0,ir],Q_norm[jr,ir],l_n[0,ir],l_f[0,ir],qResin[jnosr,jr,ir],Q_nonD[jr,ir],EvaRes[jnosr,jr,0])
                                
                # # for LISFLOOD Method Calculate Rel,Res,Sus
                # for jnosr in range(0,NOS):
                #     for ir in range(0,uR):
                #         rel[jnosr,ir] = ReliabilityLISFLOOD(qResOut[jnosr,:,ir],Q_norm[:,ir],TIMESTEP)
                #         res[jnosr,ir] = RESELIENCELISFLOOD(qResOut[jnosr,:,ir],Q_norm[:,ir],TIMESTEP)
                #         vol[jnosr,ir] = VolnurabilityLISFLOOD(qResOut[jnosr,:,ir],Q_norm[:,ir],TIMESTEP)
                #         sus[jnosr,ir] = SUSTAINABILITY(rel[jnosr,ir],res[jnosr,ir],vol[jnosr,ir])
                1 == 1       
                # Call SOP to Determine Reservior Outflow
                for jnosr in range(0,NOS):
                    for ir in range(0,uR):
                        for jr in range(0,TIMESTEP):  #????????????????????????????
                            if jr <119:
                                st[jnosr,0,ir] =  SAMPLINGMATRIX[jnosr,8 ]
                                st[jnosr,jr+1,ir],qResOut[jnosr,jr,ir] = SOP(st[jnosr,jr,ir],qResin[jnosr,jr,ir],targetRelase[jr,ir],ka[0,ir],sMin[0,ir],dt,EvaRes[jnosr,jr,0])
                            else:
                                _,qResOut[jnosr,jr,ir] = SOP(st[jnosr,jr,ir],qResin[jnosr,jr,ir],targetRelase[jr,ir],ka[0,ir],sMin[0,ir],dt,EvaRes[jnosr,jr,0])
                for jnosr in range(0,NOS):
                    for ir in range(0,uR):
                        rel[jnosr,ir] = ReliabilitySOP(qResOut[jnosr,:,ir],targetRelase[:,ir],TIMESTEP)
                        res[jnosr,ir] = RESELIENCESOP(qResOut[jnosr,:,ir],targetRelase[:,ir],TIMESTEP)
                        vol[jnosr,ir] = VolnurabilitySOP(qResOut[jnosr,:,ir],targetRelase[:,ir],TIMESTEP)
                        sus[jnosr,ir] = SUSTAINABILITY(rel[jnosr,ir],res[jnosr,ir],vol[jnosr,ir])
                        
                        
               
                        
                # Calculate Head
                for jnosr in range(0,NOS):
                    for ir in range(0,uR):
                        for jr in range(0,TIMESTEP-1):
                            h[jnosr,jr,ir]  = HEAD(st[jnosr,jr,ir])
                             
                # Create 40 * 120 Matrix to Use in Balance Equation                   
                qResOutF[:,:,4] = qResOut[:,:,0]
                1 == 1   
                # for j in range(0,TIMESTEP-1):
                # Where There Is Reservior Dishcharge in River is changed to Reservoir Outflow
                qOut[:,:,4] = qResOut[:,:,0]
                qOut[:,:,5] = qResOut[:,:,0]
             
                    # y[jnos,j+1,i+1] = (( qOut[jnos,j+1,i+1]*SAMPLINGMATRIX[jnos,2])/( b * sqrt(SAMPLINGMATRIX[jnos,3])))**(3/5)
                    # p[jnos,j+1,i+1]= b + 2 * y[jnos,j,i+1]
                    # alpha[jnos,j+1,i+1] = ((SAMPLINGMATRIX[jnos,2] * p[jnos,j,i+1]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,3]))**beta
            elif i >= 5 :
                
                for j in range(0,TIMESTEP-1): 
                    if j == 0:
                        qOut[:,0,i] = qResOut[:,0,0]
                        y[jnos,j,i] = (( qOut[jnos,j,i]*SAMPLINGMATRIX[jnos,2])/( b * sqrt(SAMPLINGMATRIX[jnos,3])))**(3/5)
                        p[jnos,j,i]= b + 2 * y[jnos,j,i]
                        alpha[jnos,j,i] = ((SAMPLINGMATRIX[jnos,2] * p[jnos,j,i]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,3]))**beta
                    else:
                        qOut[:,:,5] = qResOut[:,:,0]
                        qOut[:,1,i] = qResOut[:,0,0]
                        qOut[jnos,j+1,i+1] = routing(alpha[jnos,j,i],beta,qOut[jnos,j+1,i],qOut[jnos,j,i+1],dx,dt)
                        y[jnos,j+1,i+1] = (( qOut[jnos,j+1,i+1]*SAMPLINGMATRIX[jnos,2])/( b * sqrt(SAMPLINGMATRIX[jnos,3])))**(3/5)
                        p[jnos,j+1,i+1]= b + 2 * y[jnos,j,i+1]
                        alpha[jnos,j+1,i+1] = ((SAMPLINGMATRIX[jnos,2] * p[jnos,j,i+1]**(2/3))/sqrt(SAMPLINGMATRIX[jnos,3]))**beta
                
    # Determine Water Level in Each Aquifer Section
    for jnos in range(0,NOS):
        WaterLevel[jnos,:,0] = y[jnos,:,12] + 1395
        WaterLevel[jnos,:,1] = y[jnos,:,24] + 1326
        WaterLevel[jnos,:,2] = y[jnos,:,31] + 1290
        WaterLevel[jnos,:,3] = y[jnos,:,38] + 1280
        
        
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
    
###############################################################################                
    # Call Groundwater Storage and Head
    for jnos in range(0,NOS):  
        a1=(SAMPLINGMATRIX[jnos,34] +SAMPLINGMATRIX[jnos,35] +SAMPLINGMATRIX[jnos,36] + SAMPLINGMATRIX[jnos,37])
        a2=(SAMPLINGMATRIX[jnos,38] + SAMPLINGMATRIX[jnos,39] + SAMPLINGMATRIX[jnos,40] + SAMPLINGMATRIX[jnos,41])
        a3=(SAMPLINGMATRIX[jnos,42] + SAMPLINGMATRIX[jnos,43] + SAMPLINGMATRIX[jnos,44] + SAMPLINGMATRIX[jnos,45])
        for i in LocGW: 
            SAMPLINGMATRIX[jnos,LocGW.index(i)+34] = SAMPLINGMATRIX[jnos,LocGW.index(i)+34]/a1
            SAMPLINGMATRIX[jnos,LocGW.index(i)+38] = SAMPLINGMATRIX[jnos,LocGW.index(i)+38]/a2
            SAMPLINGMATRIX[jnos,LocGW.index(i)+42] = SAMPLINGMATRIX[jnos,LocGW.index(i)+42]/a3

    for jnos in range(0,NOS):  
        for i in LocGW: 
            kriv[jnos,0,i] = KRIV(SAMPLINGMATRIX[jnos,33],SAMPLINGMATRIX[jnos,LocGW.index(i)+25],Lriver[0,i]) 
            # Set Initial Boundary 
            head[jnos,0,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+9]
            storage[jnos,0,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+13]
            # In Base Years Comment Below Line
            # qOutGW[jnos,0,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+17]
            qInteraction[jnos,0,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+21]
            
    for jnos in range(0,NOS):  
        for i in LocGW:
            for j in range(0,TIMESTEP-1):
                cw[jnos,j,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+34]
                qReturnFC[jnos,j,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+38]
                ww[jnos,j,i] = SAMPLINGMATRIX[jnos,LocGW.index(i)+42]
            1==1
    # In Base Year qOutGW is Baased on Exsit Data, So Comment line 337 and 361
    # ********************Turn On Below Lines *******************************#
    for jnos in range(0,NOS):
        qOutGW[jnos,:,:] = FoodWGW[:,:] + IndusWGW[:,:] 
    # Change Taraz to 3D
    for jnos in range(0,NOS):
        Tarazz[jnos,:,:] = Taraz[:,:]
    
    

    for jnos in range(0,NOS):  
        for i in range(0,u):
            for j in range(0,TIMESTEP-1):
                if j == 0 :
                    deltastorage[jnos,j+1,i] = STORAGE(qReturnF[j,i],qOutGW[jnos,j,i], Rainfall[j,i], qInteraction[jnos,0,i],cw[jnos,0,i],qReturnFC[jnos,0,i],ww[jnos,0,i])
                    storage[jnos,j+1,i] = deltastorage[jnos,j+1,i] + storage[jnos,j,i]
                    deltaH[jnos,j+1,i] = deltastorage[jnos,j+1,i] / (area[0,i] *1000000* SAMPLINGMATRIX[jnos,LocGW.index(i)+29])     #Calculate Groundwater head in each
                    head[jnos,j+1,i] = deltaH[jnos,j+1,i] + head[jnos,j,i]     # Calculate head of each user in different time()
                    qInteraction[jnos,j+1,i] = DARCY(kriv[jnos,0,i],Tarazz[jnos,j+1,i],WaterLevel[jnos,j,i],riverbed[i],RiverAreaPercentages[i])
                    
                
                
                if j > 0 :
                    # In Base Years Comment Below Line
                    # qOutGW[jnos,j,i] = SUSTAINABLEWITHDRAWAL(SAMPLINGMATRIX[jnos,LocGW.index(i)+29],area[0,i],deltaH[jnos,j,i],Rainfall[j,i],qReturnF[j,i],cw[jnos,0,i],qReturnFC[jnos,0,i],ww[jnos,0,i])
                    
                    qInteraction[jnos,j,i] = DARCY(kriv[jnos,0,i],Tarazz[jnos,j,i],WaterLevel[jnos,j,i],riverbed[i],RiverAreaPercentages[i])
                    deltastorage[jnos,j+1,i] = STORAGE(qReturnF[j,i],qOutGW[jnos,j,i],Rainfall[j,i], qInteraction[jnos,j,i],cw[jnos,0,i],qReturnFC[jnos,0,i],ww[jnos,0,i])
                    storage[jnos,j+1,i] = deltastorage[jnos,j+1,i] + storage[jnos,j,i]
                    deltaH[jnos,j+1,i] = deltastorage[jnos,j+1,i] / (area[0,i] *1000000* SAMPLINGMATRIX[jnos,LocGW.index(i)+29])
                    head[jnos,j+1,i] = deltaH[jnos,j+1,i] + head[jnos,j,i]
                  
    1 == 1
    # reapeat calculated qInteraction for all Locations
    # Aquifer is started from the 10 km of River, so before it there is no qInteraction
    # 14000 is the River Lenght Which is connected to Aquifer
    # 1000 is the Spatial Scale of WSMN Model  
    for i in range(0,r):
        if i < 11:                
            qInteractionF[:,:,i] = 0
        if 11 <=i < 25:
            qInteractionF[:,:,i] = qInteraction[:,:,1]/14000*1000
        if 25<= i < 30:
            qInteractionF[:,:,i] = qInteraction[:,:,2]/5000*1000
        if 30 <= i < 39:
            qInteractionF[:,:,i] = qInteraction[:,:,3]/9000 *1000
###############################################################################      
###############################################################################
    # Import Food and Energy Withdrawal for Base Year
    # If This is Base Year Use Data as food and energy Withdrawal 
    # If it is not uncomment line FoodWRiverInt[jnos,j,i] and EnergyWRiverInt[jnos,j,i]
    # ********************Turn On Below Lines *******************************#
    for jnos in range(0,NOS):
        FoodWRiverInt[jnos,:,:] = data9[:,:]
        IndussInt[jnos,:,:] = data10[:,:]          
    # Calculate Balance Equation for Interflows Based On Allocated Water Which Calculate on SurfaceWaterAllocation
    1 == 1
    for jnos in range(0,NOS):  
        for i in range (0,k):
            for j in range(0,TIMESTEP):
                qOutIntFinall[jnos,j,i] = qOutInt[jnos,j,i] - EvaInt[jnos,j,i]
                if qOutIntFinall[jnos,j,i] < 0 :
                    qOutIntFinall[jnos,j,i] = 0
                # FoodWRiverInt[jnos,j,i] = AGRICULTUREALLOCATION(qOutIntFinall[jnos,j,i],DEInter[j,i],EnergyDemandMinInt[j,i],TDInter[j,i],AgrInterflow[j,i],AgrPFinallInt[j,0])
                # EnergyWRiverInt[jnos,j,i] = ENERGYALLOCATION(qOutIntFinall[jnos,j,i],DEInter[j,i],EnergyDemandMinInt[j,i],TDInter[j,i],EnergyDemandMaxInt[j,i],EnergyPFinallInt[j,0])
                # ReturnEnergytoRiverInt[jnos,j,i] = 0.15 * EnergyWRiverInt[jnos,j,i]
                qOutIntFinall[jnos,j,i:] =  qOutIntFinall[jnos,j,i:]  - FoodWRiverInt[jnos,j,i]  
    ###########################################################################
    ###########################################################################
    # It is better to Calculate River Depth (Y) after Calculating qOutFinall
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
    # Import Food and Energy Withdrawal for Base Year
    # If This is Base Year Use Data as food and energy Withdrawal 
    # If it is not uncomment line FoodWRiver[jnos,j,i] and EnergyWRiver[jnos,j,i]
    # ********************Turn On Below Lines *******************************#
    for jnos in range(0,NOS):
        FoodWRiver[jnos,:,:] = data3[:,:]
        EnergyWRiver[jnos,:,:] = data4[:,:]
        Domestic[jnos,:,:] =  domestic[:,:]
        Induss[jnos,:,:] = Indus[:,:]
        
    # Calculate Balance Equation for Main River
    for jnos in range(0,NOS):
        for i in range(0,r):
           for j in range(0,TIMESTEP):
            qOutFinall[jnos,j,i] =  qOut[jnos,j,i] + qOutIntFinall[jnos,j,i]  - Eva[jnos,j,i]  - qInteractionF[jnos,j,i] - 30* Domestic[jnos,j,i] -  Induss[jnos,j,i]
            if qOutFinall[jnos,j,i] < 0:
                qOutFinall[jnos,j,i] = 0
                # FoodWRiver[jnos,j,i] = AGRICULTUREALLOCATION(qOutFinall[jnos,j,i],DE[j,i],EnergyDemandMin[j,i],TD[j,0],AgrDemand[j,i],AgrPFinall[j,0])
                # EnergyWRiver[jnos,j,i] = ENERGYALLOCATION(qOutFinall[jnos,j,i],DE[j,i],EnergyDemandMin[j,i],TD[j,i],EnergyDemandMax[j,i],EnergyPFinall[j,0])
                # ReturnEnergytoRiver[jnos,j,i] =  0.1 * EnergyWRiver[jnos,j,i]
                qOutFinall[jnos,j,i:] = qOutFinall[jnos,j,i:] -  FoodWRiver[jnos,j,i] - EnergyWRiver[jnos,j,i]  
    1 == 1         
###############################################################################            
    
    # Calculate Objective Function 
###############################################################################
    for jnos in range(0,NOS):
        # If there are other Observed Station such as Alavian and Maraghe
        # DISCHARGESIMULATED[jnos,:,0] = qOutFinall[jnos,:,6]
        # DISCHARGESIMULATED[jnos,:,1] = qOutFinall[jnos,:,8]
        DISCHARGESIMULATED[jnos,:,0] = qOutFinall[jnos,:,38]
        HEADSIMULATED[jnos,:,0 ] = head[jnos,:,0]
        HEADSIMULATED[jnos,:,1 ] = head[jnos,:,1]
        HEADSIMULATED[jnos,:,2 ] = head[jnos,:,2]
        HEADSIMULATED[jnos,:,3 ] = head[jnos,:,3]
        
    1 == 1
    
    for jnos in range(0,NOS):
        for i in range(0,1):
            # Each Station Has Equal Value on Wighted RMSE 
            objective_function[jnos,0,i] = np.sqrt((np.nansum((OBSERVATION[:,i] -DISCHARGESIMULATED[jnos,:,i]) ** 2,axis = 0))/(np.count_nonzero(~np.isnan(OBSERVATION[:,i]),axis=0)))
            
    for jnos in range(0,NOS):
        for i in range(0,4):
            # Each Location of Aquifer Has Equal Value on Wighted RMSE 
            objective_function[jnos,0,i+1] = np.sqrt((np.nansum((OBSERVATIONHEAD[:,i] - HEADSIMULATED[jnos,:,i]) ** 2,axis = 0))/(np.count_nonzero(~np.isnan(OBSERVATIONHEAD[:,i]),axis=0)))
            
    for jnos in range(0,NOS):             
        for i in range(0,5):
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
    1 == 1

   
    # Determine Best Parametres in Sampling Matrix Rows
    xstar = SAMPLINGMATRIX[bb,:]
    
    
            
    1 == 1
    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------
    # Write In Balance Excel for TDS Routing
    app = xw.App(visible=True)
    wb = xw.Book('D:\My Code New\DataBank\BalanceEquation.xlsx')  
    sht2 = wb.sheets['qOutFinallCode']    
    sht2.range('B3:AO3').clear()
    sht2.range('B3:AO3').value = qOutFinall[bb,:,:]  
    # -----------------------------------------------------------------------
    wb1 = xw.Book('D:\My Code New\DataforSalinatary\ReserviorsData.xlsx') 
    sht3 = wb1.sheets['Storage'] 
    sht3.range('B2').clear()
    sht3.range('B2').value = st[bb,:,:]
    # ----------------------------------------------------------------------
    sht4 = wb1.sheets['QOut'] 
    sht4.range('B2').clear()
    sht4.range('B2').value = qResOut[bb,:,:]
    # ----------------------------------------------------------------------
    wb2 = xw.Book(r'D:\My Code New\DataforSalinatary\NodesData.xlsx') 
    sht5 = wb2.sheets['Interflows'] 
    sht5.range('B2:AO2').clear()
    sht5.range('B2:AO2').value = qOutInt[bb,:,:]
    # ---------------------------------------------------------------------
    # sht6 = wb2.sheets['Returnflow'] 
    # sht6.range('B2:BA2').clear()
    # sht6.range('B2:BA2').value = ReturnFoodtoRiver[bb,:,:]
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    #####################################################################
    #####################################################################
    #####################################################################
    ########## Get the Disirable Results for Xstar ######################
    wb3 = xw.Book(r'D:\My Code New\DataBank\FinallResults.xlsx')   
    # Extarct Main River Evaporation
    sht7 = wb3.sheets['Evaporation'] 
    Eva[bb,:,:] = Eva[bb,:,:]
    sht7.range('B2:AO2').value = Eva[bb,:,:] 
    # Extract Interflow Evaporation
    sht8 = wb3.sheets['InterflowEvaporation'] 
    sht8.range('B2:BA2').value = EvaInt[bb,:,:]
    
    # Extract QRouted in Main River Which Has QresOut 
    sht9 = wb3.sheets['qOutRouted'] 
    sht9.range('B2:BA2').value = qOut[bb,:,:]
    
    # Extract Interflow Routed 
    sht10 = wb3.sheets['qInterflowRouted'] 
    sht10.range('B2:BA2').value = qOut[bb,:,:]
    
    # Extract Head and Storage of Groundwater 
    sht11 = wb3.sheets['Groundwaterhead'] 
    sht11.range('B2:E2').value = head[bb,:,:]
    sht12 = wb3.sheets['Groundwaterstorage'] 
    sht12.range('B2:E2').value = storage[bb,:,:]
    
    # Extract qOutIntFinall After Balance Equation
    sht13 = wb3.sheets['qOutIntFinall'] 
    sht13.range('B2:BA2').value = qOutIntFinall[bb,:,:]  
    
    
    # Extract qInteraction After Balance Equation
    sht14 = wb3.sheets['qInteraction'] 
    sht14.range('B2:AO2').value = qInteractionF[bb,:,:]
    
    # Extract qOutFinall After Balance Equation
    sht15 = wb3.sheets['qOutFinall'] 
    sht15.range('B2:AO2').value = qOutFinall[bb,:,:]
    app.kill()
    
    
    # Plot Results 
    ##########################################################################
    # Plot Evaporation
    t = np.linspace(0,120,120)
    # Change Unit From M3/s to mm/day
    plt.plot(t,(Eva[bb,:,0]*1000*24*3600)/(1000*6))
    plt.legend(["Evaporation"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('Evaporation(mm/day)')
    plt.show()
    ##########################################################################
    # Plot Routed Discharge in Interflow
    qOutInt[bb,:,50] = (qOutInt[bb,:,50] /1000000) * 24 * 30 * 3600
    plt.plot(t,qOutInt[bb,:,50])
    plt.legend(["Finall Point"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('qOutInterflow(Mm3)')
    plt.show()
    ##########################################################################
    # Plot Routed Discharge in Main River
    qOut[bb,:,38] = (qOut[bb,:,38] / 1000000) * 24 * 30 * 3600
    plt.plot(t,qOut[bb,:,38])
    plt.legend(["Simulated Discharge"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('qOut(Mm3)')
    plt.show()
    ##########################################################################
    # Plot Routed Discharge in Main River After Balance Equation
    qOutFinall[bb,:,38] = (qOutFinall[bb,:,38] / 1000000) * 24 * 30 * 3600
    plt.plot(t,qOutFinall[bb,:,38])
    plt.legend(["ّFinall Point"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('qOutFinall(Mm3)')
    plt.show()
    ##########################################################################
    # Plot Routed Discharge in Main River After Balance Equation with Observation
    # qComparative[:,0] = (qOutFinall[bb,:,38] / 1000000) * 24 * 30 * 3600
    qComparative[:,0] = qOutFinall[bb,:,38]
    qComparative[:,1] = (OBSERVATION[:,0] *(24 * 30 * 3600)/1000000)
    plt.plot(t,qComparative[:,:])
    plt.legend(["ّSimulated Discharge"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('qOutFinall(Mm3)')
    plt.show()
    ##########################################################################
    qResOut[bb,:,0] =  (qResOut[bb,:,0] * 1000000) * 24 * 30 * 3600
    plt.plot(t,qResOut[bb,:,0])
    plt.legend(["ResOutflow"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('QRESERVIOR(Mm3)')
    plt.show()
    ##########################################################################
    # Plot Groundwater Results 
    # Plot  head of aquifers
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Create t and x as shape head
    tt = np.arange(1, 5, 1)
    x = np.arange(0, 120, 1)
    tt, x = np.meshgrid(tt, x)
    
    # Plot the surface.
    head11[:,:] = head[bb,:,:]
    surf = ax.plot_surface(tt, x,head11, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
    # Customize the z axis.
    ax.set_zlim(0,18)
    ax.zaxis.set_major_locator(LinearLocator(6))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.75, aspect=20)
    plt.show()
    # Plot Head over Time
    # Head In Aquifer 1 
    tt2 = np.linspace(0,120,120)
    plt.plot(tt2,head[bb,:,0])
    plt.legend(["Water Level1"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('Water Level(m)')
    plt.show()
    # Head in Other Aquifers
    tt2 = np.linspace(0,120,120)
    plt.plot(tt2,head[bb,:,1:4])
    plt.legend(["Water Level2","Water Level3","Water Level3"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('Water Level(m)')
    plt.show()
    ##########################################################################
    # Plot Head Simulated in Aquifers  with Observation
    tt2 = np.linspace(0,120,120)
    headCom[:,0] = head[bb,:,0]
    headCom[:,1] = OBSERVATIONHEAD[:,0]
    plt.plot(tt2,headCom[:,0:2])
    plt.legend(["Water Level1"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('Water Level(m)')
    plt.show()
    # Head in Other Aquifers
    tt2 = np.linspace(0,120,120)
    headCom[:,2] = head[bb,:,1]
    headCom[:,3] = OBSERVATIONHEAD[:,1]
    headCom[:,4] = head[bb,:,2]
    headCom[:,5] = OBSERVATIONHEAD[:,2]
    headCom[:,6] = head[bb,:,3]
    headCom[:,7] = OBSERVATIONHEAD[:,3]
    plt.plot(tt2,headCom[:,2:4])
    plt.legend(["Water Level2"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('Water Level(m)')
    plt.show()
    plt.plot(tt2,headCom[:,4:6])
    plt.legend(["Water Level3"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('Water Level(m)')
    plt.show()
    plt.plot(tt2,headCom[:,6:8])
    plt.legend(["Water Level4"], loc ="upper left") 
    plt.xlabel('time(Month)')
    plt.ylabel('Water Level(m)')
    plt.show()
    ##########################################################################
    # Plot QInteraction
    qInteraction[bb,:,:] = (qInteraction[bb,:,:] / 1000000) * 24 * 30 * 3600
    plt.plot(t,qInteraction[bb,:,:])
    plt.legend(["Aquifer1","Aquifer2","Aquifer3","Aquifer4"], loc ="lower right") 
    plt.xlabel('time(Month)')
    plt.ylabel('qInterrelation(Mm3)')
    plt.show()
    
    return objective_function,objective_functionW,objective_functionWS, varf, xstar, qOutFinall,DISCHARGESIMULATED,HEADSIMULATED,SAMPLINGMATRIX
  


