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


def execute_query(connection: sqlite3.Connection, query:str) -> None:
    """

    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.info("running query")
        return 0
    except Error as e:
        logger.debug(e)
        raise e

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        raise e

def create_records(conn):
    logger.info("create records table")
    execute_query(conn, """
    CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT NOT NULL,
    amount INTEGER,
    date TEXT,
    description TEXT,
    category TEXT
    );
    """)

def create_connection(path: str) -> sqlite3.Connection:
    """

    """
    connection = None
    try:
        logger.info("creating sql database")
        connection = sqlite3.connect(path)
        create_records(connection)
    except Error as e:
        logger.debug(e)
        raise e

    return connection


def add_record(conn, chat_id, amount, date, description, category):
    logger.info(f"inserting {chat_id, amount, date, description, category}")
    execute_query(conn, f"""
    INSERT INTO records(chat_id, amount, date, description, category)
VALUES ("{chat_id}", {amount}, "{date}", "{description}", "{category}");
""")

def delete_record(conn, id):
    logger.info(f"deleting {id}")
    execute_query(conn, f"""
DELETE FROM records
WHERE id={id}
""")


if __name__=="__main__":
    # connect
    conn = create_connection("sm_app.sqlite")

    create_records(conn)
    add_record(conn, "james", 123, "today", "de", "cat")



    # select records
    select_users = "SELECT * from records"
    users = execute_read_query(conn, select_users)

    for user in users:
        print(user)

    delete_record(conn, 2)

    # select records
    select_users = "SELECT * from records"
    users = execute_read_query(conn, select_users)

    for user in users:
        print(user)
