import sqlite3
DB_LOC = "SRDB.sqlite"

def createTables(file):
    conn = getDBConnector(file)
    c = conn.cursor()
    artists(c)
    albums(c)
    songs(c)
    artist_album(c)
    conn.close()

def artists(cursor):
    cursor.execute("""CREATE TABLE Artist (ArtistID INTEGER PRIMARY KEY AUTOINCREMENT,
                           ArtistName VARCHAR(100) NOT NULL);""")

def albums(cursor):
    cursor.execute("""CREATE TABLE Album (AlbumID INTEGER PRIMARY KEY AUTOINCREMENT,
                           AlbumName VARCHAR(100) NOT NULL,
                           Link VARCHAR(200));""")

def songs(cursor):
    cursor.execute("""CREATE TABLE Song (SID INTEGER PRIMARY KEY AUTOINCREMENT,
                           SongTitle VARCHAR(30) NOT NULL,
                           Length DATETIME,
                           Artist  INTEGER NOT NULL,
                           Album  INTEGER NOT NULL,
                           Playable INTEGER NOT NULL,
                           PlayCount INTEGER NOT NULL,
                           Link VARCHAR(200));""")

def artist_album(cursor):
    cursor.execute("""CREATE TABLE ArtistAlbum(
                           ArtistID INTEGER,
                           AlbumID INTEGER,
                           FOREIGN KEY(ArtistID) REFERENCES Artist(ArtistID),
                           FOREIGN KEY(AlbumID) REFERENCES Album(AlbumID),
                           PRIMARY KEY (ArtistID, AlbumID));
                           """)

def addArtist(name):
    conn = getDBConnector(DB_LOC)
    cursor = conn.cursor()

    insert_query = """INSERT INTO Artist VALUES (Null, ?);"""
    cursor.execute(insert_query, [name])

    conn.commit()
    conn.close()

def addAlbum(name, link, artist):
    conn = getDBConnector(DB_LOC)
    cursor = conn.cursor()

    fetch_query = """SELECT ArtistID FROM Artist WHERE ArtistName = ?;"""
    ArtistID = cursor.execute(fetch_query, [artist]).fetchall()[0][0]

    insert_query = """INSERT INTO Album VALUES (Null, ?, ?);"""
    cursor.execute(insert_query, [name, link])

    fetch_query = """SELECT AlbumID FROM Album WHERE AlbumName = ?;"""
    AlbumID = cursor.execute(fetch_query, [name]).fetchall()[0][0]

    query = """INSERT INTO ArtistAlbum VALUES (?,?);"""
    cursor.execute(query, [ArtistID, AlbumID])

    conn.commit()
    conn.close()

def addSong(name, length, artist, album, playable, playCount, link):
    conn = getDBConnector(DB_LOC)
    cursor = conn.cursor()

    fetch_query = """SELECT ArtistID FROM Artist WHERE ArtistName = ?;"""
    ArtistID = cursor.execute(fetch_query, [artist]).fetchall()[0][0]
    fetch_query = """SELECT AlbumID FROM Album WHERE AlbumName = ?;"""
    AlbumID = cursor.execute(fetch_query, [album]).fetchall()[0][0]

    insert_query = """INSERT INTO Song VALUES (Null, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(insert_query, [name, length, ArtistID, AlbumID, playable, playCount, link])
    conn.commit()
    conn.close()

def getDBConnector(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        return conn

if __name__ == "__main__":
    createTables(DB_LOC)
