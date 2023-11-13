from gdb_clients.neo4j_db import Neo4j

if __name__ == '__main__':
    uri = r'neo4j://localhost:10201'
    client = Neo4j(uri=uri, username='neo4j', passwd='testtest')
    client.clear()
    query = r'MATCH (en:Entity {EntityType:"Offer"}) <-[:E_EN]- (e:Event) -[df:DF]-> (e2:Event) -[:E_EN]-> (en2:Entity {EntityType:"Offer"}) WHERE df.EntityType = "Case_AWO" RETURN count(df)'
    query = 'EXPLAIN ' + query
    print(client.run(query))