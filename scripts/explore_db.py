import sqlite3
import pandas as pd

def explore_database(db_path):
    """
    Explore the applications database to understand the data and relationships
    """
    conn = sqlite3.connect(db_path)

    print("=== DATABASE EXPLORATION ===\n")

    # Basic table info
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM applications")
    total_records = cursor.fetchone()[0]
    print(f"Total applications in database: {total_records}\n")

    # Load data into DataFrame for analysis
    df = pd.read_sql_query("SELECT * FROM applications", conn)

    # Basic statistics
    print("=== BASIC STATISTICS ===")
    print(f"Active applications: {df['in_use'].sum()}")
    print(f"Inactive applications: {len(df) - df['in_use'].sum()}")
    print(f"Average annual cost: ${df['annual_cost'].mean():.2f}")
    print(f"Total annual cost: ${df['annual_cost'].sum():.2f}")
    print(f"Applications with dependencies: {df[df['depends_on_apps'] != ''].shape[0]}")
    print(f"Applications with integrations: {df[df['integrates_with_apps'] != ''].shape[0]}\n")

    # Category distribution
    print("=== CATEGORY DISTRIBUTION ===")
    category_counts = df['category'].value_counts()
    for category, count in category_counts.items():
        print(f"{category}: {count}")
    print()

    # Vendor distribution (top 10)
    print("=== TOP 10 VENDORS ===")
    vendor_counts = df['vendor_name'].value_counts().head(10)
    for vendor, count in vendor_counts.items():
        print(f"{vendor}: {count}")
    print()

    # Department distribution
    print("=== DEPARTMENT DISTRIBUTION ===")
    dept_counts = df['department'].value_counts()
    for dept, count in dept_counts.items():
        print(f"{dept}: {count}")
    print()

    # Criticality distribution
    print("=== CRITICALITY DISTRIBUTION ===")
    crit_counts = df['criticality'].value_counts()
    for crit, count in crit_counts.items():
        print(f"{crit}: {count}")
    print()

    # License type distribution
    print("=== LICENSE TYPE DISTRIBUTION ===")
    license_counts = df['license_type'].value_counts()
    for license_type, count in license_counts.items():
        print(f"{license_type}: {count}")
    print()

    # Deployment type distribution
    print("=== DEPLOYMENT TYPE DISTRIBUTION ===")
    deploy_counts = df['deployment_type'].value_counts()
    for deploy_type, count in deploy_counts.items():
        print(f"{deploy_type}: {count}")
    print()

    # Analyze dependencies and integrations
    print("=== DEPENDENCY AND INTEGRATION ANALYSIS ===")

    # Count applications with dependencies
    apps_with_deps = df[df['depends_on_apps'] != '']
    print(f"Applications with dependencies: {len(apps_with_deps)}")

    # Count applications with integrations
    apps_with_integrations = df[df['integrates_with_apps'] != '']
    print(f"Applications with integrations: {len(apps_with_integrations)}")

    # Most common dependencies
    all_dependencies = []
    for deps in df['depends_on_apps']:
        if isinstance(deps, str) and deps.strip():
            all_dependencies.extend([dep.strip() for dep in deps.split(',')])

    if all_dependencies:
        dep_counts = pd.Series(all_dependencies).value_counts().head(10)
        print("\nMost common dependencies:")
        for dep, count in dep_counts.items():
            print(f"  {dep}: {count}")

    # Most common integrations
    all_integrations = []
    for integs in df['integrates_with_apps']:
        if isinstance(integs, str) and integs.strip():
            all_integrations.extend([integ.strip() for integ in integs.split(',')])

    if all_integrations:
        integ_counts = pd.Series(all_integrations).value_counts().head(10)
        print("\nMost common integrations:")
        for integ, count in integ_counts.items():
            print(f"  {integ}: {count}")

    print()

    # Sample records for inspection
    print("=== SAMPLE RECORDS ===")
    sample_apps = df.head(3)[['app_name', 'category', 'vendor_name', 'department', 'depends_on_apps', 'integrates_with_apps']]
    for idx, row in sample_apps.iterrows():
        print(f"App: {row['app_name']}")
        print(f"  Category: {row['category']}")
        print(f"  Vendor: {row['vendor_name']}")
        print(f"  Department: {row['department']}")
        print(f"  Dependencies: {row['depends_on_apps']}")
        print(f"  Integrations: {row['integrates_with_apps']}")
        print()

    conn.close()

if __name__ == "__main__":
    path = "/Users/vamsi_mbmax/Developer/VAM_Documents/01_vam_PROJECTS/LEARNING/proj_Databases/dev_proj_Databases/practise_db_relational_to_graph_project"

    db_path = f'{path}/data/applications.db'
    explore_database(db_path)
