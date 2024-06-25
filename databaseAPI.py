import mariadb
import logging
from os import getenv
from dotenv import load_dotenv

from Table import Table, Row

# Load environment variables
load_dotenv()

USER_NAME = getenv("DB_USER")
PASSWORD = getenv("DB_PASS")
HOST = getenv("DB_HOST")

NAME_KEY = "Name"
DESCRIPTION_KEY = "Description"

def ResultstoPythonDictionary(cursor):
    # create a list of dictionary objects from the cursor
    # each dictionary object represents a row in the cursor
    # the keys are the column names and the values are the column values

    # get the column names from the cursor
    columnNames = [column[0] for column in cursor.description]
    return Table([Row(zip(columnNames, row)) for row in cursor.fetchall()])

# "from" and "by" are different
#   - "by" is used when the filtering column is of the same table
#   - "from" is used when the filtering column is from a different table
# and since I dont have some sort of weird API filter/sort-er, I've grouped them by "main" table

# region: Traits

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
    cur.callproc("uspGetTraitByMode", (gamemodeName,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

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
    cur.callproc("uspListTraits")

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

# endregion: Traits

# region: Gamemodes

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
    cur.callproc("uspGetGamemode", (gamemodeName,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    return results

def ListGamemodes():
    # connect to the database
    try:
        dbConnection = mariadb.connect(
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
    cur = dbConnection.cursor()

    # execute the query
    cur.callproc("uspListGameModes")

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    dbConnection.close()

    return results

# endregion: Gamemodes

# region: Items

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
    cur.callproc("uspGetItemByTrait", (trait,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

# endregion: Items

# region: Elections

def CastVote(userID, electionID, candidateID):
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
    cur.callproc("uspInsertDiscordUserElectionAssociation", (electionID, candidateID, userID))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def ChangeVote(electionID, newVote, userID):
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
    cur.callproc("uspUpdateDiscordUserElectionAssociation", (electionID, newVote, userID))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def CreateElection(guildID, neededVotes, isFraud = False, purpose = ""):
    # connect to the database
    try:
        conn = mariadb.connect(
            user=USER_NAME,
            password=PASSWORD,
            host=HOST,
            port=3306,
            database="s76587_WHEEL",
            autocommit=True
        )
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        return None

    # create a cursor
    cur = conn.cursor()

    # execute the query
    cur.callproc("uspInsertElection", (guildID, neededVotes, purpose, int(isFraud), 0))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def DeleteElection(electionID):
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
    cur.callproc("uspDeleteElection", (electionID,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def GetElectionByID(electionID):
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
    cur.callproc("uspGetElection", (electionID,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def GetElectionResults(electionID):
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
    cur.callproc("uspGetElectionResults", (electionID,))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

# endregion: Elections

# region: Aliases

def CreateAliasForUser(userID, guildID, alias):
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
    cur.callproc("uspInsertDiscordUserAlias", (userID, guildID, alias))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def GetAliasForUser(userID, guildID):
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
    cur.callproc("uspGetDiscordUserAlias", (userID, guildID))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def UpdateAlias(userID, guildID, alias):
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
    cur.callproc("uspUpdateDiscordUserAlias", (userID, guildID, alias))

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

# endregion: Aliases

def ListDifficulties():
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
    cur.callproc("uspListDifficulties")

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results

def ListMaps():
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
    cur.callproc("uspListMaps")

    # get the results
    results = ResultstoPythonDictionary(cur)

    # close the connection
    conn.close()

    return results