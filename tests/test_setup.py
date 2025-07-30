#!/usr/bin/env python3
"""
Setup Validation Script for Relational to Graph Database Migration Project

This script validates that all required components are properly installed
and configured for the project.

Usage: python test_setup.py
"""

import sys
import os
from pathlib import Path

def test_python_packages():
    """Test if all required Python packages are installed"""
    print("🔍 Testing Python packages...")

    required_packages = {
        'pandas': 'Data manipulation library',
        'faker': 'Fake data generation library',
        'neo4j': 'Neo4j Python driver',
        'sqlite3': 'SQLite database interface (built-in)',
        'dotenv': 'Environment variable loader'
    }

    failed_imports = []

    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description} (NOT FOUND)")
            failed_imports.append(package)

    if failed_imports:
        print(f"\n❌ Missing packages: {', '.join(failed_imports)}")
        if 'sqlite3' in failed_imports:
            print("   Note: sqlite3 should be included with Python. Try reinstalling Python.")
        else:
            print(f"   Install with: pip install {' '.join(failed_imports)}")
        return False
    else:
        print("✅ All Python packages are installed!")
        return True

def test_project_structure():
    """Test if project structure is correct"""
    print("\n🔍 Testing project structure...")

    required_dirs = ['scripts', 'sql', 'data', 'docs']
    required_files = [
        'sql/applications.sql',
        'scripts/generate_data.py',
        'scripts/create_db.py',
        'scripts/migrate_to_neo4j.py',
        'scripts/neo4j_queries.py'
    ]

    current_dir = Path('.')
    all_good = True

    # Check directories
    for dir_name in required_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"   ✅ {dir_name}/ directory exists")
        else:
            print(f"   ❌ {dir_name}/ directory missing")
            all_good = False

    # Check files
    for file_path in required_files:
        file_full_path = current_dir / file_path
        if file_full_path.exists() and file_full_path.is_file():
            print(f"   ✅ {file_path} exists")
        else:
            print(f"   ❌ {file_path} missing")
            all_good = False

    if all_good:
        print("✅ Project structure is correct!")
    else:
        print("❌ Some project files/directories are missing!")

    return all_good

def test_neo4j_connection():
    """Test Neo4j connection"""
    print("\n🔍 Testing Neo4j connection...")

    try:
        from neo4j import GraphDatabase
        from dotenv import load_dotenv

        # Load environment variables
        load_dotenv()

        # Get connection details from environment variables
        NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

        print(f"   Attempting connection to: {NEO4J_URI}")
        print(f"   Using username: {NEO4J_USER}")

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            result = session.run("RETURN 'Connection successful!' as message")
            record = result.single()
            if record:
                message = record["message"]
                print(f"   ✅ {message}")

                # Test a simple query
                result = session.run("RETURN 1 as test_number")
                test_record = result.single()
                if test_record:
                    test_val = test_record["test_number"]
                    print(f"   ✅ Test query returned: {test_val}")

        driver.close()
        print("✅ Neo4j connection test passed!")
        return True

    except ImportError as e:
        if 'dotenv' in str(e):
            print("   ❌ python-dotenv package not installed")
            print("   Install with: pip install python-dotenv")
        else:
            print("   ❌ neo4j package not installed")
        return False
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n   Troubleshooting tips:")
        print("   1. Make sure Neo4j is running (check Neo4j Desktop)")
        print("   2. Verify connection details in .env file (URI, username, password)")
        print("   3. Check if the database is started and active")
        print("   4. For Aura, use neo4j+s:// URI instead of bolt://")
        print("   5. Ensure .env file exists in the project root")
        return False

def test_sqlite_functionality():
    """Test SQLite functionality"""
    print("\n🔍 Testing SQLite functionality...")

    try:
        import sqlite3
        import tempfile
        import os

        # Create a temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            temp_db_path = tmp_file.name

        # Test database operations
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()

        # Create test table
        cursor.execute('''
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

        # Insert test data
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test_entry",))
        conn.commit()

        # Query test data
        cursor.execute("SELECT * FROM test_table")
        result = cursor.fetchone()

        conn.close()

        # Clean up
        os.unlink(temp_db_path)

        if result:
            print(f"   ✅ SQLite test passed - retrieved: {result}")
            print("✅ SQLite functionality working!")
            return True
        else:
            print("   ❌ SQLite test failed - no data retrieved")
            return False

    except Exception as e:
        print(f"   ❌ SQLite test failed: {e}")
        return False

def main():
    """Run all setup validation tests"""
    print("=" * 60)
    print("🚀 SETUP VALIDATION FOR RELATIONAL TO GRAPH DB PROJECT")
    print("=" * 60)

    tests = [
        test_python_packages,
        test_project_structure,
        test_sqlite_functionality,
        test_neo4j_connection
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    test_names = [
        "Python Packages",
        "Project Structure",
        "SQLite Functionality",
        "Neo4j Connection"
    ]

    for i, (test_name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! You're ready to run the project!")
        print("\nNext steps:")
        print("1. cd scripts")
        print("2. python generate_data.py")
        print("3. python create_db.py")
        print("4. python migrate_to_neo4j.py")
        print("5. python neo4j_queries.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above before proceeding.")

        if not results[3]:  # Neo4j connection failed
            print("\n💡 Neo4j connection tips:")
            print("- Make sure Neo4j Desktop is installed and running")
            print("- Create a database with appropriate password")
            print("- Update the .env file with correct connection details")
            print("- Check the Neo4j setup instructions in README.md")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
