# Neo4j Cypher Query Examples

This document provides a comprehensive collection of Cypher queries that demonstrate the power of graph databases for analyzing application relationships and patterns.

## Basic Graph Statistics

### Count all nodes by type
```cypher
MATCH (n)
RETURN labels(n) as node_type, count(n) as count
ORDER BY count DESC
```

### Count all relationships by type
```cypher
MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(r) as count
ORDER BY count DESC
```

## Vendor Analysis

### Find top vendors by application count
```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
RETURN v.name as vendor, count(a) as app_count, 
       sum(a.annual_cost) as total_cost
ORDER BY app_count DESC
LIMIT 10
```

### Find vendors with highest total costs
```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
WHERE a.annual_cost IS NOT NULL
RETURN v.name as vendor, sum(a.annual_cost) as total_cost
ORDER BY total_cost DESC
LIMIT 10
```

### Find vendors supplying critical applications
```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
WHERE a.criticality = 'critical'
RETURN v.name as vendor, count(a) as critical_apps
ORDER BY critical_apps DESC
```

## Dependency Analysis

### Find most common dependencies
```cypher
MATCH (e:ExternalApp)<-[:DEPENDS_ON]-(a:Application)
RETURN e.name as external_app, count(a) as dependent_apps
ORDER BY dependent_apps DESC
LIMIT 10
```

### Find applications with most dependencies
```cypher
MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)
RETURN a.name as app, count(e) as dependency_count
ORDER BY dependency_count DESC
LIMIT 10
```

### Identify shared dependencies (potential single points of failure)
```cypher
MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(other:Application)
WHERE a <> other
RETURN e.name as shared_dependency, 
       collect(DISTINCT a.name) as dependent_apps,
       count(DISTINCT a) as app_count
ORDER BY app_count DESC
LIMIT 10
```

### Find dependency chains
```cypher
MATCH path = (a:Application)-[:DEPENDS_ON*2..4]->(e:ExternalApp)
RETURN a.name as starting_app, 
       [node in nodes(path) | node.name] as dependency_chain,
       length(path) as chain_length
ORDER BY chain_length DESC
LIMIT 10
```

## Integration Analysis

### Find most common integration points
```cypher
MATCH (e:ExternalApp)<-[:INTEGRATES_WITH]-(a:Application)
RETURN e.name as external_app, count(a) as integrating_apps
ORDER BY integrating_apps DESC
LIMIT 10
```

### Find applications with most integrations
```cypher
MATCH (a:Application)-[:INTEGRATES_WITH]->(e:ExternalApp)
RETURN a.name as app, count(e) as integration_count
ORDER BY integration_count DESC
LIMIT 10
```

### Identify integration hubs
```cypher
MATCH (a1:Application)-[:INTEGRATES_WITH]->(e:ExternalApp)<-[:INTEGRATES_WITH]-(a2:Application)
WHERE a1 <> a2
RETURN e.name as integration_hub, 
       count(DISTINCT a1) + count(DISTINCT a2) as connected_apps
ORDER BY connected_apps DESC
LIMIT 10
```

## Department Analysis

### Find departments by application count
```cypher
MATCH (d:Department)<-[:OWNED_BY]-(a:Application)
RETURN d.name as department, count(a) as app_count,
       sum(a.annual_cost) as total_cost
ORDER BY app_count DESC
LIMIT 10
```

### Find departments with critical applications
```cypher
MATCH (d:Department)<-[:OWNED_BY]-(a:Application)
WHERE a.criticality = 'critical'
RETURN d.name as department, count(a) as critical_apps
ORDER BY critical_apps DESC
```

### Analyze department application categories
```cypher
MATCH (d:Department)<-[:OWNED_BY]-(a:Application)-[:BELONGS_TO]->(c:Category)
WHERE c.type = 'main'
RETURN d.name as department, c.name as category, count(a) as app_count
ORDER BY department, app_count DESC
```

## Category Analysis

### Analyze application categories
```cypher
MATCH (c:Category)<-[:BELONGS_TO]-(a:Application)
WHERE c.type = 'main'
RETURN c.name as category, count(a) as app_count,
       avg(a.annual_cost) as avg_cost
ORDER BY app_count DESC
```

### Find vendor diversity by category
```cypher
MATCH (c:Category)<-[:BELONGS_TO]-(a:Application)-[:SUPPLIED_BY]->(v:Vendor)
WHERE c.type = 'main'
RETURN c.name as category, count(DISTINCT v) as vendor_count
ORDER BY vendor_count DESC
```

### Find critical applications by category
```cypher
MATCH (c:Category)<-[:BELONGS_TO]-(a:Application)
WHERE c.type = 'main' AND a.criticality = 'critical'
RETURN c.name as category, count(a) as critical_apps
ORDER BY critical_apps DESC
```

## People Analysis

### Find people with most application responsibilities
```cypher
MATCH (p:Person)-[r]->(a:Application)
RETURN p.name as person, type(r) as role, count(a) as app_count
ORDER BY app_count DESC
LIMIT 15
```

### Find people owning critical applications
```cypher
MATCH (p:Person)-[:OWNS]->(a:Application)
WHERE a.criticality = 'critical'
RETURN p.name as person, count(a) as critical_apps
ORDER BY critical_apps DESC
```

### Find people by cost responsibility
```cypher
MATCH (p:Person)-[:OWNS]->(a:Application)
RETURN p.name as person, sum(a.annual_cost) as total_cost_responsibility
ORDER BY total_cost_responsibility DESC
LIMIT 10
```

## Advanced Pattern Analysis

### Find applications connected through external apps
```cypher
MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)<-[:INTEGRATES_WITH]-(other:Application)
WHERE a <> other
RETURN a.name as app1, other.name as app2, e.name as common_external_app
LIMIT 10
```

### Analyze vendor-department relationships
```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)-[:OWNED_BY]->(d:Department)
RETURN v.name as vendor, d.name as department, count(a) as app_count
ORDER BY app_count DESC
LIMIT 15
```

### Find end-of-life applications and their impact
```cypher
MATCH (a:Application)
WHERE a.end_of_life_date IS NOT NULL
MATCH (a)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(other:Application)
WHERE other.end_of_life_date IS NULL
RETURN a.name as eol_app, collect(DISTINCT other.name) as affected_apps
```

### Find high-cost subscription vendors
```cypher
MATCH (a:Application)
WHERE a.license_type = 'subscription' AND a.annual_cost > 50000
MATCH (a)-[:SUPPLIED_BY]->(v:Vendor)
RETURN v.name as vendor, sum(a.annual_cost) as total_subscription_cost,
       count(a) as expensive_apps
ORDER BY total_subscription_cost DESC
```

## Compliance Analysis

### Analyze compliance requirements distribution
```cypher
MATCH (a:Application)
WHERE a.compliance_requirements IS NOT NULL AND a.compliance_requirements <> ''
UNWIND split(a.compliance_requirements, ',') as compliance
RETURN trim(compliance) as requirement, count(a) as app_count
ORDER BY app_count DESC
```

### Find vendors with GDPR-compliant applications
```cypher
MATCH (a:Application)-[:SUPPLIED_BY]->(v:Vendor)
WHERE a.compliance_requirements CONTAINS 'GDPR'
RETURN v.name as vendor, count(a) as gdpr_apps
ORDER BY gdpr_apps DESC
```

### Find departments with critical data applications
```cypher
MATCH (a:Application)-[:OWNED_BY]->(d:Department)
WHERE a.data_sensitivity = 'critical'
RETURN d.name as department, count(a) as critical_data_apps
ORDER BY critical_data_apps DESC
```

## Path Analysis

### Find shortest path between two applications through dependencies
```cypher
MATCH (a1:Application {name: 'App1'}), (a2:Application {name: 'App2'})
MATCH path = shortestPath((a1)-[:DEPENDS_ON*]-(a2))
RETURN path
```

### Find all paths of specific length
```cypher
MATCH path = (a:Application)-[:DEPENDS_ON*2]-(other:Application)
WHERE a <> other
RETURN a.name, other.name, length(path) as path_length
LIMIT 10
```

## Aggregation Queries

### Calculate total cost by vendor and category
```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)-[:BELONGS_TO]->(c:Category)
WHERE c.type = 'main'
RETURN v.name as vendor, c.name as category, 
       sum(a.annual_cost) as total_cost, count(a) as app_count
ORDER BY total_cost DESC
```

### Find average application cost by deployment type
```cypher
MATCH (a:Application)
WHERE a.annual_cost IS NOT NULL
RETURN a.deployment_type, avg(a.annual_cost) as avg_cost, count(a) as app_count
ORDER BY avg_cost DESC
```

## Recommendation Queries

### Find similar applications (same category and vendor)
```cypher
MATCH (a:Application)-[:BELONGS_TO]->(c:Category)<-[:BELONGS_TO]-(similar:Application)
MATCH (a)-[:SUPPLIED_BY]->(v:Vendor)<-[:SUPPLIED_BY]-(similar)
WHERE a <> similar
RETURN a.name as app, similar.name as similar_app, c.name as category, v.name as vendor
LIMIT 10
```

### Find potential consolidation opportunities
```cypher
MATCH (a1:Application)-[:BELONGS_TO]->(c:Category)<-[:BELONGS_TO]-(a2:Application)
WHERE a1 <> a2 AND a1.in_use = true AND a2.in_use = true
RETURN c.name as category, collect(a1.name) as applications, count(*) as app_count
HAVING app_count > 2
ORDER BY app_count DESC
```

These queries demonstrate the power of graph databases in revealing relationships and patterns that would be difficult to discover using traditional SQL queries on relational data.

