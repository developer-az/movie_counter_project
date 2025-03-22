import psycopg2
from psycopg2 import IntegrityError

# Connect to the PostgreSQL database
def connect_db():
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

# List all movies and their available tickets
def list_movies(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, tickets_available FROM movies")
        movies = cur.fetchall()
        print("\nMovies:")
        for movie in movies:
            print(f"ID: {movie[0]}, Title: {movie[1]}, Tickets Available: {movie[2]}")

# Main function for the text-based interface
def main():
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
