# Graph Database Model Design

## Overview
This document describes the graph model used to convert the relational applications table into a Neo4j knowledge graph. The model is designed to reveal relationships and patterns that are difficult to discover in traditional relational queries.

## Node Types

### 1. Application
Represents the main applications in the organization.

**Properties:**
- name (unique identifier)
- description
- version
- annual_cost
- license_type
- cost_center
- in_use
- user_count
- deployment_type
- environment
- platform
- programming_language
- database_type
- compliance_requirements
- security_classification
- data_sensitivity
- installation_date
- last_updated
- end_of_life_date
- renewal_date
- uptime_sla
- criticality
- tags
- notes

### 2. Category
Represents application categories and subcategories.

**Properties:**
- name (unique identifier)
- type ('main' or 'sub')

### 3. Vendor
Represents software vendors/suppliers.

**Properties:**
- name (unique identifier)
- contact_email

### 4. Department
Represents organizational departments.

**Properties:**
- name (unique identifier)

### 5. Person
Represents people involved with applications (owners, leads, managers).

**Properties:**
- name (unique identifier)

### 6. ExternalApp
Represents external applications that our applications depend on or integrate with.

**Properties:**
- name (unique identifier)

## Relationship Types

### 1. BELONGS_TO
- **From:** Application
- **To:** Category
- **Description:** Indicates which category an application belongs to

### 2. SUPPLIED_BY
- **From:** Application
- **To:** Vendor
- **Description:** Indicates which vendor supplies the application

### 3. OWNED_BY
- **From:** Application
- **To:** Department
- **Description:** Indicates which department owns the application

### 4. OWNS
- **From:** Person
- **To:** Application
- **Description:** Indicates the application owner

### 5. LEADS
- **From:** Person
- **To:** Application
- **Description:** Indicates the technical lead for the application

### 6. MANAGES
- **From:** Person
- **To:** Application
- **Description:** Indicates the business owner/manager of the application

### 7. DEPENDS_ON
- **From:** Application
- **To:** ExternalApp
- **Description:** Indicates dependency relationships between applications

### 8. INTEGRATES_WITH
- **From:** Application
- **To:** ExternalApp
- **Description:** Indicates integration relationships between applications

## Graph Model Benefits

### 1. Relationship Discovery
The graph model makes it easy to discover:
- Which applications share the same vendor
- Which departments have the most applications
- Which external applications are most commonly used
- Dependency chains and potential single points of failure
- Integration patterns across the organization

### 2. Pattern Analysis
The graph enables analysis of:
- Vendor consolidation opportunities
- Department-specific application preferences
- Technology stack patterns
- Compliance requirement clustering
- Cost optimization opportunities

### 3. Impact Analysis
The graph supports:
- Understanding the impact of removing an application
- Identifying applications that could be consolidated
- Finding alternative applications with similar functionality
- Analyzing the blast radius of vendor changes

## Example Queries

The graph model supports various analytical queries:

1. **Find all applications from a specific vendor**
2. **Identify the most critical dependencies**
3. **Discover applications with similar technology stacks**
4. **Find potential consolidation opportunities**
5. **Analyze department-specific application portfolios**
6. **Identify compliance requirement patterns**

This graph model transforms the flat relational data into a rich network of relationships that provides deeper insights into the application landscape.

