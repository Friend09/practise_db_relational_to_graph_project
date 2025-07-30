-- Applications Table Schema for Relational to Graph Database Learning Project
-- This table stores comprehensive information about applications in an organization
-- Designed to demonstrate relationships that can be explored in a graph database

CREATE TABLE applications (
    -- Primary identifier
    app_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Basic application information
    app_name VARCHAR(100) NOT NULL,
    app_description TEXT,
    app_version VARCHAR(20),
    
    -- Categorization (will create category relationships in graph)
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    
    -- Vendor information (will create vendor relationships)
    vendor_name VARCHAR(100) NOT NULL,
    vendor_contact_email VARCHAR(100),
    
    -- Ownership and management (will create team/person relationships)
    app_owner VARCHAR(100) NOT NULL,
    technical_lead VARCHAR(100),
    business_owner VARCHAR(100),
    department VARCHAR(50) NOT NULL,
    
    -- Financial information
    annual_cost DECIMAL(12,2),
    license_type VARCHAR(30), -- 'subscription', 'perpetual', 'open_source', 'freemium'
    cost_center VARCHAR(20),
    
    -- Usage and deployment information
    in_use BOOLEAN DEFAULT TRUE,
    user_count INTEGER,
    deployment_type VARCHAR(20), -- 'cloud', 'on_premise', 'hybrid'
    environment VARCHAR(20), -- 'production', 'staging', 'development'
    
    -- Technical specifications
    platform VARCHAR(30), -- 'web', 'desktop', 'mobile', 'api'
    programming_language VARCHAR(50),
    database_type VARCHAR(30),
    
    -- Dependencies (will create dependency relationships in graph)
    depends_on_apps TEXT, -- Comma-separated list of app_names this app depends on
    integrates_with_apps TEXT, -- Comma-separated list of app_names this app integrates with
    
    -- Compliance and security
    compliance_requirements TEXT, -- Comma-separated list like 'SOX', 'GDPR', 'HIPAA'
    security_classification VARCHAR(20), -- 'public', 'internal', 'confidential', 'restricted'
    data_sensitivity VARCHAR(20), -- 'low', 'medium', 'high', 'critical'
    
    -- Lifecycle information
    installation_date DATE,
    last_updated DATE,
    end_of_life_date DATE,
    renewal_date DATE,
    
    -- Performance and reliability
    uptime_sla DECIMAL(5,2), -- Service Level Agreement uptime percentage
    criticality VARCHAR(20), -- 'low', 'medium', 'high', 'critical'
    
    -- Additional metadata
    tags TEXT, -- Comma-separated tags for flexible categorization
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_applications_category ON applications(category);
CREATE INDEX idx_applications_vendor ON applications(vendor_name);
CREATE INDEX idx_applications_department ON applications(department);
CREATE INDEX idx_applications_app_owner ON applications(app_owner);
CREATE INDEX idx_applications_in_use ON applications(in_use);
CREATE INDEX idx_applications_criticality ON applications(criticality);

-- Create a view for active applications
CREATE VIEW active_applications AS
SELECT * FROM applications 
WHERE in_use = TRUE 
AND (end_of_life_date IS NULL OR end_of_life_date > CURRENT_DATE);


