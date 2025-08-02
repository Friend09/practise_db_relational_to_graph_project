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
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password, sqlite_db_path, database="learn-graph-db"):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.sqlite_db_path = sqlite_db_path
        self.database = database

    def close(self):
        self.driver.close()

    def clear_database(self):
        """Clear all nodes and relationships in Neo4j database"""
        with self.driver.session(database=self.database) as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Cleared Neo4j database")

    def create_constraints_and_indexes(self):
        """Create constraints and indexes for better performance"""
        with self.driver.session(database=self.database) as session:
            # Create constraints for unique identifiers
            constraints = [
                "CREATE CONSTRAINT app_id_unique IF NOT EXISTS FOR (a:Application) REQUIRE a.app_id IS UNIQUE",
                "CREATE CONSTRAINT app_name_unique IF NOT EXISTS FOR (a:Application) REQUIRE a.name IS UNIQUE",
                "CREATE CONSTRAINT category_name_unique IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE",
                "CREATE CONSTRAINT subcategory_name_unique IF NOT EXISTS FOR (s:Subcategory) REQUIRE s.name IS UNIQUE",
                "CREATE CONSTRAINT vendor_name_unique IF NOT EXISTS FOR (v:Vendor) REQUIRE v.name IS UNIQUE",
                "CREATE CONSTRAINT departent_name_unique IF NOT EXISTS FOR (d:Department) REQUIRE d.name IS UNIQUE",
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
        """Create/Update Application nodes using MERGE"""
        with self.driver.session(database=self.database) as session:
            for _, row in df.iterrows():
                # Skip rows without app_id
                if pd.isna(row.get('app_id')):
                    continue

                query = """
                MERGE (a:Application {app_id: $app_id})
                SET a.name = $name,
                    a.description = $description,
                    a.version = $version,
                    a.annual_cost = $annual_cost,
                    a.license_type = $license_type,
                    a.cost_center = $cost_center,
                    a.in_use = $in_use,
                    a.user_count = $user_count,
                    a.deployment_type = $deployment_type,
                    a.environment = $environment,
                    a.platform = $platform,
                    a.programming_language = $programming_language,
                    a.database_type = $database_type,
                    a.compliance_requirements = $compliance_requirements,
                    a.security_classification = $security_classification,
                    a.data_sensitivity = $data_sensitivity,
                    a.installation_date = $installation_date,
                    a.last_updated = $last_updated,
                    a.end_of_life_date = $end_of_life_date,
                    a.renewal_date = $renewal_date,
                    a.uptime_sla = $uptime_sla,
                    a.criticality = $criticality,
                    a.tags = $tags,
                    a.notes = $notes,
                    a.created_at = $created_at,
                    a.updated_at = $updated_at
                """

                session.run(query, {
                    'app_id': int(row['app_id']),
                    'name': row['app_name'],
                    'description': row['app_description'],
                    'version': row['app_version'],
                    'annual_cost': float(row['annual_cost']) if pd.notna(row['annual_cost']) else None,
                    'license_type': row['license_type'],
                    'cost_center': row['cost_center'],
                    'in_use': bool(row['in_use']) if pd.notna(row['in_use']) else None,
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
                    'notes': row['notes'],
                    'created_at': row.get('created_at'),
                    'updated_at': row.get('updated_at')
                })

            logger.info(f"Created/Updated {len(df)} Application nodes")

    def create_category_nodes(self, df):
        """Create Category and Subcategory nodes"""
        categories = df[['category', 'subcategory']].drop_duplicates()

        with self.driver.session(database=self.database) as session:
            # Create main categories
            main_categories = df['category'].dropna().unique()
            for category in main_categories:
                query = "MERGE (c:Category {name: $name}) SET c.type = 'main'"
                session.run(query, {'name': category})

            # Create subcategories and relationships
            for _, row in categories.iterrows():
                if pd.notna(row['subcategory']):
                    # Create subcategory
                    query = "MERGE (sc:Subcategory {name: $name})"
                    session.run(query, {'name': row['subcategory']})

                    # Create relationship between main category and subcategory
                    if pd.notna(row['category']):
                        query = """
                        MATCH (c:Category {name: $main_category})
                        MATCH (sc:Subcategory {name: $subcategory})
                        MERGE (sc)-[:BELONGS_TO]->(c)
                        """
                        session.run(query, {
                            'main_category': row['category'],
                            'subcategory': row['subcategory']
                        })

            logger.info(f"Created Category and Subcategory nodes with relationships")

    def create_vendor_nodes(self, df):
        """Create Vendor nodes"""
        vendors = df[['vendor_name', 'vendor_contact_email']].dropna(subset=['vendor_name']).drop_duplicates()

        with self.driver.session(database=self.database) as session:
            for _, row in vendors.iterrows():
                query = """
                MERGE (v:Vendor {name: $name})
                SET v.contact_email = $contact_email
                """
                session.run(query, {
                    'name': row['vendor_name'],
                    'contact_email': row['vendor_contact_email'] if pd.notna(row['vendor_contact_email']) else None
                })

            logger.info(f"Created/Updated {len(vendors)} Vendor nodes")

    def create_department_nodes(self, df):
        """Create Department nodes"""
        departments = df['department'].dropna().unique()

        with self.driver.session(database=self.database) as session:
            for department in departments:
                query = "MERGE (d:Department {name: $name})"
                session.run(query, {'name': department})

            logger.info(f"Created/Updated {len(departments)} Department nodes")

    def create_person_nodes(self, df):
        """Create Person nodes for app owners, technical leads, and business owners"""
        people = set()

        # Collect all unique people
        for col in ['app_owner', 'technical_lead', 'business_owner']:
            if col in df.columns:
                people.update(df[col].dropna().unique())

        with self.driver.session(database=self.database) as session:
            for person in people:
                query = "MERGE (p:Person {name: $name})"
                session.run(query, {'name': person})

            logger.info(f"Created/Updated {len(people)} Person nodes")

    def create_relationships(self, df):
        """Create relationships between nodes"""
        with self.driver.session(database=self.database) as session:
            for _, row in df.iterrows():
                # Skip rows without app_id
                if pd.isna(row.get('app_id')):
                    continue

                app_id = int(row['app_id'])

                # Application BELONGS_TO Category
                if pd.notna(row['category']):
                    query = """
                    MATCH (a:Application {app_id: $app_id})
                    MATCH (c:Category {name: $category})
                    MERGE (a)-[:BELONGS_TO]->(c)
                    """
                    session.run(query, {'app_id': app_id, 'category': row['category']})

                # Application BELONGS_TO Subcategory
                if pd.notna(row['subcategory']):
                    query = """
                    MATCH (a:Application {app_id: $app_id})
                    MATCH (sc:Subcategory {name: $subcategory})
                    MERGE (a)-[:BELONGS_TO]->(sc)
                    """
                    session.run(query, {'app_id': app_id, 'subcategory': row['subcategory']})

                # Application SUPPLIED_BY Vendor
                if pd.notna(row['vendor_name']):
                    query = """
                    MATCH (a:Application {app_id: $app_id})
                    MATCH (v:Vendor {name: $vendor_name})
                    MERGE (a)-[:SUPPLIED_BY]->(v)
                    """
                    session.run(query, {'app_id': app_id, 'vendor_name': row['vendor_name']})

                # Application OWNED_BY Department
                if pd.notna(row['department']):
                    query = """
                    MATCH (a:Application {app_id: $app_id})
                    MATCH (d:Department {name: $department})
                    MERGE (a)-[:OWNED_BY]->(d)
                    """
                    session.run(query, {'app_id': app_id, 'department': row['department']})

                # Person relationships
                person_relationships = [
                    ('app_owner', 'OWNS'),
                    ('technical_lead', 'LEADS'),
                    ('business_owner', 'MANAGES')
                ]

                for role_col, relationship in person_relationships:
                    if role_col in df.columns and pd.notna(row[role_col]):
                        query = f"""
                        MATCH (a:Application {{app_id: $app_id}})
                        MATCH (p:Person {{name: $person_name}})
                        MERGE (p)-[:{relationship}]->(a)
                        """
                        session.run(query, {'app_id': app_id, 'person_name': row[role_col]})

                # Dependencies relationships
                if 'depends_on_apps' in df.columns and pd.notna(row['depends_on_apps']) and str(row['depends_on_apps']).strip():
                    dependencies = [dep.strip() for dep in str(row['depends_on_apps']).split(',')]
                    for dep in dependencies:
                        if dep:  # Make sure dependency is not empty
                            query = """
                            MATCH (a:Application {app_id: $app_id})
                            MERGE (dep:ExternalApp {name: $dep_name})
                            MERGE (a)-[:DEPENDS_ON]->(dep)
                            """
                            session.run(query, {'app_id': app_id, 'dep_name': dep})

                # Integration relationships
                if 'integrates_with_apps' in df.columns and pd.notna(row['integrates_with_apps']) and str(row['integrates_with_apps']).strip():
                    integrations = [integ.strip() for integ in str(row['integrates_with_apps']).split(',')]
                    for integ in integrations:
                        if integ:  # Make sure integration is not empty
                            query = """
                            MATCH (a:Application {app_id: $app_id})
                            MERGE (integ:ExternalApp {name: $integ_name})
                            MERGE (a)-[:INTEGRATES_WITH]->(integ)
                            """
                            session.run(query, {'app_id': app_id, 'integ_name': integ})

            logger.info("Created all relationships")

    def migrate(self, clear_first=True):
        """Main migration method"""
        logger.info("Starting migration from SQLite to Neo4j")

        # Load data
        df = self.load_data_from_sqlite()
        logger.info(f"Loaded {len(df)} records from SQLite")

        # Clear existing data if requested
        if clear_first:
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

    def upsert_migrate(self):
        """Migration method that updates existing data without clearing"""
        logger.info("Starting upsert migration from SQLite to Neo4j")
        self.migrate(clear_first=False)

def main():
    # Load Neo4j connection details from environment variables
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "learn-graph-db")

    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "../data/applications.db")

    print(f"Connecting to Neo4j at: {NEO4J_URI}")
    print(f"Using Neo4j database: {NEO4J_DATABASE}")
    print(f"Using SQLite database: {SQLITE_DB_PATH}")

    migrator = Neo4jMigrator(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, SQLITE_DB_PATH, NEO4J_DATABASE)

    try:
        # For first-time migration (clears database first)
        migrator.migrate()

        # For updating existing data without clearing (uncomment to use)
        # migrator.upsert_migrate()

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        print(f"Error: {e}")
        print("\nNote: This script requires a running Neo4j instance.")
        print("To run this migration:")
        print("1. Install Neo4j Desktop or use Neo4j Aura")
        print("2. Start a Neo4j database instance")
        print("3. Update the connection details in .env file")
        print("4. Run the migration script")
    finally:
        migrator.close()

if __name__ == "__main__":
    main()
