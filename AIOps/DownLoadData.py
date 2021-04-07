import csv
import requests
import sys
import time
import os
import numpy as np

"""
A simple program to print the result of a Prometheus query as CSV.
"""

DATA_SOURCE = "https://e11k8s-prometheus.newegg.org"

# https://prometheus.io/docs/prometheus/latest/querying/api/#range-queries
end = int((time.time()) * 1000) / 1000
TIME_SPAN_DAYS = 3
start = (end - TIME_SPAN_DAYS * 24 * 60 * 60)
STEP = 120  # 单位s

serviceInfoList = [
    ('prod-ssl-cart-v3', 'ec-business-ssl')
    # ('prod-ssl-shoppingservice-v5', 'ec-business-ssl'),
    # ('prod-ssl-minicart-v2', 'ec-business-ssl'),
    # ('prod-item', 'ec-business-www'),
    # ('prod-ngmwww', 'ec-app-mobile'),
]

metricsNameList = [
    # 'http_requests_received_total',
    # 'process_open_handles',
    # 'process_num_threads',
    # 'http_request_duration_seconds_count',
    # 'http_requests_in_progress',
    # 'dotnet_collection_count_total',
    # 'http_request_duration_seconds_sum',
    # 'process_cpu_seconds_total',
    'http_request_duration_seconds_bucket'
]

for serviceInfo in serviceInfoList:
    for metrixName in metricsNameList:
        query = '{0}{{namespace="{1}",service="{2}"}}'.format(
            metrixName, serviceInfo[1], serviceInfo[0])
        params = {
            'query': query,
            'start': start,
            'end': end,
            'step': STEP
        }

        response = requests.get('{0}/api/v1/query_range'.format(DATA_SOURCE), params)
        results = response.json()['data']['result']

        # Build a list of all labelnames used.
        labelnames = set()
        # for result in results:
        labelnames.update(results[0]['metric'].keys())

        # Canonicalize
        labelnames.discard('__name__')
        labelnames = sorted(labelnames)

        filename = './last{0}days/{1}/{2}.csv'.format(TIME_SPAN_DAYS, serviceInfo[0], metrixName)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, mode='w+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header
            writer.writerow(labelnames+['timeRange', 'value'])

            # Write the sanples.
            for result in results:
                l = []
                for label in labelnames:
                    l.append(result['metric'].get(label, ''))
                temp = np.array(result['values'])
                timeSpan = temp[:, 0]
                value = temp[:, 1].astype(float)
                timeRange = timeSpan[0] + "-" + timeSpan[-1]
                l.append(timeRange)
                l.append(np.diff(value).tolist())
                writer.writerow(l)
