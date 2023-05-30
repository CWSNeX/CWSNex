# -------------------------------------------------------------------------
# Name:        Reservior Operation
# Purpose:     This madule define outflow of reserviors and revise river flow after reserviors
#
# Author:      Elham Soleimanian
#
# Created:     12/12/2020
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt
#-------------------------------------------------------------------------
##########################################################################
##########################################################################
############ ***** Required Data for LISFLOOD Method ***** ###############
##########################################################################
##########################################################################
# Import River Flow from KinimaticWithInterflow Madule
data = pd.ExcelFile(r'D:\My Code New\DataBank\QRESIN.xlsx')
qResin =  pd.read_excel(data, 'Sheet1',usecols='B').to_numpy() #m3/s
[m,uR] = qResin.shape
#-------------------------------------------------------------------------
# Import constant Related to Each Reservior
data = pd.ExcelFile(r'D:\My Code New\DataBank\ReserviorsConstants.xlsx')
storageR = pd.read_excel(data, 'Sheet1',usecols='B').to_numpy()
storageR = storageR.astype(float)


l_c = pd.read_excel(data, 'Sheet1',usecols='C').to_numpy()
l_f = pd.read_excel(data, 'Sheet1',usecols='D').to_numpy()
l_n = pd.read_excel(data, 'Sheet1',usecols='E').to_numpy()


#-------------------------------------------------------------------------
# Import Discharges Related to River
data = pd.ExcelFile(r'D:\My Code New\DataBank\Qnorm_MinfromReservior.xlsx')
Q_min = pd.read_excel(data, 'Qmin',usecols='A').to_numpy()  # m3/s
Q_norm =  pd.read_excel(data, 'Qnorm',usecols='A').to_numpy()  # m3/s
Q_nonD =  pd.read_excel(data, 'QnonD',usecols='A').to_numpy()  # m3/s

#------------------------------------------------------------------------
# Import time Step(month)
dt = 30 * 24 * 3600
t = np.linspace(0,120,120)
timestep = 120 
#------------------------------------------------------------------------
# Preallocation Matrix
qResOut = np.zeros((m,uR))
F = np.zeros((m+1,uR))
st = np.zeros((m+1,uR))
rel = np.zeros((1,uR))
res = np.zeros((1,uR))
vol = np.zeros((1,uR))
sus = np.zeros((1,uR))
h = np.zeros((m+1,uR))
A = np.zeros((m+1,uR))
Alpha = np.zeros((0,uR))
#------------------------------------------------------------------------
############################################################################
############################################################################
# ################### ***** Required Data for SOP Methode ***** ############
############################################################################
############################################################################
#Import Target Release from each Reservior
data1 = pd.ExcelFile(r'D:\My Code New\DataBank\TargetRelaseforSOP.xlsx') #m3/s
targetRelase = pd.read_excel(data1, 'Sheet1',usecols='B').to_numpy()
# Import sMin & sini $ ka & sMax for each Reservior
Data  = pd.read_excel(r'D:\My Code New\DataBank\ReserviorConstantsforSOP.xlsx')
data = pd.ExcelFile(r'D:\My Code New\DataBank\ReserviorConstantsforSOP.xlsx')
sMin = pd.DataFrame(Data,columns = ['Smin1']).to_numpy() #m3
sIni = pd.read_excel(data,'Sini')
sIni = pd.DataFrame(sIni,columns = ['Sini1']).to_numpy() #m3
sMax = pd.read_excel(data,'Smax')
sMax = pd.DataFrame(sMax,columns = ['Smax1']).to_numpy() #m3
ka = pd.read_excel(data,'ka')
ka = pd.DataFrame(sMax,columns = ['Ka1']).to_numpy() #m3
# Import Calculated Evaporation from Reservior 
data2 = pd.ExcelFile(r'D:\My Code New\DataBank\ReserviorConstantsforSOP.xlsx')
e = pd.read_excel(data2, 'Eva',usecols='B').to_numpy() 
#-----------------------------------------------------------------------



############# ***** Following Function calculate Reservior Outflow *****##############
# This function is based on distributed LISFLOOD Hydrological Model
def Lisflood(ST,QMIN,DT,F,STORAGE,LC,QNORM,LN,LF,QRESIN,QNOND,E):
            QRESOUT = QNORM
            STnext = ST + QRESIN * DT - QRESOUT * DT - E
           
            if STnext < 0:
                STnext = 0
            F = STnext/STORAGE
            zzzzzzzzzzzzzz = LC
            if F <= 2*LC:
                QRESOUT = min(QMIN,1/DT * F * STORAGE)
            elif F > 2*LC and F <= LN:
                QRESOUT = QMIN + (QNORM - QMIN) * (F - 2 * LC)/(LN - 2 * LC)
            elif F > LN and F <= LF:
                QRESOUT = QNORM + ((F - LN)/(LF - LN)) * max((QRESIN - QNORM) , (QNOND - QNORM))
            elif F > LF:
                QRESOUT =  max(((F - LF)/DT) * STORAGE, QNOND)
            STnext = ST + QRESIN * DT - QRESOUT * DT - E
            return STnext,QRESOUT
        



def SOP(ST,QRESIN,TR,KA,SMIN,DT,E):  
        
        QRESOUT = TR * DT 
        STnext = ST + QRESIN * DT - QRESOUT  - E
        
        
        if STnext <= KA and STnext >= SMIN:
            QRESOUT = TR *DT
        elif STnext > KA:
            QRESOUT = TR *DT  + STnext - KA    
        else:
            QRESOUT = TR * DT + STnext - SMIN
            
        STnext = ST + QRESIN * DT - QRESOUT  - E
        return STnext,QRESOUT/DT
    
def HEAD(ST):
        AT = -0.0006 * (ST/1000000) **2  + 0.072 * (ST/1000000) + 0.123
        HT = 3 * ST/(AT*1000000)
        return HT 
     
def ReliabilityLISFLOOD(QRESOUT,QNORM,TIMESTEP):
                # zQNORM = QNORM
                # zQRESOUT = QRESOUT
                RELIABILITY = 0
                Z = np.zeros((TIMESTEP))
                for i in range(0,TIMESTEP):
                    if QRESOUT[i] >= QNORM[i]:  
                        Z[i] = 1
                    else: 
                        Z[i] = 0
                RELIABILITY = np.sum(Z,axis = 0)/TIMESTEP
                return RELIABILITY
            
            
            
def RESELIENCELISFLOOD(QRESOUT,QNORM,TIMESTEP):
                  NUMBEROFFALIURE = 0 
                  NUMBERSUCCEDAFTERFALIURE = 0
                  RESELIENCE = 0
                  for i in range(TIMESTEP):
                      if QRESOUT[i] < QNORM[i]:
                          NUMBEROFFALIURE = NUMBEROFFALIURE + 1 
                      if QRESOUT[i] >= QNORM[i] and QRESOUT[i-1] < QNORM[i-1] and i > 0:
                          NUMBERSUCCEDAFTERFALIURE = NUMBERSUCCEDAFTERFALIURE + 1 
                      if NUMBEROFFALIURE > 0 :
                          RESELIENCE = NUMBERSUCCEDAFTERFALIURE/NUMBEROFFALIURE
                  return  RESELIENCE

def VolnurabilityLISFLOOD(QRESOUT,QNORM,TIMESTEP):
                    NUMBEROFFAILIURE = 0
                    VOLNURABILITY = 0
                    DEFECIT = np.zeros((TIMESTEP))
                    for i in range(0,TIMESTEP):
                        if QRESOUT[i] < QNORM[i]:
                            DEFECIT[i] = QNORM[i] - QRESOUT[i]
                            NUMBEROFFAILIURE = NUMBEROFFAILIURE + 1
                    AVETARGETRELEASE = np.sum(QNORM,axis = 0)
                    VOLNURABILITY = (np.sum(DEFECIT,axis = 0)/NUMBEROFFAILIURE )/AVETARGETRELEASE
                    return VOLNURABILITY                    

    
def ReliabilitySOP(QRESOUT,TR,TIMESTEP):
                zQRESOUT = QRESOUT
                RELIABILITY = 0
                Z = np.zeros((TIMESTEP))
                for i in range(0,TIMESTEP):
                    if QRESOUT[i] >= TR[i]:
                        Z[i] = 1
                    else: 
                        Z[i] = 0
                RELIABILITY = np.sum(Z,axis = 0)/TIMESTEP
                return RELIABILITY
             
def RESELIENCESOP(QRESOUT,TR,TIMESTEP):
                  NUMBEROFFALIURE = 0 
                  NUMBERSUCCEDAFTERFALIURE = 0
                  RESELIENCE = 0
                  for i in range(TIMESTEP):
                      if QRESOUT[i] < TR[i]:
                          NUMBEROFFALIURE = NUMBEROFFALIURE + 1 
                      if QRESOUT[i] >= TR[i] and QRESOUT[i-1] < TR[i-1] and i > 0:
                          NUMBERSUCCEDAFTERFALIURE = NUMBERSUCCEDAFTERFALIURE + 1 
                      if NUMBEROFFALIURE > 0 :
                          RESELIENCE = NUMBERSUCCEDAFTERFALIURE/NUMBEROFFALIURE
                  return  RESELIENCE
              
def VolnurabilitySOP(QRESOUT,TR,TIMESTEP):
                    NUMBEROFFAILIURE = 0
                    VOLNURABILITY = 0
                    DEFECIT = np.zeros((TIMESTEP))
                    for i in range(0,TIMESTEP):
                        if QRESOUT[i] < TR[i]:
                            DEFECIT[i] = TR[i] - QRESOUT[i]
                            ZDEFECIT = DEFECIT
                            
                            NUMBEROFFAILIURE = NUMBEROFFAILIURE + 1
                    # AVETARGETRELEASE = TR[i] / TIMESTEP
                    AVETARGETRELEASE = np.sum(TR,axis = 0)/TIMESTEP
                    if NUMBEROFFAILIURE == 0:
                        VOLNURABILITY = 0
                    else:
                        VOLNURABILITY = (np.sum(DEFECIT,axis = 0)/NUMBEROFFAILIURE )/(AVETARGETRELEASE)
                    
                        
                        
                    zz1 = VOLNURABILITY
                    zz2 = np.sum(DEFECIT,axis = 0)
                    zz3 = NUMBEROFFAILIURE
                    zz4 = AVETARGETRELEASE
                    return VOLNURABILITY
def SUSTAINABILITY(REL,RES,VOL):
                    SUS = 0 
                    zSUS = REL
                    zRES = RES
                    zVOL = VOL
                    zREL = REL
                
                    SUS = (REL * RES * (1-VOL)) ** (1/3)
                    return SUS
# ----------------------------------------------------------------------------
# # Call LISFLOOD         
# for i in range (0,uR):
#     for j in range(0,m-1):
#         st[0,i] = 20000000
#         st[j+1,i],qResOut[j,i] = Lisflood(st[j,i],Q_min[j,i],dt,F[j,i],storageR[0,i],l_c[i,0],Q_norm[j,i],l_n[i,0],l_f[i,0],qResin[j,i],Q_nonD[j,i],e[j,i])
 
# Call SOP   
# for i in range(0,uR):
#     for j in range(0,m):
#         st[0,i] =  sIni[0,i]
#         st[j+1,i],qResOut[j,i] = SOP(st[j,i],qResin[j,i],targetRelase[j,i],ka[0,i],sMin[0,i],dt,e[j,i])
# # Calculate Head     
# for i in range(0,uR):
#     for j in range(0,m-1):
#         h[j,i]  =   HEAD(st[j,i])
     
# # for i in range(0,uR):
#         rel =  ReliabilitySOP(qResOut[:,i],targetRelase[:,i],timestep) 
#         res =  RESELIENCESOP(qResOut[:,i],targetRelase[:,i],timestep)  
#         vol =  VolnurabilitySOP(qResOut[:,i],targetRelase[:,i],timestep)
        
# sus = SUSTAINABILITY(rel,res,vol)

        
        

# ---------------------------------------------------------------------------
# Write Data to Excel File 
# app = xw.App(visible=True)
# wb = xw.Book('D:\My Code New\DataforSalinatary\ReserviorsData.xlsx')
# wb1 = xw.Book('D:\My Code New\DataBank\AllocationDemand.xlsx')
# wb2 = xw.Book('D:\My Code New\DataBank\AllocationDemandPercentage.xlsx')
# sht = wb.sheets['Storage']
# sht1 = wb.sheets['QOut']
# sht3 = wb1.sheets['QresOutMain'] 
# sht4 = wb2.sheets['QresOutMainP'] 

# sht1.range('B3').clear()
# sht.range('B3').options(transpose=True).value = st[:,0]

# sht1.range('B3').clear()
# sht1.range('B3').options(transpose=True).value = qResOut[:,0]

# # Pass qresOut to Demands xcel for Allocation Process
# sht3.range('F2').clear()
# sht3.range('F2').options(transpose=True).value = qResOut[:,0]

# sht4.range('B2').clear()
# sht4.range('B2').options(transpose=True).value = qResOut[0:-1,0]
# app.kill()
        
                                                   
# plt.plot(t,qResOut)
# plt.legend(["ResOutflow"], loc ="upper right") 
# plt.xlabel('time(Month)')
# plt.ylabel('QRESERVIOR(m3/s)')
# plt.show()