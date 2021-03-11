# pip3 install neo4j-driver
# python3 example.py

from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
  "bolt://3.237.67.131:7687",
  auth=basic_auth("neo4j", "hydraulics-operability-division"))

cypher_query = '''
MATCH (p:Person {healthstatus:$status})-[v:VISITS]->(pl:Place) 
WHERE p.confirmedtime < v.starttime 
RETURN distinct pl.name as place LIMIT 20
'''

with driver.session(database="neo4j") as session:
  results = session.read_transaction(
    lambda tx: tx.run(cypher_query,
                      status="Sick").data())
  for record in results:
    print(record['place'])

driver.close()
