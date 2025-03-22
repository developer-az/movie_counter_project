# Movie Counter System

## Overview
This project is a movie counter system developed as part of the Development Monitors Internship Assignment. It tests basic Python and SQL skills by connecting to a PostgreSQL database, creating a table for movie records, and providing a terminal-based interface to add movies, update ticket counts, and book tickets.

## Project Requirements
- **Database Setup:**  
  - PostgreSQL to store movie records.
  - Create a table called `movies` with the following columns:
    - `id` (Primary Key, auto-increment integer)
    - `title` (Text, should be unique)
    - `tickets_available` (Integer)
- **Python Script:**  
  - Connect to your PostgreSQL database.
  - Functions:
    - Add a new movie to the database.
    - Update (increment) the ticket count for a movie.
    - Book movie tickets (decrease the count of tickets available).
    - Display all movies with their available ticket counts.
  - Terminal interface that allows a user to:
    - Add a movie.
    - Increment a movie’s ticket count.
    - List all movies.
    - Book a movie ticket.

## Repository Contents
- **main.py:** Contains the Python code that connects to the PostgreSQL database, creates the `movies` table (if it doesn't exist), and implements the movie counter system.
- **create_table.sql:** SQL script to create the `movies` table in the PostgreSQL database.
- **README.md:** This file, setup instructions and usage details.

## Getting Started Guide

### 1. First I Installed PostgreSQL
- **Download & Install:**  
  Downloading PostgreSQL from website,
- **Set a Password:**  
  And setting a password for the default `postgres` user. I chose "applecider".

### 2. Set Up the Database
- **Create the Database:**  
  Open the SQL Shell and run:
  ```sql
  CREATE DATABASE movie_db;
  ```
- **(option) Create the Table via SQL Script:**  
  To manually create the `movies` table using the provided SQL script:
  1. Open PowerShell.
  2. Set the PostgreSQL password as an environment variable (replace with your actual password):
     ```powershell
     $env:PGPASSWORD = "your_postgres_password"
     ```
  3. Run the SQL script using your full path to `psql.exe` ex.:
     ```powershell
     & "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d movie_db -f create_table.sql
     ```
  *Note:* The Python script (`main.py`) will also create the table if it doesn't exist. Running this script is optional but useful for verifying the schema.

### 3. Set Up the Python Environment
  In terminal:
- **Create a Virtual Environment:**
  ```bash
  python -m venv venv
  ```
- **Activate the Virtual Environment:**
  - On Windows PowerShell:
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
- **Install Dependencies:**
  ```bash
  pip install psycopg2-binary
  ```

### 4. Configure the Python Script
- **Check Database Connection Parameters:**  
  Open `main.py` and ensuring the connection parameters match your local setup:
  ```python
  conn = psycopg2.connect(
      dbname="movie_db",
      user="postgres",          # the default username
      password="applecider",     # your PostgreSQL password ("applecider" is my example)
      host="localhost"
  )
  ```

### 5. Run the Application
- With your virtual environment activated, run:
  ```bash
  python main.py
  ```
- **Use the Text-Based Menu in terminal:**  
  You will see a menu with the following options:
  ```
  Options:
  1. Add a movie
  2. Increment a movie's ticket count
  3. List all movies
  4. Book a movie ticket
  5. Exit
  ```
  Follow the on-screen prompts to:
  - **Add a Movie:** Select `1`, then enter the movie title and the number of available tickets.
  - **Increment Ticket Count:** Select `2`, then provide the movie title and the number of additional tickets.
  - **List All Movies:** Select `3` to view all movies and their current available tickets.
  - **Book a Ticket:** Select `4`, enter the movie title, and specify the number of tickets to book.
  - **Exit:** Select `5` to exit the program.

## Additional Notes:
- Python script automatically creates the `movies` table in psql database if it doesn't already exist.