# Import Python's built-in SQLite library.
# SQLite allows us to store data without installing a database server.
import sqlite3

# Path helps us define file locations that work across operating systems.
from pathlib import Path


# Define where the SQLite database file will be stored.
# The database will be called minidash.db and will live
# inside the main MiniDash project folder.
DB_PATH = Path(__file__).resolve().parent.parent / "minidash.db"


def get_connection():
    """
    Open a connection to the MiniDash SQLite database.
    Other parts of the application will use this function
    whenever they need to read or write database records.
    """

    # Connect to the database file.
    # SQLite automatically creates the file if it doesn't exist.
    connection = sqlite3.connect(DB_PATH)

    # Allow database rows to be accessed using column names.
    # Example: restaurant["name"] instead of restaurant[1].
    connection.row_factory = sqlite3.Row

    # Enable foreign key validation to protect related records.
    connection.execute("PRAGMA foreign_keys = ON")

    # Return the connection so other functions can use it.
    return connection


def initialize_database():
    """
    Create the four baseline MiniDash tables.

    IF NOT EXISTS prevents errors when the tables
    have already been created.
    """

    # Open the database connection.
    # The context manager commits changes when successful
    # and rolls back changes if an error occurs.
    with get_connection() as connection:

        # executescript allows multiple SQL statements
        # to be executed together.
        connection.executescript("""

            -- Store information about each restaurant.
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                cuisine TEXT NOT NULL,
                opens_at TEXT NOT NULL,
                closes_at TEXT NOT NULL,
                avg_prep_minutes INTEGER NOT NULL
            );

            -- Store food items belonging to restaurants.
            -- restaurant_id links each item to its restaurant.
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY,
                restaurant_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                price_cents INTEGER NOT NULL,
                FOREIGN KEY (restaurant_id)
                    REFERENCES restaurants(id)
            );

            -- Store customer orders.
            -- Status will later support Track C's tracking feature.
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                restaurant_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                total_cents INTEGER NOT NULL,
                address TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (restaurant_id)
                    REFERENCES restaurants(id)
            );

            -- Store individual items within each order.
            -- Each record connects an order with a menu item.
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                menu_item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id)
                    REFERENCES orders(id),
                FOREIGN KEY (menu_item_id)
                    REFERENCES menu_items(id)
            );

        """)


# Only execute this block when database.py is run directly.
# Importing database.py from another file won't automatically
# run database initialization.
if __name__ == "__main__":

    # Create the database tables.
    initialize_database()

    # Confirm that initialization completed.
    print("MiniDash database initialized successfully.")