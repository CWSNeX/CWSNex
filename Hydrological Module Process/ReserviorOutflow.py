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
import matplotlib.pyplot as plt
#-------------------------------------------------------------------------
##########################################################################
##########################################################################
############ ***** Required Data for LISFLOOD Method ***** ###############
##########################################################################
##########################################################################
# Import River Flow from KinimaticWithInterflow Madule
Data  = pd.read_excel(r'D:\My Code New\DataBank\QRESIN.xlsx')
qResin = pd.DataFrame(Data,columns = ['QRESIN1','QRESIN2','QRESIN3','QRESIN4']).to_numpy()
[m,u] = qResin.shape
#-------------------------------------------------------------------------
# Import constant Related to Each Reservior
Data  = pd.read_excel(r'D:\My Code New\DataBank\ReserviorsConstants.xlsx')
s = pd.DataFrame(Data,columns = ['Total Storage Capacity(m3)']).to_numpy()
l_c = pd.DataFrame(Data,columns = ['Conservative Storage(m3)']).to_numpy()
l_f = pd.DataFrame(Data,columns = ['Flood Storage(m3)']).to_numpy()
l_n = pd.DataFrame(Data,columns = ['Availabe Capacity(m3)']).to_numpy()
area = pd.DataFrame(Data,columns = ['Area(m2)']).to_numpy()
#-------------------------------------------------------------------------
# Import Discharges Related to River
data = pd.ExcelFile(r'D:\My Code New\DataBank\Qnorm_MinfromReservior.xlsx')
Q_min = pd.read_excel(data, 'Qmin',usecols='A:D').to_numpy()
Q_norm =  pd.read_excel(data, 'Qnorm',usecols='A:D').to_numpy()
QnonD =  pd.read_excel(data, 'QnonD',usecols='A:D').to_numpy()

#------------------------------------------------------------------------
# Import time Step(s)
dt = 3*60
t = np.linspace(0,120,42) 
#------------------------------------------------------------------------
# Preallocation Matrix
qResOut = np.zeros((m,u))
f = np.zeros((m,u))
st = np.zeros((m,u))
z = np.zeros((m,u))
Alpha = np.zeros((0,u))
#------------------------------------------------------------------------
############################################################################
############################################################################
# ################### ***** Required Data for SOP Methode ***** ############
############################################################################
############################################################################
#Import Target Release from each Reservior
Data  = pd.read_excel(r'D:\My Code New\DataBank\TargetRelaseforSOP.xlsx')
targetRelase = pd.DataFrame(Data,columns = ['TargetRelase1','TargetRelase2','TargetRelase3','TargetRelase4']).to_numpy()
# Import sMin & sini $ ka & sMax for each Reservior
Data  = pd.read_excel(r'D:\My Code New\DataBank\ReserviorConstantsforSOP.xlsx')
data = pd.ExcelFile(r'D:\My Code New\DataBank\ReserviorConstantsforSOP.xlsx')
sMin = pd.DataFrame(Data,columns = ['Smin1','Smin2','Smin3','Smin4']).to_numpy()
sIni = pd.read_excel(data,'Sini')
sIni = pd.DataFrame(sIni,columns = ['Sini1','Sini2','Sini3','Sini4']).to_numpy()
sMax = pd.read_excel(data,'Smax')
sMax = pd.DataFrame(sMax,columns = ['Smax1','Smax2','Smax3','Smax4']).to_numpy()
ka = pd.read_excel(data,'ka')
ka = pd.DataFrame(sMax,columns = ['Ka1','Ka2','Ka3','Ka4']).to_numpy()
#-----------------------------------------------------------------------
############# ***** Following Function calculate Reservior Outflow *****##############
# This function is based on distributed LISFLOOD Hydrological Model
def Lisflood(QMIN,DT,F,S,LC,QNORM,LN,LF,QRESIN,QNOND,ST):
            QRESOUT = 0
            
            if F <= 2*LC:
                QRESOUT = min(QMIN,1/DT * F * S)
            elif F > 2*LC and F <= LN:
                QRESOUT = QMIN + (QNORM - QMIN) * (F - 2 * LC)/(LN - 2 * LC)
            elif F > LN and F <= LF:
                QRESOUT = QNORM + ((F - LN)/(LF - LN)) * max((QRESIN - QNORM) , (QNOND - QNORM))
            elif F > LF:
                QRESOUT =  max(((F - LF)/DT) * S, QNOND)
            return QRESOUT
        
# for i in range (0,u):
#     for j in range(0,m):
#         st[j,i] = qResin[j,i] * 180
#         f[j,i] = (st[j,i]/s[i,0]) 
#         qResOut[j,i] = Lisflood(Q_min[j,i],dt,f[j,i],s[i,0],l_c[i,0],Q_norm[j,i],l_n[i,0],l_f[i,0],qResin[j,i],Q_nonD[j,i],st[j,i])



def SOP(ST,QRESIN,TR,KA,SMAX,SMIN):  
        QRESOUT = 0
        
        if ST <= SMAX and ST >= SMIN:
            QRESOUT = TR
            
        elif ST > SMAX:
            QRESOUT = TR + ST - KA
            ST = KA
        else:
            QRESOUT = TR + ST - SMIN
            ST = SMIN
        return QRESOUT
    
def Reliability(QRESOUT,TR,ST,KA,SMIN):
              
                if QRESOUT == TR:
                    Z = 1
                elif QRESOUT == TR + ST - KA:
                    Z = 0 
                else: 
                    Z = 0
                return Z
    
for i in range(0,u):
    for j in range(0,m-1):
        st[0,i] =  sIni[0,i]
        qResOut[j,i] = SOP(st[j,i],qResin[j,i],targetRelase[j,i],ka[0,i],sMax[0,i],sMin[0,i])
        st[j+1,i] = st[j,i] + qResin[j,i] - qResOut[j,i]
        z[j,i] = Reliability(qResOut[j,i],targetRelase[j,i],st[j,i],ka[0,i],sMin[0,i])
        
# Alpha =  [sum(x) for x in zip(*z)]
Alpha = np.sum(z,axis = 0)/41

        
                                                   
plt.plot(t,qResOut)
plt.legend(["ResOutflow1", "ResOutflow2","ResOutflow3","ResOutflow4"], loc ="upper right") 
plt.xlabel('time(min)')
plt.ylabel('QRESERVIOR(CFC)')
plt.show()