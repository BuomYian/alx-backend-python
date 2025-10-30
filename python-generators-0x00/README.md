# ALX Backend Python - Python Generators Project

## Project Overview

This project is part of the ALX Backend Python curriculum and demonstrates database operations using Python and MySQL. It implements a complete database seeding system that creates a MySQL database, defines a user data table, and populates it with sample user information from a CSV file.

## Project Objectives

- Learn how to connect to MySQL databases using Python
- Understand database creation and table schema design
- Implement data insertion with duplicate prevention
- Work with CSV file parsing and data validation
- Practice using Python generators and database operations

## Features

- **Database Connection**: Establishes connections to MySQL server and specific databases
- **Database Creation**: Automatically creates the `ALX_prodev` database if it doesn't exist
- **Table Management**: Creates a `user_data` table with proper schema and indexing
- **Data Insertion**: Reads user data from CSV and inserts it into the database with duplicate prevention
- **UUID Generation**: Automatically generates unique identifiers for each user
- **Error Handling**: Comprehensive error handling for database operations

## Project Structure

```
.
├── seed.py # Main database seeding module with all functions
├── 0-main.py # Test script demonstrating the complete workflow
├── user_data.csv # Sample user data in CSV format
└── README.md # This file
```

## Files Description

### seed.py

The core module containing all database operations:

- **`connect_db()`**: Connects to the MySQL server on localhost
  - Returns: MySQL connection object or None on failure
- **`create_database(connection)`**: Creates the `ALX_prodev` database
  - Uses `CREATE DATABASE IF NOT EXISTS` to prevent errors if database already exists
- **`connect_to_prodev()`**: Connects directly to the `ALX_prodev` database
  - Returns: MySQL connection object or None on failure
- **`create_table(connection)`**: Creates the `user_data` table with the following schema:
  - `user_id` (VARCHAR(36), PRIMARY KEY): Unique identifier for each user
  - `name` (VARCHAR(255), NOT NULL): User's full name
  - `email` (VARCHAR(255), NOT NULL): User's email address
  - `age` (DECIMAL(3, 0), NOT NULL): User's age
  - Includes an index on `user_id` for faster queries
- **`insert_data(connection, csv_file)`**: Reads CSV file and inserts data into the table
  - Generates a unique UUID for each user
  - Checks for duplicate emails before inserting
  - Only inserts new records (prevents duplicates)

### 0-main.py

Test script that demonstrates the complete workflow:

1. Connects to MySQL server
2. Creates the `ALX_prodev` database
3. Connects to the newly created database
4. Creates the `user_data` table
5. Inserts data from `user_data.csv`
6. Verifies the database exists
7. Retrieves and displays the first 5 records

### user_data.csv

Sample data file containing 20 user records with the following columns:

- `name`: User's full name
- `email`: User's email address
- `age`: User's age

## Requirements

- Python 3.x
- MySQL Server (running on localhost)
- `mysql-connector-python` package

## Installation

1. Install the required Python package:

   ```bash
   pip install mysql-connector-python
   ```

2. Ensure MySQL Server is running on your system

3. Place all files in the same directory

## Usage

### Basic Usage

Run the main test script:

```bash
python3 0-main.py
```

This will:

- Create the database and table
- Insert all user data from the CSV file
- Display the first 5 records

### Using Individual Functions

```python
from seed import connect_db, create_database, connect_to_prodev, create_table, insert_data

# Step 1: Connect to MySQL server

connection = connect_db()

# Step 2: Create the database

create_database(connection)
connection.close()

# Step 3: Connect to the ALX_prodev database

connection = connect_to_prodev()

# Step 4: Create the table

create_table(connection)

# Step 5: Insert data from CSV

insert_data(connection, 'user_data.csv')

# Step 6: Query the data

cursor = connection.cursor()
cursor.execute("SELECT \* FROM user_data LIMIT 5")
rows = cursor.fetchall()
for row in rows:
print(row)

cursor.close()
connection.close()
```

## Database Schema

```sql
CREATE TABLE user_data (
user_id VARCHAR(36) PRIMARY KEY,
name VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
age DECIMAL(3, 0) NOT NULL,
INDEX idx_user_id (user_id)
);
```

## Key Features Explained

### UUID Generation

Each user is assigned a unique UUID (Universally Unique Identifier) using Python's `uuid` module. This ensures that even if the same user data is inserted multiple times, each record will have a unique identifier.

### Duplicate Prevention

The `insert_data()` function checks if an email already exists in the database before inserting. This prevents duplicate user records based on email addresses.

### Error Handling

All database operations include try-except blocks to catch and report errors gracefully, making debugging easier.

### Connection Management

The module provides separate functions for connecting to the MySQL server and the specific database, allowing flexibility in database operations.

## Example Output

When you run `0-main.py`, you should see output similar to:

```
Database ALX_prodev created successfully
connection successful
Table user_data created successfully
Data from user_data.csv inserted successfully
Database ALX_prodev is present
[('uuid-1', 'Johnnie Mayer', 'Ross.Reynolds21@hotmail.com', 35), ...]
```

## Troubleshooting

### Connection Error

- Ensure MySQL Server is running
- Check that the host, user, and password are correct in the connection functions
- Verify that port 3306 is accessible

### File Not Found Error

- Ensure `user_data.csv` is in the same directory as the Python scripts
- Check the file path in the `insert_data()` function call

### Permission Denied

- Ensure the MySQL user has permissions to create databases and tables
- Check MySQL user privileges

## Learning Outcomes

After completing this project, you will understand:

- How to establish database connections in Python
- SQL database and table creation
- Data insertion and validation techniques
- CSV file parsing and processing
- Error handling in database operations
- UUID generation for unique identifiers
- Duplicate prevention strategies

## License

This project is part of the ALX Backend Python curriculum.
