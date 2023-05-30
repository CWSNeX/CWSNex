#-------------------------------------------------------------------------
# Name:        Mass Balance Method to Rout TDS in (Rivers, Nodes< Reserviors, Root Zone)
# Purpose:
#
# Author:      Elham Soleimanian
#
# Created:     04/08/2021
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt
# -------------------------------------------------------------------------

          

def find_mass(TIMESTEP,NOS, SAMPLINGMATRIX,OBSERVATION,W):

    """
    This function calculate TDS by routing and using 3 other functions an bilans
    : param nos: Total number of simulations
    : param samplingmatrix: LHS matrix
    : param observedtds: Observed TDS file
    
    :return: objective_function: Values of objective function for each simulation
    :return: varf: Variance of objective function values
    :return: xstar: Row of lhs values which has (minimum/maximum)
    :return: tds
    """ 

        # -------------------------------------------------------------------------
    # Import Data for Oconner Method
    #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
    # Call Discharge from Balane Equation Module 
    # Attention in discharge function discharge of water withdrawal for food,
    # return flow from food to river and discharge of Interflows are ignored in balance equation
    # it's assumed that water withdrawal for energy and return flow from energy to river 
    # has no remarkable affect on TDS so the effect of them is calculated on 
    # balance equation module not on mass balance module 
    #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
    # Import Discharge of River From Balance Equation Module 
    # This  Discharge Consists Evaporation, SW and GW Interrelation, Return Flow 
    # from Energy, Water Withdrawal from Energy
    Data  = pd.ExcelFile(r'D:\My Code New\DataBank\BalanceEquation.xlsx')
    q = pd.read_excel(Data, 'qOutFinallCode',usecols='B:AO').to_numpy()
    # Location of Observation Station in Mainflow
    mainLoc=[0]
    [m , n1] = q.shape
    # ------------------------------------------------------------------------
    # Import Data for Mass Balance In Reserviors 
    Data  = pd.ExcelFile(r'D:\My Code New\DataforSalinatary\ReserviorsData.xlsx')
    s = pd.read_excel(Data, 'Storage',usecols='B').to_numpy()
    qResOut = pd.read_excel(Data, 'QOut',usecols='B').to_numpy()
    [mm , nn] =qResOut.shape
    # ------------------------------------------------------------------------
    # Import Amount of Returnflow and Interflow and water withdrawal
    # Its Assumed In Interflows there arent any Nodes so Input Interflows Regards to Their Location
    Data1 =  pd.ExcelFile(r'D:\My Code New\DataforSalinatary\NodesData.xlsx')
    qInter=np.zeros((TIMESTEP,n1))
    data = pd.read_excel(Data1, 'Interflows',usecols='AI:AI',skiprows = range(1, 2)).to_numpy()
    zzzzz = data[1:TIMESTEP,0]
    qInter[1:TIMESTEP,35] = data[1:TIMESTEP,0]
    # Determine Number of Interflows
    uu = np.size(qInter.shape)
    # Location of Observation Station in Interflow
    interLoc = [35]
    # Amount of qIrrigation and qReturn are calculated on Food Model and write  in NodesData
    qReturn = pd.read_excel(Data1, 'Returnflow',usecols='B:AO').to_numpy()
    CqReturn = pd.read_excel(Data1, 'CReturnflow',usecols='B:AO',skiprows = range(1, 2)).to_numpy()
    qIrri = pd.read_excel(Data1, 'Waterwithdrawal',usecols='B:AO',skiprows = range(1, 2)).to_numpy()
    # Input Location of Obsevation Station for Main River 
    oLoc = [0,35] # Should be Updated
    # Wight of Each Observation Station 
    1 == 1
    # -------------------------------------------------------------------------
    # # Preallocation 
    # c is a Matrix for TDS in the whole Main River Which Consists Node Equation
    c = np.zeros((NOS,TIMESTEP,n1))
    # CqInter is Matrix for TDS in Interflows which has to route
    CqInter = np.zeros((NOS,TIMESTEP,n1))
    # cStorage is the TDS in Reservior 
    cStorage = np.zeros((NOS,TIMESTEP,nn))
    cComparative = np.zeros((TIMESTEP,2))
    cComparativeInt = np.zeros((TIMESTEP,2))
    
    # In Each of Withdrawal Points TDS In River is equivalent with TDS which pass to Food Model
    CqIrri = np.zeros((m,n1))  #fkr nmikonam k in ham bayad 3 bodi bashe 
    TDSSIMULATED = np.zeros((NOS,TIMESTEP,2))
    objective_function = np.zeros((NOS,1,4)) 
    objective_functionW = np.zeros((NOS,1,4))
    objective_functionWS = np.zeros((NOS,1,1))
    # --------------------------------------------------------------------------
    # Create Relation Between Groundwar TDS and Surface Water TDS
    # SAMPLINGMATRIX[:,1] =  SAMPLINGMATRIX[:,1] *  SAMPLINGMATRIX[:,2]
    # Calculate TDS In Interflows Rivers
    # Three Interflows and Each Interflow has Four Parametes to be Calibrated
    for jnos in range(0,NOS):
        for i in interLoc:
            for j in range(0,TIMESTEP-1):
                
                CqInter[jnos,j,i] = OCONNER(qInter[j+1,i],SAMPLINGMATRIX[jnos,interLoc.index(i)*4+4],SAMPLINGMATRIX[jnos,interLoc.index(i)*4+5],SAMPLINGMATRIX[jnos,interLoc.index(i)*4+6],SAMPLINGMATRIX[jnos,interLoc.index(i)*4+7])
                


    1 == 1
    # Calculate TDS in Main River Regard to All Nodes(Interflows, Water Withdrawal, Return Flow) and Rivers
    # -------------------------------------------------------------------------
    #*********************** Assign Numbers to each section to recognize what ##############
    ######################## kind of Node, Rivers or Reservior they are ##############
    # Number 0 shows Rivers
    # Number 1 Shows Nodes Which Consists Qinterflow, Qreturnflow, Qwithdrawal for Irrigation
    # In Excel File Each section That We have each of aformentioned Q used 1 Code
    # Number 2 Shows Start Point of  Reservior Location  
    # Number 3 Shows End Point of Reservior Loccation 
    # Number 4 there is nothing to calculate new TDS so repeate the TDS from Previous Spatial Scale
    

    # # Calculate TDS In Main River   
    for jnos in range(0,NOS):
        for i in mainLoc:
            for j in range(0,TIMESTEP-1):
                    c[jnos,j,i] = OCONNER(q[j+1,i],SAMPLINGMATRIX[jnos,0],SAMPLINGMATRIX[jnos,1],SAMPLINGMATRIX[jnos,2],SAMPLINGMATRIX[jnos,3])

   
# Calculate TDS in Nodes and Reserviors
    for jnos in range(0,NOS):
        for i in range(0,n1):
            if q[0,i] == 1 : 
                for j in range(0,TIMESTEP-1):
                  
                    # For River Contraction, water withdrawal and return flow   
                        c[jnos,j,i] = NODE(q[j+1,i-1], c[jnos,j,i-1], qInter[j+1,i], CqInter[jnos,j,i], qReturn[j+1,i], CqReturn[j+1,i], qIrri[j+1,i], CqIrri[j+1,i],q[j+1,i],j) 
                        # if i >= 12 and j == 1 :
                        #     vvv ="dddd"
            # Where Reservior is located(start point)
                    ##################### tabbbbb
            if q[0,i] == 2: 
                cStorage[jnos,0,0] = c[jnos,0,i-1]
                for j in range(0,TIMESTEP-1):
                    cStorage[jnos,j+1,0] = RESERVIORTDS2(s[j,0],s[j+1,0],cStorage[jnos,j,0],c[jnos,j,i-1],q[j+1,i-1],qResOut[j,0])
                    c[jnos,:,i] = cStorage[jnos,:,0]
                    # if i >= 12 and j == 1 :
                    #         vvv ="dddd"
                    1 == 1
                        ################
                        
            # Where Reservior is located(End point)
            if q[0,i] == 3:
                for j in range(0,TIMESTEP-1): 
                    c[jnos,j,i] = (cStorage[jnos,j,0] + cStorage[jnos,j+1,0])/2
                    # if i >= 12 and j == 1 :
                    #         vvv ="dddd"
                        
            if q[0,i] == 4:
                c[jnos,:,i] = c[jnos,:,i-1]
      
# # Calculate Objective Function 
#############################################
    for jnos in range(0,NOS):  # location ha daghigh nis 
        TDSSIMULATED[jnos,:,0] = c[jnos,:,38]
        TDSSIMULATED[jnos,:,1] = CqInter[jnos,:,35]
        
       
   
    for jnos in range(0,NOS):
        for i in range(0,2):
            objective_function[jnos,0,i] = np.sqrt((np.nansum((OBSERVATION[:,i] -TDSSIMULATED[jnos,:,i]) ** 2,axis = 0))/(np.count_nonzero(~np.isnan(OBSERVATION[:,i]),axis=0)))
            # Each Station Has Equal Value on Wighted RMSE 
        
    for jnos in range(0,NOS):             
        for i in range(0,2):
            objective_functionW[jnos,0,i] = W[0,i]*objective_function[jnos,0,i]
    for jnos in range(0,NOS): 
        objective_functionWS[jnos,0,0] =  objective_functionW[jnos,0,:].sum(axis=0, keepdims =True)
   
             
               
    ############################# axis = 2 ????????????????????????????????????????????    
    objective_function=objective_function[:,0,:]
    objective_functionW=objective_functionW[:,0,:]
    objective_functionWS=objective_functionWS[:,0,0]
    # objective_functionWS = np.random.uniform(low=0.0, high=80.0, size=(NOS,1)) ################# alaki !!!!!!!!!!!!!!!
    # xstar=xstar[:,0,:]            
#alculate Variance of Objective Function with Delta Degree of Freedom of 0                 
    varf = np.var(objective_functionWS, ddof=0)  

# # Recognize of Index for Min of RMSE  ################ argmax ?????????????????????//
    bb =objective_functionWS.argmin()
#     # aa=np.argmin(objective_function,axis=2)
   
# # Determine Best Parametres in Sampling Matrix Rows
#     # xstar = SAMPLINGMATRIX[np.argmin(objective_function),:]
    xstar = SAMPLINGMATRIX[bb,:]
    
    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################
    ########## Get the Disirable Results for Xstar ######################
    app = xw.App(visible=True)
    wb = xw.Book('D:\My Code New\DataBank\FinallResults.xlsx')  
    sht1 = wb.sheets['TDSinMainRiver'] 
    sht1.range('B2:AO2').value = c[bb,:,:] 
    sht2 = wb.sheets['TDSReservoir'] 
    sht2.range('B2').value = cStorage[bb,:,:]
    sht3 = wb.sheets['TDSInterflow'] 
    sht3.range('B2').value = CqInter[bb,:,:]
    app.kill()
    # Plot Results
    #####################################################################
    # TDS Routed in Main River
    t = np.linspace(0,120,120)
    plt.plot(t,c[bb,:,38])
    plt.legend(["TDS_Main River"], loc ="upper right") 
    plt.xlabel('time(Month)')
    plt.ylabel('TDS(mg/lit)')
    plt.show()
    #####################################################################
    # TDS Routed in Reservoir
    t = np.linspace(0,120,120)
    plt.plot(t,cStorage[bb,:,0])
    plt.legend(["TDS_Reservoir"], loc ="upper right") 
    plt.xlabel('time(Month)')
    plt.ylabel('TDS(mg/lit)')
    plt.show()
    #####################################################################
    # Plot TDS Simulated and Observation
    # Plot Routed Discharge in Main River After Balance Equation with Observation
    cComparative[:,0] = c[bb,:,38]
    cComparative[:,1] = OBSERVATION[:,0]
    plt.plot(t,cComparative[:,:])
    plt.legend(["ّTDS_Simulated"], loc ="upper right") 
    plt.xlabel('time(Month)')
    plt.ylabel('TDS(mg/lit)')
    plt.show()
    cComparativeInt[:,0] = CqInter[bb,:,35]
    cComparativeInt[:,1] = OBSERVATION[:,1]
    plt.plot(t,cComparativeInt[:,:])
    plt.legend(["ّTDS_SimulatedInterflow"], loc ="upper right") 
    plt.xlabel('time(Month)')
    plt.ylabel('TDS(mg/lit)')
    plt.show()
    
    ##########################
    # Plot TDS Simulated in Interflow
    return objective_function,objective_functionW,objective_functionWS, varf, xstar, c,TDSSIMULATED,CqInter
# # # ----------------------------------------------------------------------------- 

# ------------------------------------------------------------------------
################ Following Function Route TDS in Rivers #################
def OCONNER(Q,Q0,CG,CS,N):
           
            BETA= Q0**(1-N)
            C = 0
            aa = Q
            aa1 = Q0
            aa2 = CG
            aa3 = CS
            aa4 = N
            if Q < Q0 :
                C =  CG
                
            elif Q > Q0 :
                C = CG + ((BETA * (CG -CS))/(Q ** (1 - N)))
            if C<0:
                C = 300
            
            return C 

# # ------------------------------------------------------------------------
# ################ Following Function Route TDS in each Node #################
def NODE1(QIN,CIN,QOUT) :
          C = 0
          C  = (QIN * CIN)/QOUT
          return C 
def NODE(Q,Cin,QINTER,CINTER,QRETURN,CRETURN,QWITHDRAWAL,CWITHDRAWAL,QOUT,J):
          Cout = 0
          a1=Q
          a2=Cin
          a3=QINTER
          a5=CINTER
          a6=QOUT
          a7=CRETURN
          a8=QWITHDRAWAL
          a9=CWITHDRAWAL
         
          a11 = J
          if Q < 0.3:
              Cout = 300
          #     Q = 0.1
          #     b1=Q
          
          elif QOUT < 0.3 :
              
              Cout = 300
          
            
          elif QOUT > 0 :
            
          
              Cout = ((Q * Cin) + QINTER * CINTER + QRETURN * CRETURN - QWITHDRAWAL * CWITHDRAWAL)/QOUT
         
              
          return Cout

# # ------------------------------------------------------------------------
# ################ Following Functions Route TDS in Reserviors in Two Method  #################
# This Function Calculate Reservoir TDS with Using While Loop
def RESERVIORTDS1(ST1,ST2,CSTORAGE1,CQRESINT,QRESINT,QRESOUT):
                CSTORAGE = 0
                deltaCSTORAGE = 1
                telp = 0
                tolerance = 1
                while True:
                    F = CSTORAGE * ST2 - CSTORAGE1 * ST1 - CQRESINT * QRESINT +(CSTORAGE + CSTORAGE1)/2 * QRESOUT
                    if abs(F) < tolerance: 
                        break
                    elif F>0 and telp>=0:
                        CSTORAGE = CSTORAGE - deltaCSTORAGE
                    elif F<0 and telp<=0:
                        CSTORAGE = CSTORAGE + deltaCSTORAGE
                    elif F>0 and telp<=0:
                        deltaCSTORAGE = deltaCSTORAGE/2
                        CSTORAGE = CSTORAGE - deltaCSTORAGE
                    elif F<0 and telp>=0:
                        deltaCSTORAGE = deltaCSTORAGE/2
                        CSTORAGE = CSTORAGE  + deltaCSTORAGE
                        telp = F     
                return CSTORAGE
            
# # --------------------------------------------------------------------------
# This Function Calculate Reservoir TDS with Simpler Mathematical Method
## Attention: Both Functions Are Using Same Laws with Different Solution Method
def RESERVIORTDS2(ST1,ST2,CSTORAGE1,CQRESINT,QRESINT,QRESOUT):
                  CSTORAGE = 0
                  zzz1=ST1
                  zzz2=ST2
                  zzz3=CSTORAGE1
                  zzz4=CQRESINT
                  zzz5=QRESINT
                  zzz6=QRESOUT
                  CSTORAGE = (CQRESINT * QRESINT + (ST1 - QRESOUT/2 ) * CSTORAGE1) / (ST2 + QRESOUT/2)
                  zzz7=CSTORAGE
                  return CSTORAGE

# ----------------------------------------------------------------------------   















                                   