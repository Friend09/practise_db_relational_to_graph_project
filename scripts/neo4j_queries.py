from neo4j import GraphDatabase
import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Neo4jAnalyzer:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close(self):
        self.driver.close()

    def run_query(self, query, description=""):
        """Run a Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(query)
            records = [record.data() for record in result]
            if description:
                print(f"\n=== {description} ===")
                print(f"Query: {query}")
                print(f"Results ({len(records)} records):")
                for i, record in enumerate(records[:10]):  # Show first 10 results
                    print(f"  {i+1}. {record}")
                if len(records) > 10:
                    print(f"  ... and {len(records) - 10} more records")
                print()
            return records

    def basic_graph_statistics(self):
        """Get basic statistics about the graph"""
        print("=== BASIC GRAPH STATISTICS ===")

        # Count nodes by type
        queries = [
            ("MATCH (a:Application) RETURN count(a) as count", "Total Applications"),
            ("MATCH (c:Category) RETURN count(c) as count", "Total Categories"),
            ("MATCH (v:Vendor) RETURN count(v) as count", "Total Vendors"),
            ("MATCH (d:Department) RETURN count(d) as count", "Total Departments"),
            ("MATCH (p:Person) RETURN count(p) as count", "Total People"),
            ("MATCH (e:ExternalApp) RETURN count(e) as count", "Total External Apps"),
        ]

        for query, description in queries:
            result = self.run_query(query)
            if result:
                print(f"{description}: {result[0]['count']}")

        # Count relationships
        rel_query = "MATCH ()-[r]->() RETURN type(r) as relationship_type, count(r) as count ORDER BY count DESC"
        relationships = self.run_query(rel_query, "Relationship Counts")

        print()

    def vendor_analysis(self):
        """Analyze vendor relationships"""
        queries = [
            ("""
            MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
            RETURN v.name as vendor, count(a) as app_count,
                   sum(a.annual_cost) as total_cost
            ORDER BY app_count DESC
            LIMIT 10
            """, "Top 10 Vendors by Application Count"),

            ("""
            MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
            WHERE a.annual_cost IS NOT NULL
            RETURN v.name as vendor, sum(a.annual_cost) as total_cost
            ORDER BY total_cost DESC
            LIMIT 10
            """, "Top 10 Vendors by Total Cost"),

            ("""
            MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
            WHERE a.criticality = 'critical'
            RETURN v.name as vendor, count(a) as critical_apps
            ORDER BY critical_apps DESC
            """, "Vendors with Critical Applications")
        ]

        for query, description in queries:
            self.run_query(query, description)

    def dependency_analysis(self):
        """Analyze application dependencies"""
        queries = [
            ("""
            MATCH (e:ExternalApp)<-[:DEPENDS_ON]-(a:Application)
            RETURN e.name as external_app, count(a) as dependent_apps
            ORDER BY dependent_apps DESC
            LIMIT 10
            """, "Most Common Dependencies"),

            ("""
            MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)
            RETURN a.name as app, count(e) as dependency_count
            ORDER BY dependency_count DESC
            LIMIT 10
            """, "Applications with Most Dependencies"),

            ("""
            MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(other:Application)
            WHERE a <> other
            RETURN e.name as shared_dependency,
                   collect(DISTINCT a.name) as dependent_apps,
                   count(DISTINCT a) as app_count
            ORDER BY app_count DESC
            LIMIT 10
            """, "Shared Dependencies (Potential Single Points of Failure)")
        ]

        for query, description in queries:
            self.run_query(query, description)

    def integration_analysis(self):
        """Analyze application integrations"""
        queries = [
            ("""
            MATCH (e:ExternalApp)<-[:INTEGRATES_WITH]-(a:Application)
            RETURN e.name as external_app, count(a) as integrating_apps
            ORDER BY integrating_apps DESC
            LIMIT 10
            """, "Most Common Integration Points"),

            ("""
            MATCH (a:Application)-[:INTEGRATES_WITH]->(e:ExternalApp)
            RETURN a.name as app, count(e) as integration_count
            ORDER BY integration_count DESC
            LIMIT 10
            """, "Applications with Most Integrations"),

            ("""
            MATCH (a1:Application)-[:INTEGRATES_WITH]->(e:ExternalApp)<-[:INTEGRATES_WITH]-(a2:Application)
            WHERE a1 <> a2
            RETURN e.name as integration_hub,
                   count(DISTINCT a1) + count(DISTINCT a2) as connected_apps
            ORDER BY connected_apps DESC
            LIMIT 10
            """, "Integration Hubs")
        ]

        for query, description in queries:
            self.run_query(query, description)

    def department_analysis(self):
        """Analyze department application portfolios"""
        queries = [
            ("""
            MATCH (d:Department)<-[:OWNED_BY]-(a:Application)
            RETURN d.name as department, count(a) as app_count,
                   sum(a.annual_cost) as total_cost
            ORDER BY app_count DESC
            LIMIT 10
            """, "Departments by Application Count"),

            ("""
            MATCH (d:Department)<-[:OWNED_BY]-(a:Application)
            WHERE a.criticality = 'critical'
            RETURN d.name as department, count(a) as critical_apps
            ORDER BY critical_apps DESC
            """, "Departments with Critical Applications"),

            ("""
            MATCH (d:Department)<-[:OWNED_BY]-(a:Application)-[:BELONGS_TO]->(c:Category)
            WHERE c.type = 'main'
            RETURN d.name as department, c.name as category, count(a) as app_count
            ORDER BY department, app_count DESC
            """, "Department Application Categories")
        ]

        for query, description in queries:
            self.run_query(query, description)

    def category_analysis(self):
        """Analyze application categories"""
        queries = [
            ("""
            MATCH (c:Category)<-[:BELONGS_TO]-(a:Application)
            WHERE c.type = 'main'
            RETURN c.name as category, count(a) as app_count,
                   avg(a.annual_cost) as avg_cost
            ORDER BY app_count DESC
            """, "Application Categories"),

            ("""
            MATCH (c:Category)<-[:BELONGS_TO]-(a:Application)-[:SUPPLIED_BY]->(v:Vendor)
            WHERE c.type = 'main'
            RETURN c.name as category, count(DISTINCT v) as vendor_count
            ORDER BY vendor_count DESC
            """, "Vendor Diversity by Category"),

            ("""
            MATCH (c:Category)<-[:BELONGS_TO]-(a:Application)
            WHERE c.type = 'main' AND a.criticality = 'critical'
            RETURN c.name as category, count(a) as critical_apps
            ORDER BY critical_apps DESC
            """, "Critical Applications by Category")
        ]

        for query, description in queries:
            self.run_query(query, description)

    def person_analysis(self):
        """Analyze people and their application responsibilities"""
        queries = [
            ("""
            MATCH (p:Person)-[r]->(a:Application)
            RETURN p.name as person, type(r) as role, count(a) as app_count
            ORDER BY app_count DESC
            LIMIT 15
            """, "People with Most Application Responsibilities"),

            ("""
            MATCH (p:Person)-[:OWNS]->(a:Application)
            WHERE a.criticality = 'critical'
            RETURN p.name as person, count(a) as critical_apps
            ORDER BY critical_apps DESC
            """, "People Owning Critical Applications"),

            ("""
            MATCH (p:Person)-[:OWNS]->(a:Application)
            RETURN p.name as person, sum(a.annual_cost) as total_cost_responsibility
            ORDER BY total_cost_responsibility DESC
            LIMIT 10
            """, "People by Cost Responsibility")
        ]

        for query, description in queries:
            self.run_query(query, description)

    def advanced_pattern_analysis(self):
        """Advanced pattern analysis"""
        queries = [
            ("""
            MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)<-[:INTEGRATES_WITH]-(other:Application)
            WHERE a <> other
            RETURN a.name as app1, other.name as app2, e.name as common_external_app
            LIMIT 10
            """, "Applications Connected Through External Apps"),

            ("""
            MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)-[:OWNED_BY]->(d:Department)
            RETURN v.name as vendor, d.name as department, count(a) as app_count
            ORDER BY app_count DESC
            LIMIT 15
            """, "Vendor-Department Relationships"),

            ("""
            MATCH (a:Application)
            WHERE a.end_of_life_date IS NOT NULL
            MATCH (a)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(other:Application)
            WHERE other.end_of_life_date IS NULL
            RETURN a.name as eol_app, collect(DISTINCT other.name) as affected_apps
            """, "End-of-Life Applications and Their Impact"),

            ("""
            MATCH (a:Application)
            WHERE a.license_type = 'subscription' AND a.annual_cost > 50000
            MATCH (a)-[:SUPPLIED_BY]->(v:Vendor)
            RETURN v.name as vendor, sum(a.annual_cost) as total_subscription_cost,
                   count(a) as expensive_apps
            ORDER BY total_subscription_cost DESC
            """, "High-Cost Subscription Vendors")
        ]

        for query, description in queries:
            self.run_query(query, description)

    def compliance_analysis(self):
        """Analyze compliance requirements"""
        queries = [
            ("""
            MATCH (a:Application)
            WHERE a.compliance_requirements IS NOT NULL AND a.compliance_requirements <> ''
            UNWIND split(a.compliance_requirements, ',') as compliance
            RETURN trim(compliance) as requirement, count(a) as app_count
            ORDER BY app_count DESC
            """, "Compliance Requirements Distribution"),

            ("""
            MATCH (a:Application)-[:SUPPLIED_BY]->(v:Vendor)
            WHERE a.compliance_requirements CONTAINS 'GDPR'
            RETURN v.name as vendor, count(a) as gdpr_apps
            ORDER BY gdpr_apps DESC
            """, "Vendors with GDPR-Compliant Applications"),

            ("""
            MATCH (a:Application)-[:OWNED_BY]->(d:Department)
            WHERE a.data_sensitivity = 'critical'
            RETURN d.name as department, count(a) as critical_data_apps
            ORDER BY critical_data_apps DESC
            """, "Departments with Critical Data Applications")
        ]

        for query, description in queries:
            self.run_query(query, description)

    def run_all_analyses(self):
        """Run all analysis queries"""
        print("RUNNING COMPREHENSIVE GRAPH ANALYSIS")
        print("=" * 50)

        self.basic_graph_statistics()
        self.vendor_analysis()
        self.dependency_analysis()
        self.integration_analysis()
        self.department_analysis()
        self.category_analysis()
        self.person_analysis()
        self.advanced_pattern_analysis()
        self.compliance_analysis()

def main():
    # Load Neo4j connection details from environment variables
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

    print(f"Connecting to Neo4j at: {NEO4J_URI}")

    analyzer = Neo4jAnalyzer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        analyzer.run_all_analyses()
    except Exception as e:
        print(f"Error connecting to Neo4j: {e}")
        print("\nNote: This script requires a running Neo4j instance with migrated data.")
        print("To run this analysis:")
        print("1. Ensure Neo4j is running")
        print("2. Run the migration script first")
        print("3. Update connection details in .env file if needed")
        print("4. Run this analysis script")
    finally:
        analyzer.close()

if __name__ == "__main__":
    main()
