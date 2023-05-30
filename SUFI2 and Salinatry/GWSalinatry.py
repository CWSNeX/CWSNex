# Name:        EC 
# Purpose:     Determine EC on Groundwater
#
# Author:      Elham Soleimanian

# Created:     04/25/2021
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
# Import Data
Data  = pd.ExcelFile(r'C:\0el\DataforSalinatary\GWData (Autosaved).xlsx')
ec  = pd.read_excel(Data, 'Sheet1',usecols='B').to_numpy()
tds  = pd.read_excel(Data, 'Sheet1',usecols='c').to_numpy()
head  = pd.read_excel(Data, 'Sheet1',usecols='D').to_numpy()
precipitation  = pd.read_excel(Data, 'Sheet1',usecols='E').to_numpy()
evaporation = pd.read_excel(Data, 'Sheet1',usecols='F').to_numpy()
deepperculation = pd.read_excel(Data, 'Sheet1',usecols='G').to_numpy()
y = pd.read_excel(Data, 'Sheet1',usecols='B').to_numpy()

# Calculate Linear Correlation Between EC and Independent Variables
rtds = np.corrcoef(ec, tds, rowvar=False)
rhead = np.corrcoef(ec, head, rowvar=False)
rprecipitation = np.corrcoef(ec, precipitation, rowvar=False)
revaporation = np.corrcoef(ec, evaporation, rowvar=False)
rdeepperculation = np.corrcoef(ec, deepperculation, rowvar=False)

# Generate Regression Model Based On Importabt Parametes Which Drived from Previous Step
# Import Independent and Dependent Vriables 
x = pd.read_excel(Data, 'Sheet1',usecols='C:G').to_numpy()
# y = [0.56,0.12,0.47,0.293333,0.248333,0.203333,0.158333,0.113333,0.0683333,	0.0233333,0.7,0.414444,0.47254,	0.530635,0.58873,0.646825,0.704921,0.763016]
model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)
print('intercept:', model.intercept_)
print('slope:', model.coef_)
# Validate Generated Model
# y_pred = model.predict(x)
# print('predicted response:', y_pred, sep='\n')
