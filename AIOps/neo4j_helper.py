from py2neo import Graph, Node, Relationship, NodeMatcher
import requests
import json
import re


def add_interface_to_interface(graph, interface_name_from, interface_name_to):
    interface_node_from = build_interface_node(interface_name_from)
    interface_node_to = build_interface_node(interface_name_to)
    call_relation = Relationship.type('call')

    graph.merge(call_relation(interface_node_from, interface_node_to))


def add_service_to_interface(graph, service_name, interface_name, apigateway_name, deploy_platform, is_pci):
    service_node = build_service_node(service_name, apigateway_name, deploy_platform, is_pci)
    interface_node = build_interface_node(interface_name)
    own_relation = Relationship.type('own')
    graph.merge(own_relation(service_node, interface_node))


def set_interface_error_flag(graph, interface_name, sdb_lable, sbd_value):
    matcher = NodeMatcher(graph)
    tweet = matcher.match("Interface", interface_name=interface_name).first()
    if tweet:
        tweet[sdb_lable+'_sbd'] = sbd_value
        graph.push(tweet)


def get_k8s_service_list(tx):
    # return tx.run("MATCH (n:Service) RETURN n ")
    for record in tx.run("MATCH (n:Service {deploy_platform:'k8s'}) RETURN n.service_name,n.apigateway_name,n.is_pci "):
        print(record["n.service_name"])


def format_service_info(to_server, apigateway_name):
    if re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}$', to_server) != None:
        return (apigateway_name, 'other')
    else:
        return (to_server.split('.')[0], 'k8s')


def format_interface_url(raw_url):
    if re.search('api/', raw_url) != None:
        return raw_url.split('api/')[1]
    else:
        return raw_url


def is_pci(profile_key):
    if re.search('PK8S', profile_key) != None:
        return True
    else:
        return False


def build_service_node(service_name, apigateway_name, deploy_platform, is_pci):
    service_node = Node("Service", service_name=service_name,
                        apigateway_name=apigateway_name, deploy_platform=deploy_platform, is_pci=is_pci)
    service_node.__primarylabel__ = "Service"
    service_node.__primarykey__ = "service_name"
    return service_node


def build_interface_node(interface_name):
    interface_node = Node("Interface", interface_name=interface_name.lower(),
                          P90_sbd=0, error_request_sbd=0)
    interface_node.__primarylabel__ = "Interface"
    interface_node.__primarykey__ = "interface_name"
    return interface_node


def get_graph():
    return Graph(
        "bolt://localhost:7687",
        user="neo4j",
        password="jinn1989"
    )


def BuildGraph(graph, dic):
    if(dic['GatewayTransfer'] != True):  # 为True为api gateway内部转发，应该忽略
        service_name, deploy_platform = format_service_info(dic['ToServer'], dic['ApiName'])
        add_service_to_interface(graph, service_name, format_interface_url(
            dic['RawUri']), dic['ApiName'],  deploy_platform, is_pci(dic['ProfileKey']))

    if(isinstance(dic['Next'], list)):
        for nextService in dic['Next']:
            if(dic['GatewayTransfer'] != True):  # 为True为api gateway内部转发，应该忽略
                add_interface_to_interface(graph, format_interface_url(
                    dic['RawUri']), format_interface_url(nextService['RawUri']))
            BuildGraph(graph, nextService)


# headers = {
#     "x-newegg-portal-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJuZXdlZ2cuZGV2Iiwic3ViIjoiamo4NCIsImVtYWlsIjoiSmlubi5XLkppbmdAbmV3ZWdnLmNvbSIsImF1ZCI6ImdhdGV3YXkiLCJpYXQiOjE2MjA5ODAwNjQsImV4cCI6MTYyMTA2NzA2NCwiZXh0cmEiOnsiZ3JvdXBzIjpbIkFsbG93ZWQgVGVhbXMgQ2FsbGluZyBMaWNlbnNlIiwiKiBHUCBzaXRlIGNuc2gwMSIsIiogR1AgdGVhbSB0ZWNoIGV0IGNuIiwiQWxsb3dlZCBSYWNrVGFibGUiLCIqIGdwIHRlYW0gbWlzIG5lc2MgazhzIiwiKiBHUCBOQSBTSDAxIE1JUyIsIldFQlZQTi5OUy5Ub2tlbi5mb3IuRWl0aGVyLlZQTi5vci5TdGFnaW5nU2VydmVyIiwiKiBPUkcgQ04gU0ggTkVTQyBNSVMgVVMgRCBTU0wgKDMwNS40MzNcXCMzKSIsIkFsbG93ZWQgV2lGaSBORS1UZXN0IFVzZXJzIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggbmV3ZWdnZWMgZGV2ZWxvcGVyIHNzbCIsIiogR1AgdGVhbSBtaXMgbmVzYyBjbnNoIG5ld2VnZ2VjIGRldmVsb3BlciIsIiogR1AgdGVhbSBtaXMgbmVzYyBjbnNoIG5ld2VnZ2VjIHBtIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggbmV3ZWdnZWMiLCIqIEdQIGFsbCBlbXBsb3llZXMgY24iXX19.w_avDSBXnFnj6804wLPM-jOME_jCcnvME00c0GxHtkw",
# }
# url = "http://dev.newegg.org/backend/api/api-callchains/"

# tidList = ["6ad4907a2b69c19952034ed68abf9e30"]


# graph = get_graph()
# for tid in tidList:
#     response = requests.get(url+tid, headers=headers).text
#     aaa = json.loads(response)
#     for dic in aaa['Next']:
#         BuildGraph(graph, dic)

# driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "jinn1989"))
# with driver.session() as session:
#     session.read_transaction(get_k8s_service_list)
