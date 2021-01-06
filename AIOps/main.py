import pandas as pd
import numpy as np

df1 = pd.read_csv('./last7days/process_cpu_seconds_total.csv')

df1 = df1.loc[df1['endpoint'] == 'http']

prodNameList = pd.pivot_table(df1, values='value', index=['pod']).index
table = pd.pivot_table(df1, values='value', index=['pod', 'timestamp'])

for prodName in prodNameList:
    print(prodName)
    print(table.loc[prodName].diff())


df2 = pd.read_csv('./last7days/http_requests_received_total.csv')

df1 = df1.loc[df1['endpoint'] == 'http']

prodNameList = pd.pivot_table(df1, values='value', index=['pod']).index
table = pd.pivot_table(df1, values='value', index=['pod', 'timestamp'])

for prodName in prodNameList:
    print(prodName)
    print(table.loc[prodName].diff())
