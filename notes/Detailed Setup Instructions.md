# Detailed Setup Instructions

## Prerequisites

Before starting this project, ensure you have the following installed:

### Required Software
- **Python 3.7 or higher**: Download from [python.org](https://www.python.org/downloads/)
- **Neo4j Database**: Choose one of the following options:
  - Neo4j Desktop (recommended for learning)
  - Neo4j Aura (cloud-based)
  - Neo4j Community Server (for advanced users)

### Python Knowledge
- Basic Python programming
- Understanding of data structures (lists, dictionaries)
- Familiarity with pandas library (helpful but not required)

### Database Knowledge
- Basic SQL understanding
- Familiarity with database concepts (tables, relationships, queries)
- No prior graph database experience required

## Step-by-Step Setup

### 1. Environment Preparation

#### Create Project Directory
```bash
mkdir relational_to_graph_project
cd relational_to_graph_project
```

#### Set Up Python Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv graph_env

# Activate virtual environment
# On Windows:
graph_env\Scripts\activate
# On macOS/Linux:
source graph_env/bin/activate
```

#### Install Required Python Packages
```bash
pip install pandas faker neo4j
```

### 2. Neo4j Setup Options

#### Option A: Neo4j Desktop (Recommended for Beginners)

1. **Download Neo4j Desktop**
   - Visit [neo4j.com/download](https://neo4j.com/download/)
   - Download Neo4j Desktop for your operating system
   - Install following the provided instructions

2. **Create a New Project**
   - Open Neo4j Desktop
   - Click "New Project"
   - Name it "Application Portfolio Analysis"

3. **Add a Database**
   - Click "Add Database" → "Create a Local Database"
   - Name: "applications-graph"
   - Password: "password" (or choose your own and update scripts)
   - Version: Use the latest stable version

4. **Start the Database**
   - Click the "Start" button next to your database
   - Wait for the status to show "Active"

5. **Verify Connection**
   - Click "Open" to access Neo4j Browser
   - You should see the Neo4j Browser interface

#### Option B: Neo4j Aura (Cloud-based)

1. **Create Aura Account**
   - Visit [neo4j.com/cloud/aura](https://neo4j.com/cloud/aura/)
   - Sign up for a free account

2. **Create Database Instance**
   - Click "Create Database"
   - Choose "AuraDB Free"
   - Name: "applications-graph"
   - Region: Choose closest to your location

3. **Download Credentials**
   - Save the connection URI, username, and password
   - Update these in the migration scripts

4. **Test Connection**
   - Use the provided Neo4j Browser link to verify access

#### Option C: Neo4j Community Server (Advanced)

1. **Download and Install**
   - Download from [neo4j.com/download-center](https://neo4j.com/download-center/)
   - Follow installation instructions for your OS

2. **Configure Database**
   - Set initial password using `neo4j-admin`
   - Configure memory settings if needed

3. **Start Service**
   - Start Neo4j service
   - Access via http://localhost:7474

### 3. Project Files Setup

#### Download Project Files
If you received this as a complete project:
```bash
# Extract all files to your project directory
# Ensure the following structure exists:
relational_to_graph_project/
├── scripts/
├── sql/
├── data/
└── docs/
```

#### Verify File Structure
```bash
ls -la
# Should show: scripts/, sql/, data/, docs/, README.md
```

### 4. Configuration Updates

#### Update Neo4j Connection Details
Edit the following files to match your Neo4j setup:

**scripts/migrate_to_neo4j.py**
```python
# Update these lines with your connection details
NEO4J_URI = "bolt://localhost:7687"  # or your Aura URI
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # your actual password
```

**scripts/neo4j_queries.py**
```python
# Update these lines with your connection details
NEO4J_URI = "bolt://localhost:7687"  # or your Aura URI
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # your actual password
```

### 5. Test Installation

#### Test Python Environment
```bash
python -c "import pandas, faker, neo4j; print('All packages installed successfully')"
```

#### Test Neo4j Connection
```bash
python -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password'))
with driver.session() as session:
    result = session.run('RETURN 1 as test')
    print('Neo4j connection successful:', result.single()['test'])
driver.close()
"
```

## Running the Project

### Step 1: Generate Sample Data
```bash
cd scripts
python generate_data.py
```
**Expected Output:**
```
Generated applications.csv with 100 records.
```

### Step 2: Create SQLite Database
```bash
python create_db.py
```
**Expected Output:**
```
Schema from ../sql/applications.sql loaded successfully.
Data from ../data/applications.csv loaded successfully into 'applications' table.
```

### Step 3: Explore Relational Data
```bash
python explore_db.py
```
**Expected Output:**
```
=== DATABASE EXPLORATION ===
Total applications in database: 100
=== BASIC STATISTICS ===
Active applications: 93
Inactive applications: 7
...
```

### Step 4: Migrate to Neo4j
```bash
python migrate_to_neo4j.py
```
**Expected Output:**
```
INFO:__main__:Starting migration from SQLite to Neo4j
INFO:__main__:Loaded 100 records from SQLite
INFO:__main__:Cleared Neo4j database
INFO:__main__:Created 100 Application nodes
...
INFO:__main__:Migration completed successfully
```

### Step 5: Analyze Graph Data
```bash
python neo4j_queries.py
```
**Expected Output:**
```
RUNNING COMPREHENSIVE GRAPH ANALYSIS
==================================================
=== BASIC GRAPH STATISTICS ===
Total Applications: 100
Total Categories: 20
...
```

## Troubleshooting Common Issues

### Python Package Issues

**Problem:** `ModuleNotFoundError: No module named 'pandas'`
**Solution:**
```bash
pip install pandas faker neo4j
# If using virtual environment, ensure it's activated
```

**Problem:** Permission errors during package installation
**Solution:**
```bash
# Use --user flag
pip install --user pandas faker neo4j
# Or use virtual environment
```

### Neo4j Connection Issues

**Problem:** `ServiceUnavailable: Failed to establish connection`
**Solutions:**
1. Verify Neo4j is running
2. Check connection URI (bolt:// vs neo4j://)
3. Verify username and password
4. Check firewall settings

**Problem:** `AuthError: The client is unauthorized`
**Solutions:**
1. Verify username and password
2. Reset password in Neo4j Desktop
3. Check authentication method

### Data Generation Issues

**Problem:** `FileNotFoundError` when running scripts
**Solution:**
```bash
# Ensure you're in the correct directory
cd relational_to_graph_project/scripts
# Check if data directory exists
mkdir -p ../data
```

**Problem:** SQLite database creation fails
**Solution:**
```bash
# Check file permissions
chmod 755 ../data
# Verify SQL file exists
ls -la ../sql/applications.sql
```

### Performance Issues

**Problem:** Migration takes too long
**Solutions:**
1. Reduce sample data size in `generate_data.py`
2. Increase Neo4j memory allocation
3. Check system resources

**Problem:** Queries run slowly
**Solutions:**
1. Verify indexes are created
2. Check Neo4j memory settings
3. Optimize query patterns

## Verification Steps

### Verify SQLite Database
```bash
sqlite3 ../data/applications.db "SELECT COUNT(*) FROM applications;"
# Should return: 100
```

### Verify Neo4j Migration
Open Neo4j Browser and run:
```cypher
MATCH (n) RETURN labels(n) as node_type, count(n) as count
```
Should show multiple node types with counts.

### Verify Relationships
```cypher
MATCH ()-[r]->() RETURN type(r) as relationship_type, count(r) as count
```
Should show various relationship types.

## Next Steps

Once setup is complete:
1. Review the generated data in `data/applications.csv`
2. Explore the SQLite database structure
3. Examine the Neo4j graph in Neo4j Browser
4. Run the provided analysis queries
5. Experiment with your own queries
6. Read the documentation in the `docs/` folder

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Verify all prerequisites are met
4. Check the project documentation
5. Ensure all file paths are correct

## System Requirements

### Minimum Requirements
- **RAM:** 4GB (8GB recommended)
- **Storage:** 1GB free space
- **CPU:** Any modern processor
- **OS:** Windows 10+, macOS 10.14+, or Linux

### Recommended Requirements
- **RAM:** 8GB or more
- **Storage:** 5GB free space
- **CPU:** Multi-core processor
- **OS:** Latest stable versions

This setup guide should get you up and running with the relational to graph database migration project. Take your time with each step and verify everything works before proceeding to the next phase.

