import sqlite3
import pandas as pd
from neo4j import GraphDatabase
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Neo4jMigrator:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password, sqlite_db_path):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.sqlite_db_path = sqlite_db_path

    def close(self):
        self.driver.close()

    def clear_database(self):
        """Clear all nodes and relationships in Neo4j database"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Cleared Neo4j database")

    def create_constraints_and_indexes(self):
        """Create constraints and indexes for better performance"""
        with self.driver.session() as session:
            # Create constraints for unique identifiers
            constraints = [
                "CREATE CONSTRAINT app_name_unique IF NOT EXISTS FOR (a:Application) REQUIRE a.name IS UNIQUE",
                "CREATE CONSTRAINT category_name_unique IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE",
                "CREATE CONSTRAINT vendor_name_unique IF NOT EXISTS FOR (v:Vendor) REQUIRE v.name IS UNIQUE",
                "CREATE CONSTRAINT department_name_unique IF NOT EXISTS FOR (d:Department) REQUIRE d.name IS UNIQUE",
                "CREATE CONSTRAINT person_name_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE"
            ]

            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.info(f"Created constraint: {constraint}")
                except Exception as e:
                    logger.warning(f"Constraint may already exist: {e}")

    def load_data_from_sqlite(self):
        """Load data from SQLite database"""
        conn = sqlite3.connect(self.sqlite_db_path)
        df = pd.read_sql_query("SELECT * FROM applications", conn)
        conn.close()
        return df

    def create_application_nodes(self, df):
        """Create Application nodes"""
        with self.driver.session() as session:
            for _, row in df.iterrows():
                query = """
                CREATE (a:Application {
                    name: $name,
                    description: $description,
                    version: $version,
                    annual_cost: $annual_cost,
                    license_type: $license_type,
                    cost_center: $cost_center,
                    in_use: $in_use,
                    user_count: $user_count,
                    deployment_type: $deployment_type,
                    environment: $environment,
                    platform: $platform,
                    programming_language: $programming_language,
                    database_type: $database_type,
                    compliance_requirements: $compliance_requirements,
                    security_classification: $security_classification,
                    data_sensitivity: $data_sensitivity,
                    installation_date: $installation_date,
                    last_updated: $last_updated,
                    end_of_life_date: $end_of_life_date,
                    renewal_date: $renewal_date,
                    uptime_sla: $uptime_sla,
                    criticality: $criticality,
                    tags: $tags,
                    notes: $notes
                })
                """

                session.run(query, {
                    'name': row['app_name'],
                    'description': row['app_description'],
                    'version': row['app_version'],
                    'annual_cost': float(row['annual_cost']) if pd.notna(row['annual_cost']) else None,
                    'license_type': row['license_type'],
                    'cost_center': row['cost_center'],
                    'in_use': bool(row['in_use']),
                    'user_count': int(row['user_count']) if pd.notna(row['user_count']) else None,
                    'deployment_type': row['deployment_type'],
                    'environment': row['environment'],
                    'platform': row['platform'],
                    'programming_language': row['programming_language'],
                    'database_type': row['database_type'],
                    'compliance_requirements': row['compliance_requirements'],
                    'security_classification': row['security_classification'],
                    'data_sensitivity': row['data_sensitivity'],
                    'installation_date': row['installation_date'],
                    'last_updated': row['last_updated'],
                    'end_of_life_date': row['end_of_life_date'],
                    'renewal_date': row['renewal_date'],
                    'uptime_sla': float(row['uptime_sla']) if pd.notna(row['uptime_sla']) else None,
                    'criticality': row['criticality'],
                    'tags': row['tags'],
                    'notes': row['notes']
                })

            logger.info(f"Created {len(df)} Application nodes")

    def create_category_nodes(self, df):
        """Create Category nodes"""
        categories = df[['category', 'subcategory']].drop_duplicates()

        with self.driver.session() as session:
            # Create main categories
            main_categories = df['category'].unique()
            for category in main_categories:
                query = "MERGE (c:Category {name: $name, type: 'main'})"
                session.run(query, {'name': category})

            # Create subcategories and relationships
            for _, row in categories.iterrows():
                if pd.notna(row['subcategory']):
                    # Create subcategory
                    query = "MERGE (sc:Category {name: $name, type: 'sub'})"
                    session.run(query, {'name': row['subcategory']})

                    # Create relationship between main category and subcategory
                    query = """
                    MATCH (c:Category {name: $main_category, type: 'main'})
                    MATCH (sc:Category {name: $subcategory, type: 'sub'})
                    MERGE (sc)-[:BELONGS_TO]->(c)
                    """
                    session.run(query, {
                        'main_category': row['category'],
                        'subcategory': row['subcategory']
                    })

            logger.info(f"Created Category nodes and relationships")

    def create_vendor_nodes(self, df):
        """Create Vendor nodes"""
        vendors = df[['vendor_name', 'vendor_contact_email']].drop_duplicates()

        with self.driver.session() as session:
            for _, row in vendors.iterrows():
                query = """
                MERGE (v:Vendor {
                    name: $name,
                    contact_email: $contact_email
                })
                """
                session.run(query, {
                    'name': row['vendor_name'],
                    'contact_email': row['vendor_contact_email']
                })

            logger.info(f"Created {len(vendors)} Vendor nodes")

    def create_department_nodes(self, df):
        """Create Department nodes"""
        departments = df['department'].unique()

        with self.driver.session() as session:
            for department in departments:
                query = "MERGE (d:Department {name: $name})"
                session.run(query, {'name': department})

            logger.info(f"Created {len(departments)} Department nodes")

    def create_person_nodes(self, df):
        """Create Person nodes for app owners, technical leads, and business owners"""
        people = set()

        # Collect all unique people
        for col in ['app_owner', 'technical_lead', 'business_owner']:
            people.update(df[col].dropna().unique())

        with self.driver.session() as session:
            for person in people:
                query = "MERGE (p:Person {name: $name})"
                session.run(query, {'name': person})

            logger.info(f"Created {len(people)} Person nodes")

    def create_relationships(self, df):
        """Create relationships between nodes"""
        with self.driver.session() as session:
            for _, row in df.iterrows():
                app_name = row['app_name']

                # Application BELONGS_TO Category
                if pd.notna(row['category']):
                    query = """
                    MATCH (a:Application {name: $app_name})
                    MATCH (c:Category {name: $category, type: 'main'})
                    MERGE (a)-[:BELONGS_TO]->(c)
                    """
                    session.run(query, {'app_name': app_name, 'category': row['category']})

                # Application BELONGS_TO Subcategory
                if pd.notna(row['subcategory']):
                    query = """
                    MATCH (a:Application {name: $app_name})
                    MATCH (sc:Category {name: $subcategory, type: 'sub'})
                    MERGE (a)-[:BELONGS_TO]->(sc)
                    """
                    session.run(query, {'app_name': app_name, 'subcategory': row['subcategory']})

                # Application SUPPLIED_BY Vendor
                if pd.notna(row['vendor_name']):
                    query = """
                    MATCH (a:Application {name: $app_name})
                    MATCH (v:Vendor {name: $vendor_name})
                    MERGE (a)-[:SUPPLIED_BY]->(v)
                    """
                    session.run(query, {'app_name': app_name, 'vendor_name': row['vendor_name']})

                # Application OWNED_BY Department
                if pd.notna(row['department']):
                    query = """
                    MATCH (a:Application {name: $app_name})
                    MATCH (d:Department {name: $department})
                    MERGE (a)-[:OWNED_BY]->(d)
                    """
                    session.run(query, {'app_name': app_name, 'department': row['department']})

                # Person relationships
                for role, relationship in [('app_owner', 'OWNS'), ('technical_lead', 'LEADS'), ('business_owner', 'MANAGES')]:
                    if pd.notna(row[role]):
                        query = f"""
                        MATCH (a:Application {{name: $app_name}})
                        MATCH (p:Person {{name: $person_name}})
                        MERGE (p)-[:{relationship}]->(a)
                        """
                        session.run(query, {'app_name': app_name, 'person_name': row[role]})

                # Dependencies relationships
                if pd.notna(row['depends_on_apps']) and row['depends_on_apps'].strip():
                    dependencies = [dep.strip() for dep in row['depends_on_apps'].split(',')]
                    for dep in dependencies:
                        if dep:  # Make sure dependency is not empty
                            query = """
                            MATCH (a:Application {name: $app_name})
                            MERGE (dep:ExternalApp {name: $dep_name})
                            MERGE (a)-[:DEPENDS_ON]->(dep)
                            """
                            session.run(query, {'app_name': app_name, 'dep_name': dep})

                # Integration relationships
                if pd.notna(row['integrates_with_apps']) and row['integrates_with_apps'].strip():
                    integrations = [integ.strip() for integ in row['integrates_with_apps'].split(',')]
                    for integ in integrations:
                        if integ:  # Make sure integration is not empty
                            query = """
                            MATCH (a:Application {name: $app_name})
                            MERGE (integ:ExternalApp {name: $integ_name})
                            MERGE (a)-[:INTEGRATES_WITH]->(integ)
                            """
                            session.run(query, {'app_name': app_name, 'integ_name': integ})

            logger.info("Created all relationships")

    def migrate(self):
        """Main migration method"""
        logger.info("Starting migration from SQLite to Neo4j")

        # Load data
        df = self.load_data_from_sqlite()
        logger.info(f"Loaded {len(df)} records from SQLite")

        # Clear existing data
        self.clear_database()

        # Create constraints and indexes
        self.create_constraints_and_indexes()

        # Create nodes
        self.create_application_nodes(df)
        self.create_category_nodes(df)
        self.create_vendor_nodes(df)
        self.create_department_nodes(df)
        self.create_person_nodes(df)

        # Create relationships
        self.create_relationships(df)

        logger.info("Migration completed successfully")

def main():
    # Neo4j connection details
    # Note: For this demo, we'll use a local Neo4j instance
    # In practice, you would set up Neo4j Desktop or use Neo4j Aura
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "/home/ubuntu/relational_to_graph_project/data/applications.db")

    migrator = Neo4jMigrator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, SQLITE_DB_PATH)

    try:
        migrator.migrate()
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        print(f"Error: {e}")
        print("\nNote: This script requires a running Neo4j instance.")
        print("To run this migration:")
        print("1. Install Neo4j Desktop or use Neo4j Aura")
        print("2. Start a Neo4j database instance")
        print("3. Update the connection details in this script")
        print("4. Run the migration script")
    finally:
        migrator.close()

if __name__ == "__main__":
    main()
