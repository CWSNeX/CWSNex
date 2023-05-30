# -------------------------------------------------------------------------
# Name:        Call All Modules 
# Purpose:     call all the developed moduled to run respectively
#
# Author:      Elham soleimanian
#
# Created:     2/13/2021
# -------------------------------------------------------------------------
import Evaporation 
from Evaporation import( u,m,E)
from Evaporation import(Sradiation,Temp)
# print(__name__)
for i in range(0,u):
   for j in range(0,m):
        E[j,i] = Evaporation.JensenEvaporation(Sradiation[j,i],Temp[j,i])


