
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_applications_data(num_records=50):
    data = []
    categories = ['Productivity', 'Communication', 'Design', 'Development', 'Finance', 'HR', 'Marketing', 'Sales', 'IT Operations', 'Security']
    subcategories = {
        'Productivity': ['Office Suite', 'Project Management', 'Note Taking', 'Task Management'],
        'Communication': ['Messaging', 'Video Conferencing', 'Email'],
        'Design': ['Graphic Design', 'Video Editing', 'CAD'],
        'Development': ['IDE', 'Version Control', 'CI/CD', 'Database Tool'],
        'Finance': ['Accounting', 'Expense Tracking', 'Payroll'],
        'HR': ['Recruitment', 'Performance Management', 'Onboarding'],
        'Marketing': ['CRM', 'Analytics', 'Social Media Management'],
        'Sales': ['CRM', 'Sales Enablement', 'E-commerce'],
        'IT Operations': ['Monitoring', 'Ticketing', 'Asset Management'],
        'Security': ['Antivirus', 'Firewall', 'MFA']
    }
    license_types = ['subscription', 'perpetual', 'open_source', 'freemium']
    deployment_types = ['cloud', 'on_premise', 'hybrid']
    environments = ['production', 'staging', 'development']
    platforms = ['web', 'desktop', 'mobile', 'api']
    database_types = ['PostgreSQL', 'MySQL', 'MongoDB', 'SQLite', 'Oracle', 'SQL Server', 'Neo4j']
    security_classifications = ['public', 'internal', 'confidential', 'restricted']
    data_sensitivities = ['low', 'medium', 'high', 'critical']
    criticalities = ['low', 'medium', 'high', 'critical']

    # Pre-define some common applications for dependencies and integrations
    common_apps = [
        'Gmail', 'Microsoft Teams', 'Slack', 'Zoom', 'Jira', 'Confluence', 'GitHub', 'GitLab',
        'Adobe Photoshop', 'Figma', 'Salesforce', 'SAP ERP', 'Workday', 'ServiceNow', 'Splunk',
        'Okta', 'Azure AD', 'AWS Console', 'Google Cloud Console', 'Postman', 'VS Code', 'Notion',
        'Asana', 'Trello', 'Miro', 'Tableau', 'Power BI', 'Google Analytics', 'Mailchimp'
    ]

    for i in range(num_records):
        app_name = fake.unique.company() + ' ' + fake.word().capitalize() + ' App'
        category = random.choice(categories)
        subcategory = random.choice(subcategories[category])
        vendor_name = fake.company()
        app_owner = fake.name()
        technical_lead = fake.name()
        business_owner = fake.name()
        department = fake.job().replace(' ', '_').capitalize() + ' Dept'

        installation_date = fake.date_between(start_date='-5y', end_date='today')
        last_updated = fake.date_between(start_date=installation_date, end_date='today')
        end_of_life_date = None
        if random.random() < 0.1: # 10% chance of being end-of-life
            end_of_life_date = fake.date_between(start_date='-1y', end_date='today')
        renewal_date = fake.date_between(start_date='today', end_date='+2y')

        # Generate dependencies and integrations
        num_depends = random.randint(0, 3)
        depends_on_apps = random.sample(common_apps, num_depends) if num_depends > 0 else []

        num_integrates = random.randint(0, 3)
        integrates_with_apps = random.sample(common_apps, num_integrates) if num_integrates > 0 else []

        # Ensure unique app names for dependencies/integrations
        depends_on_apps = [app for app in depends_on_apps if app != app_name]
        integrates_with_apps = [app for app in integrates_with_apps if app != app_name and app not in depends_on_apps]

        data.append({
            'app_id': i + 1,
            'app_name': app_name,
            'app_description': fake.sentence(),
            'app_version': f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            'category': category,
            'subcategory': subcategory,
            'vendor_name': vendor_name,
            'vendor_contact_email': fake.email(),
            'app_owner': app_owner,
            'technical_lead': technical_lead,
            'business_owner': business_owner,
            'department': department,
            'annual_cost': round(random.uniform(1000, 500000), 2),
            'license_type': random.choice(license_types),
            'cost_center': fake.bothify(text='CC####'),
            'in_use': fake.boolean(chance_of_getting_true=90),
            'user_count': random.randint(10, 5000) if random.random() < 0.8 else None, # 20% chance of null user count
            'deployment_type': random.choice(deployment_types),
            'environment': random.choice(environments),
            'platform': random.choice(platforms),
            'programming_language': random.choice(['Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'Rust', 'PHP', 'TypeScript', 'Swift', 'Kotlin']) if random.random() < 0.7 else None,
            'database_type': random.choice(database_types) if random.random() < 0.6 else None,
            'depends_on_apps': ','.join(depends_on_apps),
            'integrates_with_apps': ','.join(integrates_with_apps),
            'compliance_requirements': ','.join(random.sample(['SOX', 'GDPR', 'HIPAA', 'PCI DSS', 'ISO 27001'], random.randint(0, 3))),
            'security_classification': random.choice(security_classifications),
            'data_sensitivity': random.choice(data_sensitivities),
            'installation_date': installation_date.isoformat(),
            'last_updated': last_updated.isoformat(),
            'end_of_life_date': end_of_life_date.isoformat() if end_of_life_date else None,
            'renewal_date': renewal_date.isoformat(),
            'uptime_sla': round(random.uniform(99.0, 99.99), 2),
            'criticality': random.choice(criticalities),
            'tags': ','.join(fake.words(nb=random.randint(1, 5))),
            'notes': fake.paragraph(nb_sentences=2),
            'created_at': (datetime.now() - timedelta(days=random.randint(0, 365*5))).isoformat(),
            'updated_at': datetime.now().isoformat()
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_applications_data(num_records=100) # Generate 100 records
    df.to_csv('/home/ubuntu/relational_to_graph_project/data/applications.csv', index=False)
    print("Generated applications.csv with 100 records.")
