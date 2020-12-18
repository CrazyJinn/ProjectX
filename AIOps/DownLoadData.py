import csv
import requests
import sys
import time
import os

"""
A simple program to print the result of a Prometheus query as CSV.
"""

DATA_SOURCE = "https://e11k8s-prometheus.newegg.org"

# https://prometheus.io/docs/prometheus/latest/querying/api/#range-queries
end = int((time.time()) * 1000) / 1000
TIME_SPAN_DAYS = 7
start = (end - TIME_SPAN_DAYS * 24 * 60 * 60)
STEP = 600  # default duration is 14/h

nameSpace = 'ec-business-ssl'
serviceName = 'prod-ssl-realtime-v4'
metricsNames = [
    'http_requests_received_total',
    #   'process_open_handles',
    #   'process_num_threads',
    #   'http_request_duration_seconds_count',
    #   'http_requests_in_progress',
    #   'dotnet_collection_count_total',
    # 'http_request_duration_seconds_sum',
    'process_cpu_seconds_total'
]

for metrixName in metricsNames:

    query = '{0}{{namespace="{1}",service="{2}"}}'.format(metrixName, nameSpace, serviceName)
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
    for result in results:
        labelnames.update(result['metric'].keys())

    # Canonicalize
    labelnames.discard('__name__')
    labelnames = sorted(labelnames)

    filename = './last{0}days/{1}.csv'.format(TIME_SPAN_DAYS, metrixName)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(['name', 'timestamp', 'value'] + labelnames)

        # Write the sanples.
        for result in results:
            matrix = result['values']
            for m in matrix:
                l = [result['metric'].get('__name__', '')] + m
                for label in labelnames:
                    l.append(result['metric'].get(label, ''))
                writer.writerow(l)
