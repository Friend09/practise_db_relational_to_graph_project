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
```bash
pip install pandas faker neo4j sqlite3
```

### 3. Set Up Neo4j

#### Option A: Neo4j Desktop (Recommended for Learning)
1. Download and install [Neo4j Desktop](https://neo4j.com/download/)
2. Create a new project
3. Add a local DBMS with password "password" (or update the scripts with your password)
4. Start the database

#### Option B: Neo4j Aura (Cloud)
1. Sign up for [Neo4j Aura](https://neo4j.com/cloud/aura/)
2. Create a free instance
3. Update connection details in the migration scripts

## Quick Start Guide

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

