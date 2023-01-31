import sqlite3


# Debug; Test database connection.
def testdb():
    try:
        successmessage = "db connection works"
        errormessage = "db connection is not working"
        versionmessage = "SQLite version is {}"
        closemessage = "db connection closed"
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        print(f"{successmessage}")
        query = 'select sqlite_version();'
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"{versionmessage}".format(result))
        cursor.close()
    except sqlite3.Error as error:
        print(f"{errormessage}", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print(f"{closemessage}")
