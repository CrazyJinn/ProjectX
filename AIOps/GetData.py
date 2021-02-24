import pandas as pd
import numpy as np


def GetPodName(path):
    df = pd.read_csv(path)
    df = df.loc[:, ['pod']].drop_duplicates()
    return df.pod.values


def GetCpuData(path):
    df = pd.read_csv(path)
    df = df.loc[df['endpoint'] == 'http']
    table = pd.pivot_table(df, values='value', index=['pod', 'timestamp'])
    return table


def GetRequestTotal(path):
    df = pd.read_csv(path)
    df = df.loc[df['endpoint'] == 'http']
    table = pd.pivot_table(df, values='value', index=['pod', 'timestamp', 'code'], aggfunc=np.sum)
    return table


def GetRequest200Total():
    return GetRequestTotal().query('code == [200]')


def GetRequestErrorTotal():
    return GetRequestTotal().query('code != [200]')
