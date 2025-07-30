# Environment Configuration Update

## Overview

This project has been updated to use environment variables for all Neo4j connection details, making it easier to manage different configurations (local vs cloud) without modifying code files.

## Changes Made

### 1. Updated Scripts

All Python scripts now load configuration from a `.env` file:

- ✅ `scripts/migrate_to_neo4j.py` - Uses environment variables
- ✅ `scripts/neo4j_queries.py` - Uses environment variables
- ✅ `dev/migrate_to_neo4j.py` - Uses environment variables
- ✅ `dev/neo4j_queries.py` - Uses environment variables
- ✅ `tests/test_neo4j.py` - Uses environment variables
- ✅ `tests/test_setup.py` - Uses environment variables

### 2. New Files Added

- `.env.example` - Template for environment configuration
- This `ENVIRONMENT_UPDATE.md` file

### 3. Updated Documentation

- `README.md` updated with `.env` setup instructions
- All troubleshooting sections now reference `.env` file instead of manual script edits

## Setup Instructions

### 1. Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

### 2. Configure Your Environment

Edit the `.env` file with your actual Neo4j connection details:

```properties
# For Neo4j Desktop (local)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-actual-password

# For Neo4j Aura (cloud)
# NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your-generated-password

# SQLite database path
SQLITE_DB_PATH=/full/path/to/your/project/data/applications.db
```

### 3. Test Your Configuration

```bash
# Test Neo4j connection
python tests/test_neo4j.py

# Run full setup validation
python tests/test_setup.py
```

## Benefits

1. **Security**: Sensitive credentials are not stored in code files
2. **Flexibility**: Easy to switch between local and cloud configurations
3. **Consistency**: All scripts use the same configuration source
4. **Version Control**: `.env` file is in `.gitignore`, so credentials won't be committed

## Migration from Old Setup

If you were using the old setup with hardcoded credentials:

1. Create the `.env` file as described above
2. Your existing Neo4j connection will work with the new scripts
3. No need to modify any Python files manually anymore

## Troubleshooting

### Environment File Not Found

If you get errors about missing environment variables:

```bash
# Make sure .env file exists
ls -la .env

# If not, create it from the example
cp .env.example .env
```

### Connection Issues

1. Verify your `.env` file has the correct values
2. Ensure Neo4j is running (for local instances)
3. Test connection with: `python tests/test_neo4j.py`

### Path Issues

Make sure the `SQLITE_DB_PATH` in your `.env` file points to the correct location:

```properties
# Use absolute paths
SQLITE_DB_PATH=/Users/your-username/path/to/project/data/applications.db
```

## Environment Variables Reference

| Variable         | Description             | Example                         |
| ---------------- | ----------------------- | ------------------------------- |
| `NEO4J_URI`      | Neo4j connection URI    | `bolt://localhost:7687`         |
| `NEO4J_USER`     | Neo4j username          | `neo4j`                         |
| `NEO4J_PASSWORD` | Neo4j password          | `your-password`                 |
| `SQLITE_DB_PATH` | Path to SQLite database | `/path/to/data/applications.db` |

## Testing

After setup, run these tests to verify everything works:

```bash
# Test 1: Environment loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Neo4j URI:', os.getenv('NEO4J_URI'))"

# Test 2: Neo4j connection
python tests/test_neo4j.py

# Test 3: Full validation
python tests/test_setup.py
```

All tests should pass ✅
