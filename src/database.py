"""
MiniDash SQLite database setup.

This module creates the database tables, manages connections,
and adds sample restaurants and menu items.
"""

# Import libraries for database access and file paths.
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Define the default location of the SQLite database.
DEFAULT_DB = Path(__file__).resolve().parent.parent / "minidash.db"


@contextmanager
def get_connection():
    """
    Open a SQLite database connection.

    Automatically commit successful changes, roll back failed
    changes, and close the connection when finished.
    """

    # Allow tests to use a separate temporary database.
    connection = sqlite3.connect(
        os.getenv("MINIDASH_DB_PATH", str(DEFAULT_DB))
    )

    try:
        # Allow access to columns by name, such as row["name"].
        connection.row_factory = sqlite3.Row

        # Enforce foreign key relationships.
        connection.execute("PRAGMA foreign_keys = ON")

        # Make the database connection available to the caller.
        yield connection

        # Save successful database changes.
        connection.commit()

    except Exception:
        # Undo incomplete changes if an error occurs.
        connection.rollback()
        raise

    finally:
        # Always close the connection to prevent resource leaks.
        connection.close()


def initialize_database():
    """
    Create MiniDash's database tables if they do not exist.

    The first four tables support the baseline application.
    The fifth table stores the order tracking history.
    """

    with get_connection() as connection:

        # Execute SQL statements to create all five tables.
        connection.executescript("""

            -- Store restaurant details.
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                cuisine TEXT NOT NULL,
                opens_at TEXT NOT NULL,
                closes_at TEXT NOT NULL,
                avg_prep_minutes INTEGER NOT NULL
                    CHECK(avg_prep_minutes >= 0)
            );

            -- Store food items belonging to restaurants.
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY,
                restaurant_id INTEGER NOT NULL
                    REFERENCES restaurants(id),
                name TEXT NOT NULL,
                price_cents INTEGER NOT NULL
                    CHECK(price_cents >= 0)
            );

            -- Store customer orders and estimated arrival times.
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                restaurant_id INTEGER NOT NULL
                    REFERENCES restaurants(id),
                status TEXT NOT NULL,
                total_cents INTEGER NOT NULL
                    CHECK(total_cents >= 0),
                address TEXT NOT NULL,
                created_at TEXT NOT NULL,
                eta_at TEXT
            );

            -- Store the individual items within each order.
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL
                    REFERENCES orders(id),
                menu_item_id INTEGER NOT NULL
                    REFERENCES menu_items(id),
                quantity INTEGER NOT NULL
                    CHECK(quantity > 0)
            );

            -- Record every order status change with a timestamp.
            CREATE TABLE IF NOT EXISTS order_status_history (
                id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL
                    REFERENCES orders(id),
                status TEXT NOT NULL,
                changed_at TEXT NOT NULL
            );

        """)

        # Check whether an older database is missing the ETA column.
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(orders)")
        }

        # Upgrade older databases without deleting existing orders.
        if "eta_at" not in columns:
            connection.execute(
                "ALTER TABLE orders ADD COLUMN eta_at TEXT"
            )


def seed_restaurants():
    """
    Add five sample restaurants and their menus.

    This runs only if the restaurant table is empty,
    preventing duplicate sample records.
    """

    with get_connection() as connection:

        # Check whether restaurant records already exist.
        if connection.execute(
            "SELECT COUNT(*) FROM restaurants"
        ).fetchone()[0]:
            return

        # Restaurant ID, name, cuisine, hours, and preparation time.
        restaurants = [
            (1, "Little Napoli", "Italian", "11:00", "22:00", 25),
            (2, "Green Bowl", "Healthy", "10:00", "21:00", 15),
            (3, "Sushi Harbor", "Japanese", "12:00", "22:00", 30),
            (4, "Taco Corner", "Mexican", "11:00", "23:00", 20),
            (5, "Burger Station", "American", "11:00", "23:00", 18),
        ]

        # Insert all five restaurants.
        connection.executemany(
            "INSERT INTO restaurants VALUES (?,?,?,?,?,?)",
            restaurants
        )

        # Sample menu items.
        # Prices are stored in cents to avoid floating-point errors.
        items = [
            (1, 1, "Margherita Pizza", 1299),
            (2, 1, "Pasta Primavera", 1499),
            (3, 2, "Grain Bowl", 1099),
            (4, 2, "Garden Salad", 899),
            (5, 3, "Salmon Roll (Cooked)", 1399),
            (6, 3, "Miso Soup", 399),
            (7, 4, "Chicken Tacos", 1199),
            (8, 4, "Bean Burrito", 999),
            (9, 5, "Classic Burger", 1299),
            (10, 5, "Fries", 499),
        ]

        # Insert sample menu items into SQLite.
        connection.executemany(
            "INSERT INTO menu_items VALUES (?,?,?,?)",
            items
        )


# Execute these functions only when this file is run directly.
if __name__ == "__main__":

    # Create or upgrade the database tables.
    initialize_database()

    # Add sample restaurants and menu items.
    seed_restaurants()

    # Display a confirmation message.
    print("MiniDash database initialized and five restaurants seeded.")