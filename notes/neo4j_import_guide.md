# Neo4j Application Portfolio Import Guide

## Data Model Overview

Based on your CSV structure, here's the proposed graph model:

### Nodes
- **Application** - Core entity with all app properties
- **Vendor** - Companies providing applications
- **Person** - App owners, technical leads, business owners
- **Department** - Organizational units using apps
- **Category** - High-level app categories
- **Subcategory** - Detailed app classifications

### Relationships
- `(:Application)-[:PROVIDED_BY]->(:Vendor)`
- `(:Application)-[:OWNED_BY]->(:Person {role: 'app_owner'})`
- `(:Application)-[:TECH_LEAD]->(:Person {role: 'technical_lead'})`
- `(:Application)-[:BUSINESS_OWNER]->(:Person {role: 'business_owner'})`
- `(:Application)-[:USED_BY]->(:Department)`
- `(:Application)-[:BELONGS_TO]->(:Category)`
- `(:Application)-[:SUBCATEGORY_OF]->(:Subcategory)`
- `(:Application)-[:DEPENDS_ON]->(:Application)`
- `(:Application)-[:INTEGRATES_WITH]->(:Application)`

## Step 1: Prepare Your Neo4j Environment

1. **Start your Neo4j instance** "Learn App Portfolio Analysis"
2. **Open Neo4j Browser** (usually http://localhost:7474)
3. **Select database** "learn-graph-db"
4. **Clear any existing data** (if needed):
   ```cypher
   MATCH (n) DETACH DELETE n
   ```

## Step 2: Copy CSV to Neo4j Import Directory

Copy your `applications.csv` file to the Neo4j import directory:
- **Mac**: `~/Library/Application Support/Neo4j Desktop/Application/relate-data/dbmss/[dbms-id]/import/`
- **Alternative**: Use the `file:///` protocol with absolute path

## Step 3: Data Import Cypher Queries

Execute these queries in order in Neo4j Browser:

### 3.1 Create Constraints (for performance and data integrity)
```cypher
// Create constraints
CREATE CONSTRAINT app_id_unique FOR (a:Application) REQUIRE a.app_id IS UNIQUE;
CREATE CONSTRAINT vendor_name_unique FOR (v:Vendor) REQUIRE v.name IS UNIQUE;
CREATE CONSTRAINT person_name_unique FOR (p:Person) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT department_name_unique FOR (d:Department) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT category_name_unique FOR (c:Category) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT subcategory_name_unique FOR (s:Subcategory) REQUIRE s.name IS UNIQUE;
```

### 3.2 Import Applications
```cypher
LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
WHERE row.app_id IS NOT NULL
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

### 3.3 Import Vendors and Create Relationships
```cypher
LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
WHERE row.vendor_name IS NOT NULL
MERGE (v:Vendor {name: row.vendor_name})
ON CREATE SET v.contact_email = row.vendor_contact_email
WITH v, row
MATCH (a:Application {app_id: toInteger(row.app_id)})
MERGE (a)-[:PROVIDED_BY]->(v);
```

### 3.4 Import People and Create Relationships
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

### 3.5 Import Departments and Create Relationships
```cypher
LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
WHERE row.department IS NOT NULL
MERGE (d:Department {name: row.department})
WITH d, row
MATCH (a:Application {app_id: toInteger(row.app_id)})
MERGE (a)-[:USED_BY]->(d);
```

### 3.6 Import Categories and Subcategories
```cypher
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

### 3.7 Create Application Dependencies
```cypher
LOAD CSV WITH HEADERS FROM 'file:///applications.csv' AS row
WHERE row.depends_on_apps IS NOT NULL
WITH row, split(row.depends_on_apps, ',') AS deps
MATCH (a:Application {app_id: toInteger(row.app_id)})
UNWIND deps AS dep
WITH a, trim(dep) AS dependency_name
MATCH (dep_app:Application)
WHERE dep_app.name CONTAINS dependency_name
MERGE (a)-[:DEPENDS_ON]->(dep_app);
```

### 3.8 Create Application Integrations
```cypher
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

## Step 4: Verification Queries

Check your import was successful:

```cypher
// Count nodes
MATCH (n) RETURN labels(n) AS NodeType, count(n) AS Count;

// Count relationships
MATCH ()-[r]->() RETURN type(r) AS RelationshipType, count(r) AS Count;

// Check sample data
MATCH (a:Application)-[r]->(n) 
RETURN a.name, type(r), labels(n), 
       CASE WHEN 'Person' IN labels(n) THEN n.name
            WHEN 'Vendor' IN labels(n) THEN n.name
            WHEN 'Department' IN labels(n) THEN n.name
            WHEN 'Category' IN labels(n) THEN n.name
            ELSE toString(n) END AS target
LIMIT 20;
```

## Step 5: Sample Analysis Queries

Now you can start exploring your data with these example queries:

### Most Expensive Applications
```cypher
MATCH (a:Application)
WHERE a.annual_cost IS NOT NULL
RETURN a.name, a.annual_cost, a.criticality
ORDER BY a.annual_cost DESC
LIMIT 10;
```

### Application Dependencies Graph
```cypher
MATCH (a:Application)-[:DEPENDS_ON]->(dep:Application)
RETURN a.name AS Application, dep.name AS DependsOn
ORDER BY a.name;
```

### Vendor Portfolio Analysis
```cypher
MATCH (v:Vendor)<-[:PROVIDED_BY]-(a:Application)
RETURN v.name AS Vendor, 
       count(a) AS ApplicationCount,
       sum(a.annual_cost) AS TotalCost,
       avg(a.annual_cost) AS AvgCost
ORDER BY TotalCost DESC;
```

### Critical Applications by Department
```cypher
MATCH (d:Department)<-[:USED_BY]-(a:Application)
WHERE a.criticality = 'high'
RETURN d.name AS Department, 
       count(a) AS CriticalApps,
       sum(a.annual_cost) AS TotalCost
ORDER BY CriticalApps DESC;
```

### People with Multiple Responsibilities
```cypher
MATCH (p:Person)
WITH p, 
     [(a:Application)-[:OWNED_BY]->(p) | a] AS owned,
     [(a:Application)-[:TECH_LEAD]->(p) | a] AS tech_lead,
     [(a:Application)-[:BUSINESS_OWNER]->(p) | a] AS business_owner
WHERE size(owned) + size(tech_lead) + size(business_owner) > 1
RETURN p.name, 
       size(owned) AS AppsOwned,
       size(tech_lead) AS TechLead,
       size(business_owner) AS BusinessOwner,
       size(owned) + size(tech_lead) + size(business_owner) AS TotalResponsibilities
ORDER BY TotalResponsibilities DESC;
```

## Next Steps for Learning

1. **Explore the Graph Visually**: Use the Neo4j Browser to visualize relationships
2. **Practice Cypher**: Try modifying the sample queries above
3. **Advanced Analytics**: Learn about graph algorithms (shortest path, centrality measures)
4. **Data Updates**: Practice updating nodes and relationships
5. **Performance**: Learn about indexing and query optimization

## Common Commands for Exploration

```cypher
// See the schema
CALL db.schema.visualization();

// Find orphaned nodes (no relationships)
MATCH (n) WHERE NOT (n)--() RETURN n;

// Get random sample of data
MATCH (a:Application) RETURN a LIMIT 5;

// Clear specific data if needed
MATCH (n:Application) DETACH DELETE n;
```
