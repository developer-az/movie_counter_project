import psycopg2
from psycopg2 import IntegrityError

# Connect to the PostgreSQL database
def connect_db():
    """
    Establish a connection to the PostgreSQL database.

    This function attempts to connect to a PostgreSQL database using
    the specified connection parameters. If the connection is successful,
    it returns the connection object; otherwise, it prints an error
    message and returns None.

    Returns:
        conn: The database connection object if successful, None otherwise.
    """

    try:
        conn = psycopg2.connect(
            dbname="movie_db",          # Your database name
            user="postgres",            # default 'postgres' username
            password="applecider",      # psql password set on installation
            host="localhost"            # Default host
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Create the movies table if it doesn't exist
def create_table(conn):
    """
    Create the movies table if it doesn't exist.

    This function creates a table named "movies" in the database if
    it doesn't already exist. The table has columns for the id, title
    and tickets available.

    Args:
        conn: The database connection object.
    """
    
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id SERIAL PRIMARY KEY,
                title TEXT UNIQUE,
                tickets_available INTEGER
            );
        """)
        conn.commit()

# Add a new movie to the database
def add_movie(conn, title, tickets_available):
    """
    Add a new movie to the database.

    This function adds a new movie to the movies table in the database
    with the specified title and number of tickets available. If the
    movie already exists in the database, it will print an error message
    indicating that the movie already exists.

    Args:
        conn: The database connection object.
        title: The title of the movie to be added.
        tickets_available: The number of tickets available for the movie.
    """
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO movies (title, tickets_available)
                VALUES (%s, %s)
            """, (title, tickets_available))
            conn.commit()
            print(f"Movie '{title}' added successfully.")
        except IntegrityError:
            conn.rollback()
            print(f"Movie '{title}' already exists.")

# Update the ticket count for a movie
def update_tickets(conn, title, additional_tickets):
    """
    Update the ticket count for a movie.

    This function adds the specified number of tickets to a movie's
    available ticket count. If the movie doesn't exist, it will print
    an error message indicating that the movie doesn't exist.

    Args:
        conn: The database connection object.
        title: The title of the movie for which tickets are to be updated.
        additional_tickets: The number of additional tickets to add to the movie's count.
    """
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE movies
            SET tickets_available = tickets_available + %s
            WHERE title = %s
        """, (additional_tickets, title))
        conn.commit()
        print(f"Updated '{title}' with {additional_tickets} additional tickets.")

# Book a movie ticket (decrease the ticket count)
def book_ticket(conn, title, num_tickets=1):
    """
    Book a specified number of tickets for a given movie.

    This function decreases the number of available tickets for a movie
    by the specified amount if enough tickets are available. It commits
    the changes to the database if successful, otherwise it prints an
    error message indicating the issue.

    Args:
        conn: The database connection object.
        title: The title of the movie for which tickets are to be booked.
        num_tickets: The number of tickets to book. Defaults to 1.
    """

    with conn.cursor() as cur:
        cur.execute("SELECT tickets_available FROM movies WHERE title = %s", (title,))
        result = cur.fetchone()
        if result:
            available = result[0]
            if available >= num_tickets:
                cur.execute("""
                    UPDATE movies
                    SET tickets_available = tickets_available - %s
                    WHERE title = %s
                """, (num_tickets, title))
                conn.commit()
                print("Ticket booked successfully.")
            else:
                print("Not enough tickets available.")
        else:
            print("Movie not found.")

def list_movies(conn):
    """
    List all movies and their available tickets.

    This function executes a SELECT query on the movies table to retrieve
    all movies and their available tickets. It then prints the results in a
    user-friendly format.

    Args:
        conn: The database connection object.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, tickets_available FROM movies")
        movies = cur.fetchall()
        print("\nMovies:")
        for movie in movies:
            print(f"ID: {movie[0]}, Title: {movie[1]}, Tickets Available: {movie[2]}")

# Main function for the text-based interface
def main():
    """
    Main function for the text-based interface.

    This function connects to the PostgreSQL database, creates the movies
    table if it doesn't exist, and provides a text-based menu to interact
    with the database. The user can add a movie, increment a movie's
    ticket count, list all movies, book a movie ticket, or exit the
    program.

    Args:
        None

    Returns:
        None
    """
    conn = connect_db()
    if conn is None:
        return

    create_table(conn)
    
    while True:
        print("\nOptions:")
        print("1. Add a movie")
        print("2. Increment a movie's ticket count")
        print("3. List all movies")
        print("4. Book a movie ticket")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter movie title: ")
            try:
                tickets = int(input("Enter number of tickets available: "))
            except ValueError:
                print("Invalid ticket number")
                continue
            add_movie(conn, title, tickets)
        
        elif choice == "2":
            title = input("Enter movie title: ")
            try:
                additional = int(input("Enter number of additional tickets: "))
            except ValueError:
                print("Invalid number")
                continue
            update_tickets(conn, title, additional)
        
        elif choice == "3":
            list_movies(conn)
        
        elif choice == "4":
            title = input("Enter movie title: ")
            try:
                num = int(input("Enter number of tickets to book: "))
            except ValueError:
                print("Invalid number")
                continue
            book_ticket(conn, title, num)
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice, please try again.")
    
    conn.close()

if __name__ == "__main__":
    main()
