from neo4j import GraphDatabase

class Neo4jConnection:    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
    
    def add_node(self, label, properties):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session() 
            response = session.execute_write(self.__create_node, label, properties)
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        assert response is not None, "Failed to create node"
        return response
    
    @staticmethod
    def __create_node(tx, label, properties):
        query = "MERGE (a:{}{}) RETURN a".format(label, properties).replace("{'", "{").replace("':", ":").replace(", '", ", ")
        result = tx.run(query, properties=properties)
        return result.data()

    def create_link(self, sourceLink, targetLink, relationType):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session() 
            response = session.execute_write(self.__create_link, sourceLink, targetLink, relationType)
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        assert response is not None, "Failed to create link"
        return response
    
    @staticmethod
    def __create_link(tx, sourceLink, targetLink, relationType):
        query = '''
        MATCH (s), (p)
        WHERE s.link = $sourceLink AND p.link = $targetLink
        MERGE (s)-[:{}]->(p)'''.format(relationType)
        result = tx.run(query, sourceLink=sourceLink, targetLink=targetLink)
        return result.data()
    
    def get_relation(self, sourceType, source, relationType = ""):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session() 
            response = session.execute_write(self.__get_relation, sourceType, source, relationType)
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        assert response is not None, "Failed to get relation"
        return response
    
    @staticmethod
    def __get_relation(tx, sourceType, source, relationType):
        relationType = "" if relationType == "" else ":" + relationType
        query = '''
        MATCH (:{}{})-[{}]->(node)
        RETURN node'''.format(sourceType, source, relationType).replace("{'", "{").replace("':", ":").replace(", '", ", ")
        result = tx.run(query)
        return result.data()

    def add_word(self, link):
        return self.add_node("Word", {'link': link})

    def get_word_relation(self, sourceLink):
        return self.get_relation("Word", {'link': sourceLink})

if __name__ == "__main__":
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="superman", pwd="pizza")    
    print("add Word :", conn.add_word("https://en.wikipedia.org/wiki/Artificial_intelligence"))
    print("add Word :", conn.add_word("https://en.wikipedia.org/wiki/Machine_learning"))
    print("add Word :", conn.add_word("https://en.wikipedia.org/wiki/Deep_learning"))
    print("create Link :", conn.create_link("https://en.wikipedia.org/wiki/Artificial_intelligence", "https://en.wikipedia.org/wiki/Machine_learning", "partOf"))
    print("get word relation :", conn.get_word_relation("https://en.wikipedia.org/wiki/Artificial_intelligence"))
