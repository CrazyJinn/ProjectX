import csv
import requests
import time
import os
import numpy as np
import pandas as pd


def get_data(data_source, namespace, serviceName, metricsName):
    # https://prometheus.io/docs/prometheus/latest/querying/api/#range-queries
    end = int((time.time()) * 1000) / 1000
    # start = (end - 1 * 60 * 60)
    # STEP = 120  # 单位s
    start = (end - 15 * 60)
    STEP = 30  # 单位s
    query = '{0}{{namespace="{1}",service="{2}"}}'.format(metricsName, namespace, serviceName)
    params = {
        'query': query,
        'start': start,
        'end': end,
        'step': STEP
    }
    # DATA_SOURCE_Dic = {
    #     "nonPCI": "https://e11k8s-prometheus.newegg.org",
    #     "PCI": "https://e11pk8s-prometheus.newegg.org"
    # }

    DATA_SOURCE_Dic = {
        "nonPCI": "https://gqc-prometheus.newegg.org/",
        "PCI": "https://gqc-prometheus.newegg.org/"
    }
    response = requests.get('{0}/api/v1/query_range'.format(DATA_SOURCE_Dic[data_source]), params)
    return response

#pN数据带le
def GetOnlineData_le(data_source, namespace, serviceName, metricsName):
    response = get_data(data_source, namespace, serviceName, metricsName)
    results = response.json()['data']['result']

    # Build a list of all labelnames used.
    labelnames = set()
    # for result in results:
    labelnames.update(results[0]['metric'].keys())

    # Canonicalize
    labelnames.discard('__name__')
    labelnames.discard('owner')
    labelnames = sorted(labelnames)

    seriesList = []

    # writeCSV(results)

    # Write the sanples.
    for result in results:
        if(result['metric'].get('action') == None and result['metric'].get('controller') == None):   # 排除FAQ
            continue
        l = []
        for label in labelnames:
            if(label == 'code'):
                l.append(int(result['metric'].get(label)))
            elif (label == 'le'):
                l.append(float(result['metric'].get(label)))
            else:
                l.append(result['metric'].get(label))
        temp = np.array(result['values'])
        timeSpan = temp[:, 0]
        value = temp[:, 1].astype(float)
        timeRange = timeSpan[0] + "-" + timeSpan[-1]
        l.append(timeRange)
        temp_len = 31 - len(value)  #todo
        l.append(np.pad(np.diff(value),(temp_len,0),'constant',constant_values=(0,0)))
        seriesList.append(pd.Series(data=l, index=['action', 'code', 'controller', 'endpoint', 'instance',
                                                   'job', 'le', 'method', 'namespace', 'pod', 'service', 'timeRange', 'value']))
    df = pd.DataFrame(data=seriesList)
    return df

def GetOnlineData(data_source, namespace, serviceName, metricsName):
    response = get_data(data_source, namespace, serviceName, metricsName)
    results = response.json()['data']['result']

    # Build a list of all labelnames used.
    labelnames = set()
    # for result in results:
    labelnames.update(results[0]['metric'].keys())

    # Canonicalize
    labelnames.discard('__name__')
    labelnames.discard('owner')
    labelnames = sorted(labelnames)

    seriesList = []

    # writeCSV(results)

    # Write the sanples.
    for result in results:
        if(result['metric'].get('action') == None and result['metric'].get('controller') == None):   # 排除FAQ
            continue
        l = []
        for label in labelnames:
            if(label == 'code'):
                l.append(int(result['metric'].get(label)))
            elif (label == 'le'):
                l.append(float(result['metric'].get(label)))
            else:
                l.append(result['metric'].get(label))
        temp = np.array(result['values'])
        timeSpan = temp[:, 0]
        value = temp[:, 1].astype(float)
        timeRange = timeSpan[0] + "-" + timeSpan[-1]
        l.append(timeRange)
        temp_len = 31 - len(value) #todo
        l.append(np.pad(np.diff(value),(temp_len,0),'constant',constant_values=(0,0)))
        seriesList.append(pd.Series(data=l, index=['action', 'code', 'controller', 'endpoint', 'instance',
                                                   'job', 'method', 'namespace', 'pod', 'service', 'timeRange', 'value']))
    df = pd.DataFrame(data=seriesList)
    return df

# def writeCSV(results):
#     labelnames = set()
#     # for result in results:
#     labelnames.update(results[0]['metric'].keys())

#     # Canonicalize
#     labelnames.discard('__name__')
#     labelnames = sorted(labelnames)

#     filename = './debugData/1.csv'
#     os.makedirs(os.path.dirname(filename), exist_ok=True)

#     with open(filename, mode='w+', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         # Write the header
#         writer.writerow(labelnames+['timeRange', 'value'])

#         # Write the sanples.
#         for result in results:
#             if(result['metric'].get('action') == None and result['metric'].get('controller') == None):   # 排除FAQ
#                 continue
#             l = []
#             for label in labelnames:
#                 l.append(result['metric'].get(label, ''))
#             temp = np.array(result['values'])
#             timeSpan = temp[:, 0]
#             value = temp[:, 1].astype(float)
#             timeRange = timeSpan[0] + "-" + timeSpan[-1]
#             l.append(timeRange)
#             l.append(np.diff(value).tolist())
#             writer.writerow(l)
