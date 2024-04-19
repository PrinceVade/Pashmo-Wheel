import mariadb
import logging
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USER_NAME = getenv("DB_USER")
PASSWORD = getenv("DB_PASS")
HOST = getenv("DB_HOST")

GAMEMODE_NAME_KEY = "name"
GAMEMODE_DESCRIPTION_KEY = "description"

TRAIT_NAME_KEY = GAMEMODE_NAME_KEY
TRAIT_DESCRIPTION_KEY = GAMEMODE_DESCRIPTION_KEY

def ResultstoPythonDictionary(cursor):
    # create a list of dictionary objects from the cursor
    # each dictionary object represents a row in the cursor
    # the keys are the column names and the values are the column values

    # get the column names from the cursor
    columnNames = [column[0] for column in cursor.description]
    return [dict(zip(columnNames, row)) for row in cursor.fetchall()]

def ListTraits():
    # connect to the database
    try:
        conn = mariadb.connect(
            user=USER_NAME,
            password=PASSWORD,
            host=HOST,
            port=3306,
            database="s76587_WHEEL"
        )
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        return None

    # create a cursor
    cur = conn.cursor()

    # execute the query
    cur.callproc("get_traits")

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def ListGamemodes():
    # connect to the database
    try:
        conn = mariadb.connect(
            user=USER_NAME,
            password=PASSWORD,
            host=HOST,
            port=3306,
            database="s76587_WHEEL"
        )
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        return None

    # create a cursor
    cur = conn.cursor()

    # execute the query
    cur.callproc("get_gamemodes")

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def FetchGameModeByName(gamemodeName):
    try:
        conn = mariadb.connect(
            user=USER_NAME,
            password=PASSWORD,
            host=HOST,
            port=3306,
            database="s76587_WHEEL"
        )
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        return None
    
    # create a cursor
    cur = conn.cursor()

    # execute the query
    cur.callproc("get_gamemode_by_name", (gamemodeName,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    return results

def FetchTraitsForGamemode(gamemodeName):
    # connect to the database
    try:
        conn = mariadb.connect(
            user=USER_NAME,
            password=PASSWORD,
            host=HOST,
            port=3306,
            database="s76587_WHEEL"
        )
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        return None

    # create a cursor
    cur = conn.cursor()

    # execute the query
    cur.callproc("get_traits_for_mode", (gamemodeName,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def FetchItemsForTrait(trait):
    # connect to the database
    try:
        conn = mariadb.connect(
            user=USER_NAME,
            password=PASSWORD,
            host=HOST,
            port=3306,
            database="s76587_WHEEL"
        )
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        return None

    # create a cursor
    cur = conn.cursor()

    # execute the query
    cur.callproc("get_items_for_trait", (trait,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results