import pandas as pd
from pathlib import Path
# src_file = Path.cwd() /  'shipping_tables.xlsx'

# df = pd.read_excel(src_file, header=1, usecols='B:F')
data = pd.ExcelFile(r'D:\My Code New\DataBank\Qnorm_MinfromReservior.xlsx')
Q_min = pd.read_excel(data, 'Qmin',usecols='A:D').to_numpy()
# Q_min = pd.DataFrame(Q_min,usecols='B:F').to_numpy()

dx = np.concatenate((disfood, disenergy))
dx[dx==0]=np.nan
dx = np.sort(dx, axis=0)
k = np.count_nonzero(DisConsumer)