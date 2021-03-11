from neo4j import GraphDatabase
import requests
import json

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "jinn1989"))


def add_Service_Interface(tx, service_name, interface_name):
    tx.run("MERGE (s:Service {name: $service_name}) "
           "MERGE (s)-[:own]->(i:Interface {name: $interface_name})",
           service_name=service_name, interface_name=interface_name)


def add_interface_Service(tx, service_name, interface_name):
    tx.run("MERGE (s:Service {name: $service_name}) "
           "MERGE (i:Interface {name: $interface_name}) "
           "MERGE (i)-[:call]->(s)",
           service_name=service_name, interface_name=interface_name)


def BuildGraph(session, dic):
    session.write_transaction(add_Service_Interface, dic['ApiName'], dic['RawUri'])
    if(isinstance(dic['Next'], list)):
        for nextService in dic['Next']:
            if(dic['ApiName'] != nextService['ApiName']):  # 当service名不相同时，产生调用关系；service名相同就属于Api gateway之间互相转发的情况
                session.write_transaction(add_interface_Service,
                                          nextService['ApiName'], dic['RawUri'])
            BuildGraph(session, nextService)


headers = {
    "x-newegg-portal-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJuZXdlZ2cuZGV2Iiwic3ViIjoiamo4NCIsImVtYWlsIjoiSmlubi5XLkppbmdAbmV3ZWdnLmNvbSIsImF1ZCI6InBvcnRhbCIsImlhdCI6MTYxNTM2MzU5MCwiZXhwIjoxNjE1NDUwNTkwLCJleHRyYSI6eyJncm91cHMiOlsiQWxsb3dlZCBUZWFtcyBDYWxsaW5nIExpY2Vuc2UiLCIqIEdQIHNpdGUgY25zaDAxIiwiKiBHUCB0ZWFtIHRlY2ggZXQgY24iLCJBbGxvd2VkIFJhY2tUYWJsZSIsIiogZ3AgdGVhbSBtaXMgbmVzYyBrOHMiLCIqIEdQIE5BIFNIMDEgTUlTIiwiV0VCVlBOLk5TLlRva2VuLmZvci5FaXRoZXIuVlBOLm9yLlN0YWdpbmdTZXJ2ZXIiLCIqIE9SRyBDTiBTSCBORVNDIE1JUyBVUyBEIFNTTCAoMzA1LjQzM1xcIzMpIiwiQWxsb3dlZCBXaUZpIE5FLVRlc3QgVXNlcnMiLCIqIEdQIHRlYW0gbWlzIG5lc2MgY25zaCBuZXdlZ2dlYyBkZXZlbG9wZXIgc3NsIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggbmV3ZWdnZWMgZGV2ZWxvcGVyIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggbmV3ZWdnZWMgcG0iLCIqIEdQIHRlYW0gbWlzIG5lc2MgY25zaCBuZXdlZ2dlYyIsIiogR1AgYWxsIGVtcGxveWVlcyBjbiJdfX0.Tb4_c6sdwkqHy_uTdduA6lvYtbTfnQrjDxXPkyw4iLY",
}
url = "http://dev.newegg.org/backend/api/api-callchains/"

tidList = ["0a1daa74d8cb14157ef0ba829e5e311b",
           "8bc029e8c22915d554dab5a8ee7baae8", "e05f69a8911ae7a07445c02eda89a315"]

for tid in tidList:
    response = requests.get(url+tid, headers=headers).text
    aaa = json.loads(response)
    with driver.session() as session:
        BuildGraph(session, aaa['Next'][0])
