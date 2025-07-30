# tests/test_neo4j.py
from neo4j import GraphDatabase
import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
    
# Update these with your actual connection details
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

try:
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful!' as message")
        print(result.single()["message"])
    driver.close()
    print("✅ Neo4j connection working!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
