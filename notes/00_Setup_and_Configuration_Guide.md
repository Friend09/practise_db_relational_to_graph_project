# Complete Setup and Configuration Guide

## Overview

This guide provides comprehensive instructions for setting up the relational to graph database migration project, including environment configuration, Neo4j setup, and troubleshooting.

## Prerequisites

### Required Software

- **Python 3.7+**: Download from [python.org](https://www.python.org/downloads/)
- **Neo4j Database**: Choose Neo4j Desktop (recommended) or Neo4j Aura (cloud)

### Required Knowledge

- Basic Python programming and SQL understanding
- Database concepts (tables, relationships, queries)
- No prior graph database experience required

## Step 1: Environment Setup

### Create Project Directory

```bash
mkdir relational_to_graph_project
cd relational_to_graph_project
```

### Python Virtual Environment (Recommended)

```bash
# Create and activate virtual environment
python -m venv graph_env

# Activate (macOS/Linux)
source graph_env/bin/activate

# Activate (Windows)
graph_env\Scripts\activate
```

### Install Dependencies

```bash
pip install pandas faker neo4j python-dotenv
```

## Step 2: Neo4j Setup

### Option A: Neo4j Desktop (Recommended)

1. **Download and Install**

   - Visit [neo4j.com/download](https://neo4j.com/download/)
   - Install Neo4j Desktop for your OS

2. **Create Database**

   - Create a new database called "learn-graph-db"
   - Start the database

3. **Configure Import Directory**

   For CSV import functionality, you'll need to copy your data files to Neo4j's import directory:

   - **macOS**: `~/Library/Application Support/Neo4j Desktop/Application/relate-data/dbmss/[dbms-id]/import/`
   - **Windows**: `%UserProfile%\AppData\Local\Neo4j\Relate\Data\dbmss\[dbms-id]\import\`
   - **Linux**: `~/.config/Neo4j Desktop/Application/relate-data/dbmss/[dbms-id]/import/`

   Alternatively, you can use absolute file paths with the `file:///` protocol.

4. **Verify Connection**
   - Click "Open" to access Neo4j Browser
   - Should see Neo4j Browser interface at <http://localhost:7474>
   - Select the "learn-graph-db" database from the dropdown

### Manual CSV Import (Alternative Method)

If you prefer to manually import the CSV data using Cypher queries instead of the automated script, follow these steps:

1. **Copy CSV to Import Directory**

   Copy your `applications.csv` file to the Neo4j import directory identified above.

2. **Create Database Constraints**

   In Neo4j Browser, execute these queries to create constraints for data integrity:

   ```cypher
   CREATE CONSTRAINT app_id_unique FOR (a:Application) REQUIRE a.app_id IS UNIQUE;
   CREATE CONSTRAINT vendor_name_unique FOR (v:Vendor) REQUIRE v.name IS UNIQUE;
   CREATE CONSTRAINT person_name_unique FOR (p:Person) REQUIRE p.name IS UNIQUE;
   CREATE CONSTRAINT department_name_unique FOR (d:Department) REQUIRE d.name IS UNIQUE;
   CREATE CONSTRAINT category_name_unique FOR (c:Category) REQUIRE c.name IS UNIQUE;
   CREATE CONSTRAINT subcategory_name_unique FOR (s:Subcategory) REQUIRE s.name IS UNIQUE;
   ```

3. **Import Applications**

```cypher
LOAD CSV WITH HEADERS FROM 'file:////Users/../data/applications.csv' AS row
WITH row WHERE row.app_id IS NOT NULL
CREATE (a:Application {
    app_id: toInteger(row.app_id),
    name: row.app_name,
    description: row.app_description,
    version: row.app_version,
    annual_cost: toFloat(row.annual_cost),
    license_type: row.license_type,
    cost_center: row.cost_center,
    in_use: toBoolean(row.in_use),
    user_count: toFloat(row.user_count),
    deployment_type: row.deployment_type,
    environment: row.environment,
    platform: row.platform,
    programming_language: row.programming_language,
    database_type: row.database_type,
    compliance_requirements: row.compliance_requirements,
    security_classification: row.security_classification,
    data_sensitivity: row.data_sensitivity,
    installation_date: date(row.installation_date),
    last_updated: date(row.last_updated),
    end_of_life_date: CASE WHEN row.end_of_life_date IS NOT NULL THEN date(row.end_of_life_date) ELSE null END,
    renewal_date: date(row.renewal_date),
    uptime_sla: toFloat(row.uptime_sla),
    criticality: row.criticality,
    tags: split(row.tags, ','),
    notes: row.notes,
    created_at: datetime(row.created_at),
    updated_at: datetime(row.updated_at)
});
   ```

4. **Import Vendors and Create Relationships**

   ```cypher
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.vendor_name IS NOT NULL
   MERGE (v:Vendor {name: row.vendor_name})
   ON CREATE SET v.contact_email = row.vendor_contact_email
   WITH v, row
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   MERGE (a)-[:PROVIDED_BY]->(v);
   ```

5. **Import People and Create Relationships**

   ```cypher
   // App Owners
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.app_owner IS NOT NULL
   MERGE (p:Person {name: row.app_owner})
   WITH p, row
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   MERGE (a)-[:OWNED_BY]->(p);

   // Technical Leads
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.technical_lead IS NOT NULL
   MERGE (p:Person {name: row.technical_lead})
   WITH p, row
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   MERGE (a)-[:TECH_LEAD]->(p);

   // Business Owners
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.business_owner IS NOT NULL
   MERGE (p:Person {name: row.business_owner})
   WITH p, row
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   MERGE (a)-[:BUSINESS_OWNER]->(p);
   ```

6. **Import Departments and Categories**

   ```cypher
   // Departments
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.department IS NOT NULL
   MERGE (d:Department {name: row.department})
   WITH d, row
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   MERGE (a)-[:USED_BY]->(d);

   // Categories
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.category IS NOT NULL
   MERGE (c:Category {name: row.category})
   WITH c, row
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   MERGE (a)-[:BELONGS_TO]->(c);

   // Subcategories
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.subcategory IS NOT NULL
   MERGE (s:Subcategory {name: row.subcategory})
   WITH s, row
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   MERGE (a)-[:SUBCATEGORY_OF]->(s);
   ```

7. **Create Application Dependencies and Integrations**

   ```cypher
   // Dependencies
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.depends_on_apps IS NOT NULL
   WITH row, split(row.depends_on_apps, ',') AS deps
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   UNWIND deps AS dep
   WITH a, trim(dep) AS dependency_name
   MATCH (dep_app:Application)
   WHERE dep_app.name CONTAINS dependency_name
   MERGE (a)-[:DEPENDS_ON]->(dep_app);

   // Integrations
   LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
   WHERE row.integrates_with_apps IS NOT NULL
   WITH row, split(row.integrates_with_apps, ',') AS integrations
   MATCH (a:Application {app_id: toInteger(row.app_id)})
   UNWIND integrations AS integration
   WITH a, trim(integration) AS integration_name
   MATCH (int_app:Application)
   WHERE int_app.name CONTAINS integration_name
   MERGE (a)-[:INTEGRATES_WITH]->(int_app);
   ```

### Option B: Neo4j Aura (Cloud)

1. **Create Account**

   - Visit [neo4j.com/cloud/aura](https://neo4j.com/cloud/aura/)
   - Sign up for free account

2. **Create Instance**
   - Create "AuraDB Free" instance
   - Name: "applications-graph"
   - Save connection URI, username, and password

## Step 3: Environment Configuration

### Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

### Configure `.env` File

Edit `.env` with your actual Neo4j connection details:

```properties
# For Neo4j Desktop (local)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-actual-password
NEO4J_DATABASE=learn-graph-db

# For Neo4j Aura (cloud)
# NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your-generated-password
# NEO4J_DATABASE=neo4j

# SQLite database path (use absolute path)
SQLITE_DB_PATH=/full/path/to/your/project/data/applications.db
```

## Step 4: Project Execution

### Generate Sample Data

```bash
cd scripts
python generate_data.py
```

Expected output: `Generated applications.csv with 100 records.`

### Create SQLite Database

```bash
python create_db.py
```

Expected output: `Data loaded successfully into 'applications' table.`

### Explore Relational Data

```bash
python explore_db.py
```

Shows statistics and analysis of the relational data.

### Migrate to Neo4j

```bash
python migrate_to_neo4j.py
```

Expected output: `Migration completed successfully`

### Analyze Graph Data

```bash
python neo4j_queries.py
```

Runs comprehensive graph analysis queries.

## Step 5: Verification

### Test Python Environment

```bash
python -c "import pandas, faker, neo4j; print('All packages installed successfully')"
```

### Test Neo4j Connection

```bash
python -c "
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')
database = os.getenv('NEO4J_DATABASE', 'learn-graph-db')

driver = GraphDatabase.driver(uri, auth=(user, password))
with driver.session(database=database) as session:
    result = session.run('RETURN 1 as test')
    print('Neo4j connection successful:', result.single()['test'])
    print('Connected to database:', database)
driver.close()
"
```

### Verify Data Migration

In Neo4j Browser, run:

```cypher
MATCH (n) RETURN labels(n) as node_type, count(n) as count
```

You should see results similar to:

```text
node_type          count
["Application"]      100
["Vendor"]           15-20
["Person"]           30-40
["Department"]       8-10
["Category"]         6-8
["Subcategory"]      10-15
```

Check relationships were created:

```cypher
MATCH ()-[r]->() RETURN type(r) AS RelationshipType, count(r) AS Count;
```

Verify sample data structure:

```cypher
MATCH (a:Application)-[r]->(n)
RETURN a.name, type(r), labels(n),
       CASE WHEN 'Person' IN labels(n) THEN n.name
            WHEN 'Vendor' IN labels(n) THEN n.name
            WHEN 'Department' IN labels(n) THEN n.name
            WHEN 'Category' IN labels(n) THEN n.name
            ELSE toString(n) END AS target
LIMIT 20;
```

## Troubleshooting

### Python Package Issues

**Problem**: `ModuleNotFoundError`
**Solution**:

```bash
# Ensure virtual environment is activated
source graph_env/bin/activate  # macOS/Linux
# or
graph_env\Scripts\activate     # Windows

# Reinstall packages
pip install pandas faker neo4j python-dotenv
```

### Neo4j Connection Issues

**Problem**: `ServiceUnavailable: Failed to establish connection`
**Solutions**:

1. Verify Neo4j is running (check Neo4j Desktop)
2. Check `.env` file has correct URI and credentials
3. For Desktop: ensure URI is `bolt://localhost:7687`
4. For Aura: ensure URI starts with `neo4j+s://`

**Problem**: `AuthError: The client is unauthorized`
**Solutions**:

1. Verify username and password in `.env` file
2. Reset password in Neo4j Desktop if needed
3. For Aura, use the generated credentials exactly as provided

### Environment File Issues

**Problem**: Environment variables not loading
**Solution**:

```bash
# Ensure .env file exists in project root
ls -la .env

# If missing, create from example
cp .env.example .env

# Verify content format (no spaces around =)
cat .env
```

### Data Migration Issues

**Problem**: SQLite database creation fails
**Solution**:

```bash
# Ensure data directory exists
mkdir -p data

# Check file permissions
chmod 755 data/

# Verify SQL schema file exists
ls -la sql/applications.sql
```

**Problem**: Neo4j migration fails
**Solution**:

1. Verify Neo4j is running and accessible
2. Check `.env` file configuration
3. Ensure SQLite database exists: `ls -la data/applications.db`
4. Run test connection script above

### Performance Issues

**Problem**: Migration takes too long
**Solutions**:

1. Reduce sample data size in `generate_data.py` (change `num_records = 100` to smaller number)
2. Increase Neo4j memory allocation in Neo4j Desktop settings
3. Check system resources (RAM, CPU usage)

**Problem**: Queries run slowly
**Solutions**:

1. Verify indexes are created (automatic in migration script)
2. Check Neo4j memory settings in configuration
3. Use `EXPLAIN` prefix in Cypher queries to analyze performance

## System Requirements

### Minimum Requirements

- **RAM**: 4GB (8GB recommended)
- **Storage**: 1GB free space
- **CPU**: Any modern processor
- **OS**: Windows 10+, macOS 10.14+, or Linux

### Recommended Requirements

- **RAM**: 8GB or more
- **Storage**: 5GB free space for data and logs
- **CPU**: Multi-core processor
- **Internet**: Required for Neo4j Aura setup

## File Structure Verification

Your project should have this structure after setup:

```
relational_to_graph_project/
├── .env                           # Your environment configuration
├── .env.example                   # Template file
├── README.md                      # Main project documentation
├── requirements.txt               # Python dependencies
├── data/
│   ├── applications.csv           # Generated sample data
│   └── applications.db            # SQLite database
├── scripts/
│   ├── generate_data.py           # Data generation
│   ├── create_db.py               # SQLite database creation
│   ├── explore_db.py              # Relational analysis
│   ├── migrate_to_neo4j.py        # Graph migration
│   └── neo4j_queries.py           # Graph analysis
├── sql/
│   └── applications.sql           # Database schema
└── notes/
    ├── 00_Setup_and_Configuration_Guide.md    # This file
    ├── 01_Query_Reference_and_Examples.md     # Cypher queries
    ├── 02_Project_Overview_and_Analysis.md    # Project insights
    └── 03_Technical_Documentation.md          # Graph model docs
```

## Next Steps

Once setup is complete:

1. Review generated data in `data/applications.csv`
2. Explore SQLite database structure with `explore_db.py`
3. Examine Neo4j graph in Neo4j Browser
4. Run analysis queries from the Query Reference guide
5. Experiment with custom queries
6. Read the Project Overview for deeper insights

## Getting Help

If you encounter issues:

1. Check this troubleshooting section first
2. Review error messages carefully - they often contain the solution
3. Verify all prerequisites are met
4. Ensure file paths are correct (use absolute paths in `.env`)
5. Test each step individually rather than running everything at once

This setup guide provides everything needed to get the project running successfully. Take time with each step and verify before proceeding.
