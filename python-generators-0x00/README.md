# ALX Backend Python - Python Generators Project

## Project Overview

This project is part of the ALX Backend Python curriculum and demonstrates database operations using Python and MySQL. It implements a complete database seeding system that creates a MySQL database, defines a user data table, and populates it with sample user information from a CSV file. It also demonstrates the use of Python generators for efficient data streaming and batch processing.

## Project Objectives

- Learn how to connect to MySQL databases using Python
- Understand database creation and table schema design
- Implement data insertion with duplicate prevention
- Work with CSV file parsing and data validation
- Practice using Python generators and database operations
- Understand generator functions and the `yield` keyword for memory-efficient data streaming
- Implement batch processing for large datasets
- Implement lazy pagination for efficient data retrieval
- Implement memory-efficient aggregation using generators

## Features

- **Database Connection**: Establishes connections to MySQL server and specific databases
- **Database Creation**: Automatically creates the `ALX_prodev` database if it doesn't exist
- **Table Management**: Creates a `user_data` table with proper schema and indexing
- **Data Insertion**: Reads user data from CSV and inserts it into the database with duplicate prevention
- **UUID Generation**: Automatically generates unique identifiers for each user
- **Generator Streaming**: Efficiently streams database rows one at a time using Python generators
- **Batch Processing**: Processes large datasets in configurable batches with filtering capabilities
- **Lazy Pagination**: Retrieves data in pages on-demand for efficient memory usage
- **Memory-Efficient Aggregation**: Calculates aggregate functions without loading entire datasets into memory
- **Error Handling**: Comprehensive error handling for database operations

## Project Structure

```
.
├── seed.py # Main database seeding module with all functions
├── 0-main.py # Test script demonstrating the complete workflow
├── 0-stream_users.py # Generator function for streaming users from database
├── 1-main.py # Test script demonstrating the generator
├── 1-batch_processing.py # Batch processing with generators and filtering
├── 2-main.py # Test script for batch processing
├── 2-lazy_paginate.py # Lazy pagination with generators
├── 3-main.py # Test script for lazy pagination
├── 4-stream_ages.py # Memory-efficient aggregation with generators
├── 5-main.py # Test script for aggregation
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

### 0-stream_users.py

Generator function that efficiently streams user records from the database:

- **`stream_users()`**: A generator function that yields user records one at a time
  - Uses the `yield` keyword for memory-efficient data streaming
  - Connects to the database, executes a SELECT query, and yields each row as a dictionary
  - Automatically closes the cursor and connection after all rows are yielded
  - Returns: Generator object that yields dictionaries with `user_id`, `name`, `email`, and `age`

### 1-main.py

Test script that demonstrates the generator functionality:

- Uses `itertools.islice()` to fetch and print the first 6 users from the database
- Shows how to iterate over the generator without loading all data into memory
- Demonstrates the memory efficiency of generators for large datasets

### 1-batch_processing.py

Batch processing module with two generator functions:

- **`stream_users_in_batches(batch_size)`**: A generator that fetches users in configurable batches
  - Connects to the database and fetches all users
  - Yields batches of the specified size as lists of dictionaries
  - Yields remaining records even if they don't fill a complete batch
  - Returns: Generator object that yields lists of user dictionaries
- **`batch_processing(batch_size)`**: Processes batches and filters users over age 25
  - Iterates through batches from `stream_users_in_batches()`
  - Filters users with age > 25
  - Prints each filtered user record
  - Demonstrates practical use of batch processing for data filtering

### 2-main.py

Test script for batch processing:

- Calls `batch_processing(50)` to process users in batches of 50
- Filters and displays only users over age 25
- Handles `BrokenPipeError` for piping output to other commands (e.g., `head`)

### 2-lazy_paginate.py

Lazy pagination module with two functions:

- **`paginate_users(page_size, offset)`**: Fetches a single page of users from the database
  - Parameters: `page_size` (number of users per page), `offset` (starting position)
  - Returns: List of user dictionaries for the requested page
  - Connects to the database, executes a SELECT query with LIMIT and OFFSET, and returns results
- **`lazy_pagination(page_size)`**: A generator that lazily loads pages one at a time
  - Uses the `yield` keyword to return pages as they are requested
  - Only fetches the next page when needed (lazy loading)
  - Starts at offset 0 and increments by page_size for each iteration
  - Stops when no more records are available
  - Returns: Generator object that yields lists of user dictionaries

### 3-main.py

Test script for lazy pagination:

- Calls `lazy_pagination(100)` to load users in pages of 100
- Iterates through each page and prints individual user records
- Handles `BrokenPipeError` for piping output to other commands (e.g., `head`)
- Demonstrates memory-efficient pagination for large datasets

### 4-stream_ages.py

Memory-efficient aggregation module with two functions:

- **`stream_user_ages()`**: A generator function that yields user ages one by one
  - Connects to the database and executes a SELECT query for ages only
  - Uses the `yield` keyword to return ages one at a time
  - Automatically closes the cursor and connection after all ages are yielded
  - Returns: Generator object that yields individual user ages
- **`average_age()`**: Calculates the average age without loading all data into memory
  - Uses the `stream_user_ages()` generator to iterate through ages
  - Maintains only a running total and count in memory
  - Returns: Float representing the average age, or None if no users exist
  - Demonstrates memory-efficient aggregation for large datasets

### 5-main.py

Test script for memory-efficient aggregation:

- Calls `average_age()` to calculate the average age of all users
- Prints the result in the format: "Average age of users: {average_age}"
- Demonstrates how to use generators for computing aggregate functions efficiently

### Using Memory-Efficient Aggregation in Your Code

```python
from 4-stream_ages import stream_user_ages, average_age

# Calculate average age

avg = average_age()
print(f"Average age: {avg}")

# Or manually iterate through ages

total = 0
count = 0
for age in stream_user_ages():
total += age
count += 1

manual_avg = total / count if count > 0 else 0
print(f"Manual average: {manual_avg}")
```

### Using Lazy Pagination in Your Code

```python
from 2-lazy_paginate import lazy_pagination

# Paginate through all users in pages of 50

for page in lazy_pagination(50):
print(f"Processing page with {len(page)} users")
for user in page:
print(user)

# Paginate through users in pages of 100

for page in lazy_pagination(100):
for user in page:
if user['age'] > 30:
print(user)
```

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

### Python Generators

Generators are functions that use the `yield` keyword to return values one at a time. They are memory-efficient because they don't load all data into memory at once. Instead, they generate values on-the-fly as you iterate over them. This is especially useful for large datasets.

**Benefits of Generators:**

- Memory efficient: Only one item is in memory at a time
- Lazy evaluation: Values are computed only when needed
- Cleaner code: More readable than manual iteration with cursors

### Batch Processing

Batch processing divides large datasets into smaller, manageable chunks. This approach is useful for:

- Processing large datasets without loading everything into memory
- Applying filters or transformations to groups of records
- Improving performance when working with external APIs or services
- Reducing database load by fetching data in controlled amounts

The `stream_users_in_batches()` function demonstrates how to efficiently fetch and yield batches of records, while `batch_processing()` shows how to apply filtering logic to each batch.

### Lazy Pagination

Lazy pagination retrieves data in pages on-demand, which is useful for:

- Handling large datasets without loading everything into memory
- Efficiently managing memory usage
- Improving performance by fetching data in smaller chunks

The `paginate_users()` function fetches a single page of users, while `lazy_pagination()` yields pages one at a time as needed.

### Memory-Efficient Aggregation

Memory-efficient aggregation computes aggregate functions (like average, sum, count) without loading the entire dataset into memory. This is achieved by:

- Using generators to stream individual values one at a time
- Maintaining only running totals and counts in memory
- Processing values as they arrive from the database

The `stream_user_ages()` generator yields ages one at a time, while `average_age()` computes the average using only a running total and count, making it suitable for datasets with millions of records.

### Error Handling

All database operations include try-except blocks to catch and report errors gracefully, making debugging easier.

### Connection Management

The module provides separate functions for connecting to the MySQL server and the specific database, allowing flexibility in database operations.

## Example Output

When you run \`0-main.py\`, you should see output similar to:

```
Database ALX_prodev created successfully
connection successful
Table user_data created successfully
Data from user_data.csv inserted successfully
Database ALX_prodev is present
[('uuid-1', 'Johnnie Mayer', 'Ross.Reynolds21@hotmail.com', 35), ...]
```

When you run \`1-main.py\`, you should see output similar to:

```
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
{'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}
{'user_id': '00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'name': 'Ronnie Bechtelar', 'email': 'Sandra19@yahoo.com', 'age': 22}
{'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102}
{'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}
```

When you run \`2-main.py\`, you should see output similar to:

```
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
{'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}
{'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102}
{'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}
```

When you run \`3-main.py\`, you should see output similar to:

```
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
{'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}
{'user_id': '00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'name': 'Ronnie Bechtelar', 'email': 'Sandra19@yahoo.com', 'age': 22}
{'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102}
{'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}
```

When you run \`5-main.py\`, you should see output similar to:

```
Average age of users: 67.42
```

## Troubleshooting

### Connection Error

- Ensure MySQL Server is running
- Check that the host, user, and password are correct in the connection functions
- Verify that port 3306 is accessible

### File Not Found Error

- Ensure \`user_data.csv\` is in the same directory as the Python scripts
- Check the file path in the \`insert_data()\` function call

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
- Python generators and the \`yield\` keyword
- Memory-efficient data streaming techniques
- Using \`itertools\` for advanced iteration patterns
- Batch processing for large datasets
- Filtering and transforming data in batches
- Lazy pagination for efficient data retrieval
- LIMIT and OFFSET in SQL queries for pagination
- Memory-efficient aggregation for computing aggregate functions
- Performance optimization for database operations

## License

This project is part of the ALX Backend Python curriculum.
