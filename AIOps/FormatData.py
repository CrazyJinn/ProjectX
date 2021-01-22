import pandas as pd
import numpy as np


def GetPodName():
    df = pd.read_csv('./last7days/process_cpu_seconds_total.csv')
    df = df.loc[:,['pod']].drop_duplicates()
    return df

def FormatCpuData():
    df = pd.read_csv('./last7days/process_cpu_seconds_total.csv')
    df = df.loc[df['endpoint'] == 'http']
    table = pd.pivot_table(df, values='value', index=['pod', 'timestamp'])
    return table


def FormatRequestTotal():
    df = pd.read_csv('./last7days/http_requests_received_total.csv')
    df = df.loc[df['endpoint'] == 'http']
    table = pd.pivot_table(df, values='value', index=[
        'pod', 'timestamp', 'code'], aggfunc=np.sum)
    return table


def FormatRequest200Total():
    return FormatRequestTotal().query('code == [200]')

def FormatRequestErrorTotal():
    return FormatRequestTotal().query('code != [200]')
