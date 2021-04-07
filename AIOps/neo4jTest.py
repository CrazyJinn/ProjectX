from neo4j import GraphDatabase
import requests
import json

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "jinn1989"))


def add_interface_to_interface(tx, service_name_from, interface_name_from, service_name_to, interface_name_to):
    tx.run("MERGE (if:Interface {interface_name: $interface_name_from,service_name: $service_name_from }) "
           "MERGE (it:Interface {interface_name: $interface_name_to,service_name: $service_name_to }) "
           "MERGE (if)-[r:call]->(it) SET r.weight = coalesce(r.weight, 0) + 1 ",
           service_name_from=service_name_from, interface_name_from=interface_name_from,
           service_name_to=service_name_to, interface_name_to=interface_name_to)


def BuildGraph(session, dic):
    if(isinstance(dic['Next'], list)):
        for nextService in dic['Next']:
            if(dic['ApiName'] != nextService['ApiName']):  # 当service名不相同时，产生调用关系；service名相同就属于Api gateway之间互相转发的情况
                session.write_transaction(add_interface_to_interface,
                                          dic['ApiName'], dic['RawUri'], nextService['ApiName'], nextService['RawUri'])
            BuildGraph(session, nextService)


headers = {
    "x-newegg-portal-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJuZXdlZ2cuZGV2Iiwic3ViIjoianoyNiIsImVtYWlsIjoiSmVmZS5ZLlpoYW5nQG5ld2VnZy5jb20iLCJhdWQiOiJwb3J0YWwiLCJpYXQiOjE2MTU0NTczNjMsImV4cCI6MTYxNTU0NDM2MywiZXh0cmEiOnsiZ3JvdXBzIjpbIiogR1AgcHJvamVjdCBhdXRvcGFydHMiLCIqIEdQIFByb2plY3QgRUMgUGVyc29uYWxpemF0aW9uIiwiQWxsb3dlZCBUZWFtcyBDYWxsaW5nIExpY2Vuc2UiLCJQcmUtQmFja2VuZCIsIiogR1Agc2l0ZSBjbnNoMDEiLCIqIEdQIHRlYW0gdGVjaCBldCBjbiIsIiogR1AgdGVhbSBtaXMgaW1hZ2Ugc3BsaXQgc3NsIiwiQWxsb3dlZCBSYWNrVGFibGUiLCIqIGdwIHRlYW0gbWlzIG5lc2MgazhzIiwiTkVTQyBFQyBTdXBlcnZpc29yIiwiKiBHUCBOQSBTSDAxIE1JUyIsIldFQlZQTi5OUy5QZXJtLkcyIiwiV0VCVlBOLk5TLlRva2VuLmZvci5FaXRoZXIuVlBOLm9yLlN0YWdpbmdTZXJ2ZXIiLCIqIEdQIFByb2plY3QgTmV3ZWdnR2xvYmFsIiwiKiBHUCBQcm9qZWN0IFE0Uy1NS1BMIERlZHVjdGlvbiIsIkFsbG93ZWQgU3RhZ2luZyBTZXJ2ZXJzIFVTIE1JUyBOb24tUENJIFJEUCBQZXJtaXNzaW9uIiwiQWxsb3dlZCBNS1QgM3JkIFBhcnR5IEFwcGxpY2F0aW9uIiwiKiBPUkcgQ04gU0ggTkVTQyBNSVMgVVMgRCBTU0wgKDMwNS40MzNcXCMzKSIsIiogR1AgdGVhbSBtaXMgbmVzYyBjbnNoIG5ld2VnZ2VjIG5nLXBsYXRmb3JtIiwiKiBHUCBwcm9qZWN0IFByZW1pZXIgU2VsbGVyIGFuZCBJbnRlcm5hdGlvbmFsIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggcHJvamVjdCBzZWxlY3Rpb24iLCIqIEdQIHRlYW0gbWlzIG5lc2MgY25zaCBuZXdlZ2dlYyBkZXZlbG9wZXIgc3NsIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggbmV3ZWdnZWMgY29kZXJldmlldyIsIiogR1AgdGVhbSBtaXMgbmVzYyBjbnNoIG5ld2VnZ2VjIGRldmVsb3BlciIsIiogR1AgdGVhbSBtaXMgbmVzYyBjbnNoIG5ld2VnZ2VjIHBtIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggbmV3ZWdnZWMiLCIqIHByb2plY3QtZnVsZmlsbGJ5bmV3ZWdnIChjbikiLCJERkZVc2VycyIsIi5uZXNjLXNoLm1pcy5lYy5EZXZlbG9wZXIiLCIqIHByb2plY3QtbWFya2V0cGxhY2UgKGNuKSIsIiogR1AgdGVhbSBtaXMgdXMgZWMgY2FjaGUiLCIubmVzYy1zaC5taXMuZWMubWFya2V0cGxhY2UiLCIqIEdQIHRlYW0gbWlzIG5lc2MgY25zaCBlYyBzdXBwb3J0IiwiQWxsb3dlZCBXZWJtYWlsIENOIFVzZXJzIiwiKiBhbGwgbmVzYyBwaWMiLCIqIEdQIHRlYW0gbWlzIG5lc2MgY25zaCBwbSBzdXBlcnZpc29ycyIsIiogR1AgYWxsIGVtcGxveWVlcyBjbiJdfX0.iS8JmZQPt91kyAQ8Qn-kEmS4tCsbOjPJ3hVwJVItUCw",
}
url = "http://dev.newegg.org/backend/api/api-callchains/"

tidList = ["0a1daa74d8cb14157ef0ba829e5e311b",
           "8bc029e8c22915d554dab5a8ee7baae8", "e05f69a8911ae7a07445c02eda89a315", "3781f4b95280b1c27909be1a5e7a4c95"]


for tid in tidList:
    response = requests.get(url+tid, headers=headers).text
    aaa = json.loads(response)
    with driver.session() as session:
        for dic in aaa['Next']:
            BuildGraph(session, dic)
