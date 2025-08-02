# Query Reference and Examples

## Overview

This comprehensive guide provides Cypher query examples for analyzing application portfolios in Neo4j, comparing SQL vs Cypher approaches, and demonstrating advanced graph analysis patterns.

## Basic Graph Statistics

### Node and Relationship Counts

```cypher
// Count all nodes by type
MATCH (n)
RETURN labels(n) as node_type, count(n) as count
ORDER BY count DESC
```

```cypher
// Count all relationships by type
MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(r) as count
ORDER BY count DESC
```

```cypher
// Get complete graph overview
CALL db.schema.visualization()
```

### Data Structure Exploration

```cypher
// Explore sample data with relationships
MATCH (a:Application)-[r]->(n)
RETURN a.name, type(r), labels(n),
       CASE WHEN 'Person' IN labels(n) THEN n.name
            WHEN 'Vendor' IN labels(n) THEN n.name
            WHEN 'Department' IN labels(n) THEN n.name
            WHEN 'Category' IN labels(n) THEN n.name
            ELSE toString(n) END AS target
LIMIT 20;
```

```cypher
// Find orphaned nodes (no relationships)
MATCH (n) WHERE NOT (n)--() RETURN n;
```

```cypher
// Get random sample of applications
MATCH (a:Application) RETURN a LIMIT 5;
```

## Quick Start Analysis Queries

These queries are specifically designed for the imported application portfolio data and provide immediate insights:

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

### Find Unused Applications Costing Money

```cypher
MATCH (a:Application)
WHERE a.in_use = false AND a.annual_cost > 0
RETURN a.name AS Application,
       a.annual_cost AS AnnualCost,
       a.criticality AS Criticality,
       a.vendor_name AS Vendor
ORDER BY a.annual_cost DESC
```

### High Cost per User Applications

```cypher
MATCH (a:Application)
WHERE a.annual_cost > 200000 AND a.user_count < 100
RETURN a.name AS Application,
       a.annual_cost AS Cost,
       a.user_count AS Users,
       round(a.annual_cost / a.user_count) AS CostPerUser
ORDER BY CostPerUser DESC
```

### Department Cost Analysis

```cypher
MATCH (d:Department)<-[:USED_BY]-(a:Application)
WITH d,
     count(a) AS totalApps,
     sum(a.annual_cost) AS totalCost,
     sum(CASE WHEN a.criticality = 'critical' THEN 1 ELSE 0 END) AS criticalApps,
     sum(CASE WHEN a.in_use = false THEN a.annual_cost ELSE 0 END) AS wastedCost
RETURN d.name AS Department,
       totalApps AS TotalApplications,
       totalCost AS TotalAnnualCost,
       criticalApps AS CriticalApplications,
       wastedCost AS UnusedAppCost,
       round(wastedCost / totalCost * 100) AS WastePercentage
ORDER BY totalCost DESC
```

## Vendor Analysis

### Top Vendors by Application Count

```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
RETURN v.name as vendor, count(a) as app_count,
       sum(a.annual_cost) as total_cost
ORDER BY app_count DESC
LIMIT 10
```

### Vendor Consolidation Opportunities

```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)
WITH v,
     count(a) AS appCount,
     sum(a.annual_cost) AS totalSpend,
     sum(CASE WHEN a.criticality IN ['high', 'critical'] THEN 1 ELSE 0 END) AS criticalApps
WHERE appCount > 1 OR totalSpend > 400000
RETURN v.name AS Vendor,
       appCount AS Applications,
       totalSpend AS TotalSpend,
       criticalApps AS CriticalApps,
       round(totalSpend / appCount) AS AvgCostPerApp
ORDER BY totalSpend DESC
```

### Vendor Dependency Mapping

```cypher
MATCH (v:Vendor)<-[:PROVIDED_BY]-(a:Application)-[:DEPENDS_ON]->(dep:Application)-[:PROVIDED_BY]->(depVendor:Vendor)
WHERE v <> depVendor
RETURN v.name AS Vendor,
       depVendor.name AS DependsOnVendor,
       count(*) AS ConnectionCount,
       collect(DISTINCT a.name) AS Applications
ORDER BY ConnectionCount DESC
```

## Dependency Risk Analysis

### Critical Dependency Impact Analysis

```cypher
MATCH (critical:Application {name: "Miro"})<-[:DEPENDS_ON]-(dependent:Application)
RETURN critical.name AS CriticalApp,
       collect(dependent.name) AS DependentApps,
       count(dependent) AS DependentCount,
       sum(dependent.annual_cost) AS TotalDependentCost
ORDER BY DependentCount DESC
```

### Shared Dependencies (Single Points of Failure)

```cypher
MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(other:Application)
WHERE a <> other
RETURN e.name as shared_dependency,
       collect(DISTINCT a.name) as dependent_apps,
       count(DISTINCT a) as app_count
ORDER BY app_count DESC
LIMIT 10
```

### Dependency Chain Analysis

```cypher
MATCH path = (a:Application)-[:DEPENDS_ON*1..3]->(d:Application)
WITH a, length(path) AS depth, count(DISTINCT d) AS totalDependencies
WHERE depth > 1
RETURN a.name AS Application,
       depth AS MaxDependencyDepth,
       totalDependencies AS TotalDependencies,
       a.criticality AS Criticality
ORDER BY depth DESC, totalDependencies DESC
```

### Find Circular Dependencies

```cypher
MATCH (a:Application)-[:DEPENDS_ON*1..10]->(a)
RETURN a.name as app_with_circular_dependency
```

## Integration Analysis

### Integration Hub Identification

```cypher
MATCH (a1:Application)-[:INTEGRATES_WITH]->(e:ExternalApp)<-[:INTEGRATES_WITH]-(a2:Application)
WHERE a1 <> a2
RETURN e.name as integration_hub,
       count(DISTINCT a1) + count(DISTINCT a2) as connected_apps
ORDER BY connected_apps DESC
LIMIT 10
```

### Most Connected Applications

```cypher
MATCH (a:Application)
OPTIONAL MATCH (a)-[dep:DEPENDS_ON]->()
OPTIONAL MATCH (a)-[int:INTEGRATES_WITH]->()
OPTIONAL MATCH ()-[depOn:DEPENDS_ON]->(a)
OPTIONAL MATCH ()-[intWith:INTEGRATES_WITH]->(a)
WITH a,
     count(dep) AS outgoingDeps,
     count(int) AS outgoingInts,
     count(depOn) AS incomingDeps,
     count(intWith) AS incomingInts
WITH a,
     outgoingDeps + outgoingInts + incomingDeps + incomingInts AS totalConnections,
     outgoingDeps, outgoingInts, incomingDeps, incomingInts
WHERE totalConnections > 0
RETURN a.name AS Application,
       totalConnections AS TotalConnections,
       incomingDeps AS IncomingDependencies,
       outgoingDeps AS OutgoingDependencies,
       incomingInts AS IncomingIntegrations,
       outgoingInts AS OutgoingIntegrations,
       a.criticality AS Criticality
ORDER BY totalConnections DESC
LIMIT 20
```

## People and Organizational Analysis

### People with Multiple Critical App Responsibilities

```cypher
MATCH (p:Person)<-[r]-(a:Application)
WHERE a.criticality IN ['high', 'critical']
WITH p, type(r) AS role, count(a) AS appCount, collect(a.name) AS apps
WHERE appCount > 1
RETURN p.name AS Person,
       role AS Role,
       appCount AS CriticalAppsManaged,
       apps AS Applications
ORDER BY appCount DESC
```

### High-Value People (by Cost Responsibility)

```cypher
MATCH (p:Person)-[:OWNS]->(a:Application)
RETURN p.name as person, sum(a.annual_cost) as total_cost_responsibility
ORDER BY total_cost_responsibility DESC
LIMIT 10
```

## Security and Compliance Analysis

### High-Risk Security Applications

```cypher
MATCH (a:Application)
WHERE a.security_classification = 'restricted'
   OR a.data_sensitivity = 'high'
RETURN a.name AS Application,
       a.security_classification AS SecurityLevel,
       a.data_sensitivity AS DataSensitivity,
       a.compliance_requirements AS ComplianceReqs,
       a.criticality AS Criticality,
       a.environment AS Environment
ORDER BY
  CASE a.security_classification
    WHEN 'restricted' THEN 1
    WHEN 'confidential' THEN 2
    ELSE 3
  END,
  CASE a.data_sensitivity
    WHEN 'high' THEN 1
    WHEN 'medium' THEN 2
    ELSE 3
  END
```

### Compliance Requirements Distribution

```cypher
MATCH (a:Application)
WHERE a.compliance_requirements IS NOT NULL
WITH split(a.compliance_requirements, ',') AS requirements, a
UNWIND requirements AS requirement
WITH trim(requirement) AS req, count(a) AS appCount, collect(a.name) AS apps
RETURN req AS ComplianceRequirement,
       appCount AS ApplicationCount,
       apps AS Applications
ORDER BY appCount DESC
```

## Lifecycle Management

### Applications Approaching End of Life

```cypher
MATCH (a:Application)
WHERE a.end_of_life_date IS NOT NULL
   AND date(a.end_of_life_date) < date() + duration({years: 1})
RETURN a.name AS Application,
       a.end_of_life_date AS EndOfLife,
       a.annual_cost AS Cost,
       a.criticality AS Criticality,
       a.user_count AS Users
ORDER BY a.end_of_life_date
```

### License Renewal Calendar

```cypher
MATCH (a:Application)
WHERE a.renewal_date IS NOT NULL
   AND date(a.renewal_date) < date() + duration({months: 6})
RETURN a.name AS Application,
       a.renewal_date AS RenewalDate,
       a.annual_cost AS Cost,
       a.license_type AS LicenseType,
       a.vendor_name AS Vendor
ORDER BY a.renewal_date
```

## Technology Stack Analysis

### Platform Distribution

```cypher
MATCH (a:Application)
WHERE a.platform IS NOT NULL
RETURN a.platform AS Platform,
       count(*) AS ApplicationCount,
       sum(a.annual_cost) AS TotalCost,
       round(avg(a.annual_cost)) AS AvgCost,
       collect(a.name)[0..5] AS SampleApps
ORDER BY ApplicationCount DESC
```

### Programming Language Ecosystem

```cypher
MATCH (a:Application)
WHERE a.programming_language IS NOT NULL
RETURN a.programming_language AS Language,
       count(*) AS AppCount,
       sum(a.annual_cost) AS TotalInvestment,
       avg(a.user_count) AS AvgUserCount
ORDER BY AppCount DESC
```

## Recommendation and Discovery Queries

### Find Similar Applications

```cypher
MATCH (a1:Application)-[:BELONGS_TO]->(c:Category)<-[:BELONGS_TO]-(a2:Application)
MATCH (a1)-[:SUPPLIED_BY]->(v:Vendor)<-[:SUPPLIED_BY]-(a2)
WHERE a1 <> a2
OPTIONAL MATCH (a1)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(a2)
RETURN a1.name as app1, a2.name as app2,
       count(DISTINCT c) + count(DISTINCT v) + count(DISTINCT e) as similarity_score
ORDER BY similarity_score DESC
```

### Consolidation Opportunities

```cypher
MATCH (a1:Application)-[:BELONGS_TO]->(c:Category)<-[:BELONGS_TO]-(a2:Application)
WHERE a1 <> a2 AND a1.in_use = true AND a2.in_use = true
RETURN c.name as category, collect(a1.name) as applications, count(*) as app_count
HAVING app_count > 2
ORDER BY app_count DESC
```

## SQL vs Cypher Comparison Examples

### Example 1: Finding Shared Dependencies

**SQL Approach (Complex)**:

```sql
WITH app_dependencies AS (
    SELECT app_name,
           TRIM(value) as dependency
    FROM applications
    CROSS APPLY STRING_SPLIT(depends_on_apps, ',')
    WHERE depends_on_apps IS NOT NULL
),
shared_deps AS (
    SELECT dependency, COUNT(*) as app_count
    FROM app_dependencies
    GROUP BY dependency
    HAVING COUNT(*) > 1
)
SELECT sd.dependency, sd.app_count,
       STRING_AGG(ad.app_name, ', ') as dependent_apps
FROM shared_deps sd
JOIN app_dependencies ad ON sd.dependency = ad.dependency
GROUP BY sd.dependency, sd.app_count
ORDER BY sd.app_count DESC;
```

**Cypher Approach (Simple)**:

```cypher
MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)<-[:DEPENDS_ON]-(other:Application)
WHERE a <> other
RETURN e.name as shared_dependency,
       collect(DISTINCT a.name) as dependent_apps,
       count(DISTINCT a) as app_count
ORDER BY app_count DESC
```

### Example 2: Finding Applications 2 Degrees Away

**SQL Approach**:

```sql
-- Requires complex recursive CTE with string parsing
WITH RECURSIVE dependency_chain AS (
    SELECT a1.app_name as source_app,
           TRIM(dep.value) as intermediate_app,
           a2.app_name as target_app,
           1 as depth
    FROM applications a1
    CROSS APPLY STRING_SPLIT(a1.depends_on_apps, ',') dep
    JOIN applications a2 ON TRIM(dep.value) = a2.app_name
    WHERE a1.depends_on_apps IS NOT NULL

    UNION ALL

    SELECT dc.source_app,
           dc.target_app as intermediate_app,
           TRIM(dep2.value) as target_app,
           dc.depth + 1
    FROM dependency_chain dc
    JOIN applications a ON dc.target_app = a.app_name
    CROSS APPLY STRING_SPLIT(a.depends_on_apps, ',') dep2
    WHERE dc.depth < 2 AND a.depends_on_apps IS NOT NULL
)
SELECT source_app, target_app, depth
FROM dependency_chain
WHERE depth = 2;
```

**Cypher Approach**:

```cypher
MATCH (a:Application)-[:DEPENDS_ON*2]->(target:ExternalApp)
RETURN a.name as source_app, target.name as target_app
```

## Advanced Pattern Queries

### Impact Analysis for Application Removal

```cypher
// Comprehensive impact analysis for removing an application
MATCH (target:Application {name: "Gmail"})
OPTIONAL MATCH (target)<-[:DEPENDS_ON]-(dependent:Application)
OPTIONAL MATCH (target)<-[:INTEGRATES_WITH]-(integrated:Application)
OPTIONAL MATCH (target)-[:BELONGS_TO]->(category:Category)<-[:BELONGS_TO]-(alternative:Application)
WHERE alternative <> target
RETURN
    target.name AS TargetApplication,
    collect(DISTINCT dependent.name) AS DependentApps,
    collect(DISTINCT integrated.name) AS IntegratedApps,
    collect(DISTINCT alternative.name) AS PotentialAlternatives
```

### Cross-Department Vendor Analysis

```cypher
MATCH (v:Vendor)<-[:SUPPLIED_BY]-(a:Application)-[:OWNED_BY]->(d:Department)
RETURN v.name as vendor, d.name as department, count(a) as app_count
ORDER BY app_count DESC
LIMIT 15
```

### SLA vs Criticality Mismatch Analysis

```cypher
MATCH (a:Application)
WHERE a.uptime_sla IS NOT NULL AND a.criticality IS NOT NULL
WITH a,
     CASE a.criticality
       WHEN 'critical' THEN 99.99
       WHEN 'high' THEN 99.9
       WHEN 'medium' THEN 99.5
       WHEN 'low' THEN 99.0
       ELSE 99.0
     END AS expectedSLA
WHERE a.uptime_sla < expectedSLA
RETURN a.name AS Application,
       a.criticality AS Criticality,
       a.uptime_sla AS CurrentSLA,
       expectedSLA AS ExpectedSLA,
       round(expectedSLA - a.uptime_sla, 2) AS SLAGap,
       a.annual_cost AS Cost
ORDER BY SLAGap DESC
```

## Visualization Queries

### Complete Application Ecosystem View

```cypher
MATCH (a:Application)-[r]-(n)
WHERE a.name CONTAINS 'Miro' // Replace with any app name
RETURN a, r, n
LIMIT 50
```

### Department Application Landscape

```cypher
MATCH (d:Department)<-[:USED_BY]-(a:Application)-[r]-(other)
WHERE d.name CONTAINS 'Medical' // Replace with department name
RETURN d, a, r, other
LIMIT 100
```

### Critical Application Network

```cypher
MATCH (a:Application)-[r]-(other)
WHERE a.criticality IN ['critical', 'high']
RETURN a, r, other
LIMIT 200
```

## Performance Tips

### Using Indexes

```cypher
// Check existing indexes
SHOW INDEXES

// Create additional indexes if needed
CREATE INDEX app_name_index FOR (a:Application) ON (a.name)
CREATE INDEX vendor_name_index FOR (v:Vendor) ON (v.name)
```

### Query Optimization

```cypher
// Use EXPLAIN to analyze query performance
EXPLAIN MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)
RETURN a.name, e.name

// Use PROFILE for detailed performance analysis
PROFILE MATCH (a:Application)-[:DEPENDS_ON]->(e:ExternalApp)
RETURN a.name, e.name
```

## Common Query Patterns

### Pattern Matching with Optional Relationships

```cypher
MATCH (a:Application)
OPTIONAL MATCH (a)-[:DEPENDS_ON]->(dep:ExternalApp)
OPTIONAL MATCH (a)-[:INTEGRATES_WITH]->(int:ExternalApp)
RETURN a.name,
       collect(DISTINCT dep.name) AS dependencies,
       collect(DISTINCT int.name) AS integrations
```

### Conditional Logic in Queries

```cypher
MATCH (a:Application)
RETURN a.name,
       CASE
         WHEN a.annual_cost > 100000 THEN 'High Cost'
         WHEN a.annual_cost > 50000 THEN 'Medium Cost'
         ELSE 'Low Cost'
       END AS cost_category
```

### Aggregation with Filtering

```cypher
MATCH (a:Application)
WHERE a.in_use = true
WITH a.category as category,
     count(a) as total_apps,
     sum(a.annual_cost) as total_cost
WHERE total_apps > 2
RETURN category, total_apps, total_cost
ORDER BY total_cost DESC
```

This query reference provides a comprehensive foundation for analyzing application portfolios using graph database capabilities. The examples demonstrate the power and simplicity of Cypher compared to equivalent SQL queries, especially for relationship-heavy analysis.
