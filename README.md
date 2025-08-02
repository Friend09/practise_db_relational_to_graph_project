# Relational to Graph Database Migration Project

## Overview

This project demonstrates how to convert a traditional relational database into a knowledge graph using Neo4j, revealing relationship patterns and insights that are difficult to discover with standard SQL queries. Through application portfolio management analysis, you'll learn graph database modeling, Cypher query language, and when to choose graph databases over relational ones.

## Project Structure

```
relational_to_graph_project/
├── README.md                              # This file
├── .env.example                           # Environment configuration template
├── requirements.txt                       # Python dependencies
├── sql/
│   └── applications.sql                   # SQL schema for applications table
├── data/
│   ├── applications.csv                   # Sample data (generated)
│   └── applications.db                    # SQLite database (generated)
├── scripts/
│   ├── generate_data.py                   # Generate sample application data
│   ├── create_db.py                       # Create SQLite database and load data
│   ├── explore_db.py                      # Explore relational database
│   ├── migrate_to_neo4j.py                # Migrate data to Neo4j
│   └── neo4j_queries.py                   # Neo4j analysis examples
├── tests/
│   ├── test_setup.py                      # Complete setup validation
│   └── test_neo4j.py                      # Neo4j connection test
└── notes/
    ├── README.md                          # Documentation navigation guide
    ├── 00_Setup_and_Configuration_Guide.md   # Complete setup instructions
    ├── 01_Query_Reference_and_Examples.md    # Cypher queries and examples
    ├── 02_Project_Overview_and_Analysis.md   # Strategic insights and analysis
    └── 03_Technical_Documentation.md         # Graph model and technical details
```

## What You'll Learn

- **Graph Database Modeling**: Design graph schemas from relational data
- **Cypher Query Language**: Master pattern matching and relationship traversal
- **Migration Strategies**: Convert relational data to graph format
- **Relationship Analysis**: Discover patterns through graph traversal
- **Performance Insights**: Understand when graphs outperform relational databases
- **Business Intelligence**: Apply graph analysis to real-world scenarios

## Prerequisites

- Python 3.7+
- Neo4j Desktop or Neo4j Aura account
- Basic understanding of databases and SQL
- Familiarity with Python programming

## Quick Start

### Prerequisites

- Python 3.7+
- Neo4j Desktop or Neo4j Aura account

### Installation

```bash
# Install dependencies
pip install pandas faker neo4j python-dotenv

# Verify installation
python -c "import pandas, faker, neo4j, sqlite3; from dotenv import load_dotenv; print('✅ All packages installed!')"
```

### Setup Neo4j

1. **Neo4j Desktop**: Download from [neo4j.com](https://neo4j.com/download/), create database
2. **Neo4j Aura**: Sign up at [neo4j.com/aura](https://neo4j.com/aura/) for cloud instance

### Configure Environment

```bash
cp .env.example .env
# Edit .env with your Neo4j connection details
```

**📖 For detailed setup instructions and troubleshooting, see:** [**Setup Guide**](notes/00_Setup_and_Configuration_Guide.md)

## Run the Project

### Step 1: Verify Setup

```bash
python tests/test_setup.py
```

All tests should pass ✅

### Step 2: Execute Migration Workflow

```bash
cd scripts
python generate_data.py      # Creates sample data (applications.csv)
python create_db.py          # Sets up SQLite database
python migrate_to_neo4j.py   # Migrates data to Neo4j
python neo4j_queries.py      # Runs graph analysis
```

**🎉 That's it!** You now have a complete application portfolio graph with 100 sample applications and can explore powerful relationship analysis.

## 📚 Complete Documentation

### Documentation Structure

- **[Setup Guide](notes/00_Setup_and_Configuration_Guide.md)** - Complete environment setup, troubleshooting, and system requirements
- **[Query Reference](notes/01_Query_Reference_and_Examples.md)** - 50+ business-focused Cypher queries, cost optimization, dependency analysis, and SQL vs Cypher comparisons
- **[Project Analysis](notes/02_Project_Overview_and_Analysis.md)** - Strategic insights, business value, and implementation best practices
- **[Technical Docs](notes/03_Technical_Documentation.md)** - Graph model design, migration strategies, and performance optimization

### 🎯 Quick Navigation

| Need to...                    | Go to Document   | Section                             |
| ----------------------------- | ---------------- | ----------------------------------- |
| Set up the project            | Setup Guide      | Step 1-5                            |
| Fix connection issues         | Setup Guide      | Troubleshooting                     |
| Find vendor analysis queries  | Query Reference  | Vendor Analysis                     |
| Understand graph vs SQL       | Query Reference  | SQL vs Cypher Comparison            |
| Learn about business benefits | Project Analysis | Business Value and Strategic Impact |
| Understand the graph model    | Technical Docs   | Graph Database Model Design         |
| Add new node types            | Technical Docs   | Schema Evolution                    |
| Optimize query performance    | Technical Docs   | Performance Optimization            |

## Key Features

### Data Model

- **6 Node Types**: Applications, Categories, Vendors, Departments, People, External Apps
- **8 Relationship Types**: BELONGS_TO, SUPPLIED_BY, OWNED_BY, DEPENDS_ON, etc.
- **Realistic Data**: 100 sample applications with complex interdependencies

### Analysis Capabilities

- **Vendor Risk Assessment**: Identify consolidation opportunities and dependencies
- **Dependency Analysis**: Find shared dependencies and single points of failure
- **Cost Optimization**: Discover unused applications and high cost-per-user scenarios
- **Portfolio Intelligence**: Department-level analysis and compliance tracking

### Query Examples

**Find Shared Dependencies (Graph vs SQL advantage):**

```cypher
MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(other:Application)
WHERE a <> other
RETURN e.name as shared_dependency, count(DISTINCT a) as risk_level
ORDER BY risk_level DESC
```

**📖 For 50+ more query examples, see:** [**Query Reference**](notes/01_Query_Reference_and_Examples.md)

## Learning Outcomes

- **Graph Database Fundamentals**: When to use graphs vs relational databases
- **Cypher Mastery**: Pattern matching, relationship traversal, and optimization
- **Data Migration**: Strategies for converting relational to graph format
- **Business Analysis**: Vendor risk, dependency analysis, and cost optimization
- **Performance Insights**: Understanding graph database advantages and trade-offs

## Next Steps

1. **Explore the Data**: Use Neo4j Browser to visually explore the application graph
2. **Try Custom Queries**: Modify existing queries or create your own analysis
3. **Add Real Data**: Replace sample data with your organization's application portfolio
4. **Advanced Features**: Explore graph algorithms and machine learning capabilities

## Troubleshooting

**Common Issues:**

- **Neo4j won't start**: Check port 7687 availability, restart Neo4j Desktop
- **Connection errors**: Verify `.env` file configuration and database status
- **Import failures**: Ensure Neo4j is running and credentials are correct

**📖 For comprehensive troubleshooting:** [**Setup Guide**](notes/00_Setup_and_Configuration_Guide.md)

## Contributing

This project is designed for learning. Feel free to:

- Add new analysis queries and extend the data model
- Create visualization examples and improve documentation
- Share your insights and real-world applications

## Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Cypher Query Language Guide](https://neo4j.com/developer/cypher/)
- [Graph Database Concepts](https://neo4j.com/developer/graph-database/)

This project demonstrates the transformative power of graph databases for relationship analysis and provides a foundation for advanced graph analytics in enterprise environments.
