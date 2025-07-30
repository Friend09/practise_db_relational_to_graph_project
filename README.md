# Relational to Graph Database Migration Project

## Overview

This project demonstrates how to convert a traditional relational database table into a knowledge graph using Neo4j, enabling powerful relationship-based analysis that would be difficult or impossible with standard SQL queries.

## Project Structure

```
relational_to_graph_project/
├── README.md                          # This file
├── sql/
│   └── applications.sql               # SQL schema for applications table
├── data/
│   ├── applications.csv               # Sample data (generated)
│   └── applications.db                # SQLite database (generated)
├── scripts/
│   ├── generate_data.py               # Generate sample application data
│   ├── create_db.py                   # Create SQLite database and load data
│   ├── explore_db.py                  # Explore relational database
│   ├── migrate_to_neo4j.py            # Migrate data to Neo4j
│   └── neo4j_queries.py               # Neo4j analysis examples
└── docs/
    ├── graph_model.md                 # Graph model documentation
    ├── cypher_queries.md              # Cypher query examples
    ├── relational_vs_graph_comparison.md  # Comparison analysis
    └── insights_and_learnings.md      # Key insights document
```

## What You'll Learn

1. **Database Design for Relationships**: How to design relational schemas with graph conversion in mind
2. **Data Migration Strategies**: Techniques for converting relational data to graph format
3. **Graph Modeling**: How to model entities and relationships in a graph database
4. **Cypher Query Language**: Powerful graph query patterns and techniques
5. **Relationship Analysis**: Discovering patterns and insights through graph traversal
6. **Performance Differences**: Understanding when graph databases outperform relational databases

## Prerequisites

- Python 3.7+
- Neo4j Desktop or Neo4j Aura account
- Basic understanding of databases and SQL
- Familiarity with Python programming

## Installation and Setup

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd relational_to_graph_project

# Or download and extract the project files
```

### 2. Install Python Dependencies

#### Option A: Quick Installation (Default Python)

```bash
pip install pandas faker neo4j
```

Note: `sqlite3` is included with Python by default, so no separate installation needed.

#### Option B: Virtual Environment (Recommended)

Creating a virtual environment keeps your project dependencies isolated:

```bash
# Create virtual environment
python -m venv graph_env

# Activate virtual environment
# On macOS/Linux:
source graph_env/bin/activate
# On Windows:
graph_env\Scripts\activate

# Install dependencies
pip install pandas faker neo4j

# Verify installation
pip list
```

#### Verify Installation

Test that all packages are properly installed:

```bash
python -c "import pandas, faker, neo4j, sqlite3; print('✅ All packages installed successfully!')"
```

### 3. Set Up Environment Configuration

Create your environment configuration file:

```bash
# Copy the example environment file
cp .env.example .env
```

The `.env` file will contain your Neo4j connection details and will be configured in the next step when you set up Neo4j.

### 4. Set Up Neo4j

#### Option A: Neo4j Desktop (Recommended for Learning)

##### Step 1: Download and Install

1. Visit [Neo4j Desktop](https://neo4j.com/download/) and download for your OS
2. Install Neo4j Desktop following the installation wizard
3. Launch Neo4j Desktop and create an account (or sign in)

##### Step 2: Create Your First Project

1. Click "New Project" in Neo4j Desktop
2. Name it "Application Portfolio Analysis" or similar
3. Click "Create"

##### Step 3: Add a Local Database

1. In your project, click "Add Database" → "Create a Local Database"
2. Configure the database:
   - **Name**: `applications-graph`
   - **Password**: `password` (or choose your own)
   - **Version**: Use latest stable version (e.g., 5.x)
3. Click "Create"

##### Step 4: Start and Verify Database

1. Click the "Start" button next to your database
2. Wait for status to show "Active" (may take 1-2 minutes)
3. Click "Open" to launch Neo4j Browser
4. In the browser, run: `RETURN "Hello Neo4j!" as greeting`
5. If successful, you'll see the greeting message

##### Step 5: Note Connection Details

Your connection details will be:

- **URI**: `bolt://localhost:7687`
- **Username**: `neo4j`
- **Password**: What you set in Step 3

#### Option B: Neo4j Aura (Cloud-based)

##### Step 1: Create Account

1. Visit [Neo4j Aura](https://neo4j.com/cloud/aura/)
2. Sign up for a free account
3. Verify your email address

##### Step 2: Create Database Instance

1. Click "Create Database"
2. Select "AuraDB Free" (no credit card required)
3. Configure:
   - **Name**: `applications-graph`
   - **Region**: Choose closest to your location
4. Click "Create Database"

##### Step 3: Save Credentials

1. **IMPORTANT**: Download and save the credentials file
2. Note the connection details:
   - **URI**: `neo4j+s://xxxxx.databases.neo4j.io`
   - **Username**: Usually `neo4j`
   - **Password**: Auto-generated (save this!)

##### Step 4: Test Connection

1. Click "Open" to access Neo4j Browser
2. Sign in with your credentials
3. Run: `RETURN "Hello Neo4j Aura!" as greeting`

##### Step 5: Update Script Configuration

##### Step 5: Configure Environment Variables

Create a `.env` file in the project root with your connection details:

```bash
# Copy the example file
cp .env.example .env
```

Then edit the `.env` file with your actual connection details:

```properties
# For Neo4j Desktop (local instance)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-actual-password

# SQLite database path (update with your actual path)
SQLITE_DB_PATH=/your/project/path/data/applications.db
```

For Aura, update the `.env` file with your cloud instance details:

```properties
# For Neo4j Aura (cloud instance)
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-generated-password
```

#### Troubleshooting Neo4j Setup

##### Common Neo4j Desktop Issues

###### Issue: Database won't start

- Check if port 7687 is already in use: `lsof -i :7687` (macOS/Linux) or `netstat -an | find "7687"` (Windows)
- Try restarting Neo4j Desktop
- Check system requirements (4GB RAM minimum)

###### Issue: Can't connect to database

- Verify the database status shows "Active"
- Check connection details match your setup
- Try connecting via Neo4j Browser first

###### Issue: Password authentication failed

- **Password too short**: Neo4j requires passwords to be at least 8 characters long
- **Recommended passwords**: Use `password123`, `neo4j123`, or similar (8+ characters)
- Reset password in Neo4j Desktop (Database settings → Reset password)
- Make sure you're using the correct password in your `.env` file
- Ensure the `.env` file exists in the project root directory

##### Common Neo4j Aura Issues

###### Issue: Connection timeout

- Check your internet connection
- Verify the URI starts with `neo4j+s://` (not `bolt://`)
- Ensure you're using the correct region

###### Issue: Invalid credentials

- Double-check the auto-generated password from the credentials file
- Make sure you're using the correct database URI
- Try resetting the password in Aura console

##### Quick Connection Test

Test your Neo4j connection with the included test script:

```bash
python tests/test_neo4j.py
```

This will use your `.env` file configuration automatically.

```python
from neo4j import GraphDatabase

# Update these with your actual connection details
URI = "bolt://localhost:7687"  # or your Aura URI
USER = "neo4j"
PASSWORD = "password"  # your actual password

try:
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful!' as message")
        print(result.single()["message"])
    driver.close()
    print("✅ Neo4j connection working!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

#### Complete Setup Validation

Run the provided setup validation script to test everything at once:

```bash
python test_setup.py
```

This script will verify:

- All Python packages are installed
- Project structure is correct
- SQLite functionality works
- Neo4j connection is successful

### Neo4j First-Time Setup Checklist

If you're setting up Neo4j for the first time, follow this checklist:

#### For Neo4j Desktop

1. **Download**: Get Neo4j Desktop from [neo4j.com/download](https://neo4j.com/download/)
2. **Install**: Run the installer for your operating system
3. **Launch**: Open Neo4j Desktop and sign in/create account
4. **Create Project**: Click "New Project" → Name it "Learning Graph DBs"
5. **Add Database**: Click "Add Database" → "Create a Local Database"
   - **Name**: `applications-graph` (or similar like "Learn App Portfolio Analysis")
   - **Password**: Choose a password **at least 8 characters long** (e.g., `password123` or `neo4j123`)
   - **Version**: Use latest stable version (2025.06.2 or similar)
   - **Important**: Remember your password - you'll need it for the scripts!
6. **Start Database**: Click the "Start" button and wait for "Active" status
7. **Update Script Passwords**: If you used a password different from `password`, update it in:
   - `dev/migrate_to_neo4j.py` (line 298): `NEO4J_PASSWORD = "your-actual-password"`
   - `scripts/neo4j_queries.py`: Update the password there too
8. **Test**: Click "Open" to launch Neo4j Browser, run: `RETURN "Hello!" as greeting`

**💡 What to expect during database creation:**

- Neo4j Desktop will download the database version (may take 1-2 minutes)
- You'll see progress indicators during the download/setup process
- Once complete, you'll see a "Start" button next to your database
- The database status will show "Stopped" initially - this is normal!

#### For Neo4j Aura (Cloud)

1. **Sign Up**: Visit [neo4j.com/cloud/aura](https://neo4j.com/cloud/aura/)
2. **Create Instance**: Choose "AuraDB Free" → Name it `applications-graph`
3. **Save Credentials**: Download the credentials file (very important!)
4. **Update .env File**: Edit your `.env` file with the Aura connection details:

   ```properties
   NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your-generated-password
   ```

#### Verify Your Setup

Run the validation script after setup:

```bash
python test_setup.py
```

All 4 tests should now pass! ✅

### 🎯 **Right After Creating Your Neo4j Instance**

If you just created a Neo4j instance (like "Learn App Portfolio Analysis"), here's what to do next:

1. **Click "Create"** to finish creating your database instance
2. **Wait for installation** - Neo4j Desktop will download and set up the database
3. **Start the database** - Click the "Start" button when it appears
4. **Update your .env file** - Update the `.env` file with your actual password:

   ```properties
   # Edit .env file and update with your actual password
   NEO4J_PASSWORD=your-actual-password
   ```

5. **Test the connection**:

   ```bash
   python test_setup.py
   ```

   You should now see all 4 tests pass!

### 🚀 **Once All Tests Pass**

You're ready to run the full project:

```bash
cd scripts
python generate_data.py      # Creates sample data
python create_db.py          # Sets up SQLite database
python migrate_to_neo4j.py   # Migrates data to Neo4j
python neo4j_queries.py      # Runs graph analysis
```

## Quick Start Guide

**Before running the project steps, make sure Neo4j is set up and running!**

### Step 0: Verify Setup

First, validate your setup by running:

```bash
python test_setup.py
```

**Expected Results:**

- ✅ Python Packages: PASS
- ✅ Project Structure: PASS
- ✅ SQLite Functionality: PASS
- ❌ Neo4j Connection: FAIL (if Neo4j not started yet)

If Neo4j connection fails, complete the Neo4j setup in Section 3 above, then run the test again.

### Step 1: Generate Sample Data

```bash
cd scripts
python generate_data.py
```

This creates `data/applications.csv` with 100 sample application records.

### Step 2: Create SQLite Database

```bash
python create_db.py
```

This creates `data/applications.db` and loads the sample data.

### Step 3: Explore Relational Data

```bash
python explore_db.py
```

This provides insights into the relational data structure and relationships.

### Step 4: Migrate to Neo4j

```bash
# Make sure Neo4j is running first
python migrate_to_neo4j.py
```

This converts the relational data into a graph database.

### Step 5: Analyze Graph Data

```bash
python neo4j_queries.py
```

This runs comprehensive analysis queries on the graph database.

## Key Features

### Relational Database Schema

The applications table includes fields designed to demonstrate relationships:

- **Basic Info**: name, description, version, cost
- **Categorization**: category, subcategory for grouping
- **Vendor Relationships**: vendor information for supplier analysis
- **Ownership**: department, owners, leads for organizational structure
- **Dependencies**: comma-separated lists of dependent applications
- **Integrations**: applications that integrate with this one
- **Compliance**: requirements and security classifications

### Graph Database Model

The graph model creates the following node types:

- **Application**: Core application entities
- **Category**: Application categories and subcategories
- **Vendor**: Software suppliers
- **Department**: Organizational departments
- **Person**: Application owners and leads
- **ExternalApp**: External applications for dependencies/integrations

### Relationship Types

- **BELONGS_TO**: Application → Category
- **SUPPLIED_BY**: Application → Vendor
- **OWNED_BY**: Application → Department
- **OWNS/LEADS/MANAGES**: Person → Application
- **DEPENDS_ON**: Application → ExternalApp
- **INTEGRATES_WITH**: Application → ExternalApp

## Example Analyses

### 1. Vendor Consolidation Analysis

Find vendors supplying multiple applications to identify consolidation opportunities:

```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
RETURN v.name, count(a) as app_count, sum(a.annual_cost) as total_cost
ORDER BY app_count DESC
```

### 2. Dependency Risk Assessment

Identify shared dependencies that could be single points of failure:

```cypher
MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(other:Application)
WHERE a <> other
RETURN e.name as shared_dependency, count(DISTINCT a) as risk_level
ORDER BY risk_level DESC
```

### 3. Department Portfolio Analysis

Analyze application portfolios by department:

```cypher
MATCH (d:Department)<-[:OWNED_BY]-(a:Application)-[:BELONGS_TO]->(c:Category)
RETURN d.name, c.name, count(a) as app_count
ORDER BY d.name, app_count DESC
```

## Learning Outcomes

After completing this project, you will understand:

1. **When to Use Graph Databases**: Scenarios where graph databases provide significant advantages over relational databases

2. **Graph Modeling Principles**: How to design effective graph schemas that capture meaningful relationships

3. **Migration Strategies**: Techniques for converting existing relational data to graph format

4. **Cypher Query Patterns**: Common graph query patterns for analysis and discovery

5. **Relationship Analysis**: How to uncover hidden patterns and insights through graph traversal

6. **Performance Considerations**: Understanding the performance characteristics of graph vs. relational queries

## Advanced Topics

### Custom Analysis Scripts

The project includes templates for creating your own analysis scripts. You can extend the `neo4j_queries.py` script to add custom analyses specific to your use case.

### Data Visualization

Consider integrating with visualization tools like:

- Neo4j Bloom for interactive graph exploration
- Gephi for network analysis and visualization
- Python libraries like NetworkX for custom visualizations

### Real-World Applications

This pattern can be applied to various domains:

- **IT Asset Management**: Track software, hardware, and their relationships
- **Supply Chain Analysis**: Model suppliers, products, and dependencies
- **Social Network Analysis**: Understand connections between people and organizations
- **Fraud Detection**: Identify suspicious patterns through relationship analysis

## Troubleshooting

### Common Issues

1. **Neo4j Connection Errors**

   - Ensure Neo4j is running
   - Check connection credentials
   - Verify firewall settings

2. **Data Migration Issues**

   - Check data format and encoding
   - Verify CSV file structure
   - Ensure sufficient memory for large datasets

3. **Query Performance**
   - Create appropriate indexes
   - Use EXPLAIN to analyze query plans
   - Consider data model optimizations

### Getting Help

- Check the `docs/` folder for detailed documentation
- Review the comparison document for SQL vs. Cypher examples
- Examine the sample queries for common patterns

## Contributing

This project is designed for learning purposes. Feel free to:

- Add new analysis queries
- Extend the data model
- Create additional visualization examples
- Improve documentation

## License

This project is provided for educational purposes. Feel free to use and modify for your learning and development needs.

## Next Steps

1. **Experiment with Real Data**: Try migrating your own relational data
2. **Explore Advanced Cypher**: Learn about graph algorithms and advanced patterns
3. **Build Applications**: Create web applications that leverage graph data
4. **Study Graph Algorithms**: Explore centrality, community detection, and pathfinding algorithms

## Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Cypher Query Language Guide](https://neo4j.com/developer/cypher/)
- [Graph Database Concepts](https://neo4j.com/developer/graph-database/)
- [Graph Data Science Library](https://neo4j.com/docs/graph-data-science/)

This project provides a foundation for understanding the power of graph databases in revealing relationships and patterns that traditional relational databases struggle to uncover efficiently.
