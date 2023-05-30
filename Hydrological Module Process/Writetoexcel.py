# from openpyxl import *
# #Load existing excel file into a Workbook object
# wb=load_workbook("D:\My Code New\DataBank\BalanceEquation.xlsx")
# #Creates a Worksheet variable 'ws' containing the worksheet with name "Sheet1".
# ws=wb["Evaporation"]
# #Access the cell located at row 6 and column 1 using a variable of type Cell
# wcell1=ws.cell(6,4)
# wcell1.value=5
# wcell2=ws.cell(6,2)
# wcell2.value="Williams"

# #Saving the excel file using "wb.save" method
# wb.save("D:\My Code New\DataBank\BalanceEquation.xlsx")

# ---------------------------------------------------------------------------
import pandas as pd
df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
                    index=['row 1', 'row 2'],
                    columns=['col 1', 'col 2'])
df1.to_excel("output.xlsx") 
df1.to_excel("output.xlsx",
              sheet_name='Sheet_name_1') 
df2 = df1.copy()
with pd.ExcelWriter('output.xlsx') as writer:  
    df1.to_excel(writer, sheet_name='Sheet_name_1')
    df2.to_excel(writer, sheet_name='Sheet_name_2')
    
    
# with pd.ExcelWriter('output.xlsx',
#                      mode='a') as writer:  
#     df.to_excel(writer, sheet_name='Sheet_name_3')
    
df1.to_excel('output1.xlsx', engine='xlsxwriter')  

