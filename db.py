"""

"""

import sqlite3
from sqlite3 import Error
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


def create_connection(path: str) -> sqlite3.Connection:
    """

    """
    connection = None
    try:
        logger.info("creating sql database")
        connection = sqlite3.connect(path)
    except Error as e:
        logger.debug(e)

    return connection

def execute_query(connection: sqlite3.Connection, query:str) -> None:
    """

    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.info("running query")
    except Error as e:
        logger.debug(e)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


if __name__=="__main__":
    # connect
    conn = create_connection("sm_app.sqlite")

    # create table
    query = """
    CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  gender TEXT,
  nationality TEXT
);
    """
    execute_query(conn, query)

    # create entry
    create_users = """
    INSERT INTO
      users (name, age, gender, nationality)
    VALUES
      ('James', 25, 'male', 'USA'),
      ('Leila', 32, 'female', 'France'),
      ('Brigitte', 35, 'female', 'England'),
      ('Mike', 40, 'male', 'Denmark'),
      ('Elizabeth', 21, 'female', 'Canada');
    """

    execute_query(conn, create_users)


    # select records
    select_users = "SELECT * from users"
    users = execute_read_query(conn, select_users)

    for user in users:
        print(user)
