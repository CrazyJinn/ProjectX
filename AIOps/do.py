import matplotlib.pyplot as plt
from numpy.lib.financial import fv
import GetData as gd
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
import DownLoadOnlineData as ddd
import neo4j_helper as nh
import service_info_helper as sh


magicNumber = 30


def SBD(v):
    a = np.ones(magicNumber)  # 暂时全和1比较
    correlate = np.correlate(a, v, mode='full')
    norm1 = np.linalg.norm(a)
    norm2 = np.linalg.norm(v)
    return 1 - np.max(correlate / (norm1 * norm2))


def FindCentroid(labels, sbdValue):
    result = np.dstack((labels, sbdValue))[0]
    # print("============ train data =============")
    # print(result)
    # print("============ ========== =============")
    result = result[np.where(result[:, 0] >= 0)]  # 排除未分类的点(-1为分类失败)
    result = result[np.argsort(result[:, 0])]  # 按照聚类排序
    result = np.split(result[:, 1], np.unique(result[:, 0], return_index=True)[1][1:])
    fvk = []
    for temp in result:
        fvk.append(np.mean(temp, axis=0))
    return fvk


# serviceInfoList = [
#     ('prod-ssl-auth-v2', 'ec-business-ssl', "nonPCI"),
#     ('prod-ssl-cart-v3', 'ec-business-ssl', "nonPCI"),
#     ('prod-ssl-customer-v4', 'ec-business-ssl', "nonPCI"),
#     ('prod-ssl-realtime-v4', 'ec-business-ssl', "nonPCI"),
#     ('prod-ssl-basicdata-v2', 'ec-business-ssl', "nonPCI"),
#     ('prod-ssl-shoppingservice-v5', 'ec-business-ssl', "nonPCI"),
#     ('prod-shippingservice', 'ec-business-ssl', "nonPCI"),

#     ('prod-shoppingflow-v3', 'ec-business-ssl', "PCI"),
#     ('prod-desktop-shopping-v1', 'ec-app-website-b2c', "PCI"),
# ]

serviceInfoList = [
    ('gqc-auth-v2', 'ec-business-ssl', "nonPCI"),
    ('gqc-cart-v3', 'ec-business-ssl', "nonPCI"),
    ('gqc-customer-v4', 'ec-business-ssl', "nonPCI"),
    ('gqc-realtime-v4', 'ec-business-ssl', "nonPCI"),
    # ('gqc-basicdata-v2', 'ec-business-ssl', "nonPCI"),
    ('gqc-shoppingservice-v5', 'ec-business-ssl', "nonPCI"),
    ('gqc-shippingservice', 'ec-business-ssl', "nonPCI"),

    ('gqc-shoppingflow-v3', 'ec-business-ssl', "PCI"),
    ('gqc-desktop-shopping', 'ec-app-website-b2c', "PCI"),
]

def P90():
    graph = nh.get_graph()

    for serviceInfo in serviceInfoList:
        test_df = ddd.GetOnlineData_le(serviceInfo[2], serviceInfo[1], serviceInfo[0], 'http_request_duration_seconds_bucket')
        test_data = gd.get_P90(test_df, magicNumber)

        sbdValue = np.array([])

        for key, value in test_data.items():
            sbdValue = np.append(sbdValue, SBD(value))

        result = list(zip(sbdValue, test_data.keys(), test_data.values()))

        print(serviceInfo)
        print("+++++++++++++++")
        # print(result)
        for aaa in result:
            interface_name = aaa[1].split('---')[0]
            nh.set_interface_error_flag(graph, sh.format_interface_name(interface_name),'P90', aaa[0])

def error():
    graph = nh.get_graph()

    for serviceInfo in serviceInfoList:
        test_df = ddd.GetOnlineData(serviceInfo[2], serviceInfo[1], serviceInfo[0], 'http_requests_received_total')
        test_data = gd.get_request_error(test_df, magicNumber)

        sbdValue = np.array([])

        for key, value in test_data.items():
            sbdValue = np.append(sbdValue, SBD(value+1)) #全部+1，避免[0,0,0,1,0]这样的数据进来算SBD会非常高

        result = list(zip(sbdValue, test_data.keys(), test_data.values()))

        print(serviceInfo)
        print("+++++++++++++++")
        print(result)
        for aaa in result:
            interface_name = aaa[1].split('---')[0]
            nh.set_interface_error_flag(graph, sh.format_interface_name(interface_name),'error_request', aaa[0])

def error_rate():
    graph = nh.get_graph()

    for serviceInfo in serviceInfoList:
        test_df = ddd.GetOnlineData(serviceInfo[2], serviceInfo[1], serviceInfo[0], 'http_requests_received_total')
        test_data = gd.get_request_error(test_df, magicNumber)

        sbdValue = np.array([])

        for key, value in test_data.items():
            sbdValue = np.append(sbdValue, SBD(value+1)) #全部+1，避免[0,0,0,1,0]这样的数据进来算SBD会非常高

        result = list(zip(sbdValue, test_data.keys(), test_data.values()))

        print(serviceInfo)
        print("+++++++++++++++")
        print(result)
        for aaa in result:
            interface_name = aaa[1].split('---')[0]
            nh.set_interface_error_flag(graph, sh.format_interface_name(interface_name),'error_request', aaa[0])

P90()
error()