import requests
import json


import requests
headers = {
    "x-newegg-portal-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJuZXdlZ2cuZGV2Iiwic3ViIjoianoyNiIsImVtYWlsIjoiSmVmZS5ZLlpoYW5nQG5ld2VnZy5jb20iLCJhdWQiOiJwb3J0YWwiLCJpYXQiOjE2MTQ5MTEzMjAsImV4cCI6MTYxNDk5ODMyMCwiZXh0cmEiOnsiZ3JvdXBzIjpbIiogR1AgcHJvamVjdCBhdXRvcGFydHMiLCIqIEdQIFByb2plY3QgRUMgUGVyc29uYWxpemF0aW9uIiwiQWxsb3dlZCBUZWFtcyBDYWxsaW5nIExpY2Vuc2UiLCJQcmUtQmFja2VuZCIsIiogR1Agc2l0ZSBjbnNoMDEiLCIqIEdQIHRlYW0gdGVjaCBldCBjbiIsIiogR1AgdGVhbSBtaXMgaW1hZ2Ugc3BsaXQgc3NsIiwiQWxsb3dlZCBSYWNrVGFibGUiLCIqIGdwIHRlYW0gbWlzIG5lc2MgazhzIiwiTkVTQyBFQyBTdXBlcnZpc29yIiwiKiBHUCBOQSBTSDAxIE1JUyIsIldFQlZQTi5OUy5QZXJtLkcyIiwiV0VCVlBOLk5TLlRva2VuLmZvci5FaXRoZXIuVlBOLm9yLlN0YWdpbmdTZXJ2ZXIiLCIqIEdQIFByb2plY3QgTmV3ZWdnR2xvYmFsIiwiKiBHUCBQcm9qZWN0IFE0Uy1NS1BMIERlZHVjdGlvbiIsIkFsbG93ZWQgU3RhZ2luZyBTZXJ2ZXJzIFVTIE1JUyBOb24tUENJIFJEUCBQZXJtaXNzaW9uIiwiQWxsb3dlZCBNS1QgM3JkIFBhcnR5IEFwcGxpY2F0aW9uIiwiKiBPUkcgQ04gU0ggTkVTQyBNSVMgVVMgRCBTU0wgKDMwNS40MzNcXCMzKSIsIiogR1AgdGVhbSBtaXMgbmVzYyBjbnNoIG5ld2VnZ2VjIG5nLXBsYXRmb3JtIiwiKiBHUCBwcm9qZWN0IFByZW1pZXIgU2VsbGVyIGFuZCBJbnRlcm5hdGlvbmFsIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggcHJvamVjdCBzZWxlY3Rpb24iLCIqIEdQIHRlYW0gbWlzIG5lc2MgY25zaCBuZXdlZ2dlYyBkZXZlbG9wZXIgc3NsIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggbmV3ZWdnZWMgY29kZXJldmlldyIsIiogR1AgdGVhbSBtaXMgbmVzYyBjbnNoIG5ld2VnZ2VjIGRldmVsb3BlciIsIiogR1AgdGVhbSBtaXMgbmVzYyBjbnNoIG5ld2VnZ2VjIHBtIiwiKiBHUCB0ZWFtIG1pcyBuZXNjIGNuc2ggbmV3ZWdnZWMiLCIqIHByb2plY3QtZnVsZmlsbGJ5bmV3ZWdnIChjbikiLCJERkZVc2VycyIsIi5uZXNjLXNoLm1pcy5lYy5EZXZlbG9wZXIiLCIqIHByb2plY3QtbWFya2V0cGxhY2UgKGNuKSIsIiogR1AgdGVhbSBtaXMgdXMgZWMgY2FjaGUiLCIubmVzYy1zaC5taXMuZWMubWFya2V0cGxhY2UiLCIqIEdQIHRlYW0gbWlzIG5lc2MgY25zaCBlYyBzdXBwb3J0IiwiQWxsb3dlZCBXZWJtYWlsIENOIFVzZXJzIiwiKiBhbGwgbmVzYyBwaWMiLCIqIEdQIHRlYW0gbWlzIG5lc2MgY25zaCBwbSBzdXBlcnZpc29ycyIsIiogR1AgYWxsIGVtcGxveWVlcyBjbiJdfX0.Fu8NzS-JnjToaYZJx_ceZ9nOCMp0MH7NteEuPKCGREA",
}
url = "http://dev.newegg.org/backend/api/api-callchains/83ea0fedc6277f3dcfcd7c340262072a"
response = requests.get(url, headers=headers).text


def BuildObj(dic):
    print("service name:", dic['ApiName'])
    print("interface name:", dic['RawUri'])
    if(isinstance(dic['Next'], list)):
        for nextObj in dic['Next']:
            BuildObj(nextObj)


def BuildRelation(dic):
    print(dic['ApiName'] , " own " , dic['RawUri'])
    if(isinstance(dic['Next'], list)):
        for nextObj in dic['Next']:
            print(dic['RawUri'] , " call " , nextObj['ApiName'])
            BuildRelation(nextObj)

aaa = json.loads(response)
BuildRelation(aaa)
