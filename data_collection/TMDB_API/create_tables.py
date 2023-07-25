import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()
server = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password)
cursor = cnxn.cursor()


def delete_table(table_name):
    # Delete movie_info
    drop_table_query = f'DROP TABLE IF EXISTS {table_name};'
    cursor.execute(drop_table_query)
    cnxn.commit()


# Create a table to store the information
create_table_query = '''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='movie_info' and xtype='U')
BEGIN
    CREATE TABLE movie_info (
        movie_id INTEGER NOT NULL IDENTITY(1,1),
        original_language VARCHAR(2),
        original_title VARCHAR(255),
        overview TEXT,
        popularity FLOAT,
        release_date DATE,
        title VARCHAR(255),
        PRIMARY KEY (movie_id)
        )
    END
'''
cursor.execute(create_table_query)
cnxn.commit()

create_table_query = '''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='movie_genre' and xtype='U')
BEGIN
    CREATE TABLE movie_genre (
        id INTEGER NOT NULL IDENTITY(1,1),
        movie_id INTEGER,
        genre_id INTEGER,
        PRIMARY KEY (id)
        )
    END
'''

foreign_key_query = '''
ALTER TABLE movie_genre
ADD CONSTRAINT fk_movies_genre_id
FOREIGN KEY (movie_id)
REFERENCES movie_info (movie_id);
'''

cursor.execute(create_table_query)
cursor.execute(foreign_key_query)
cnxn.commit()


create_table_query = '''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='cast_info' and xtype='U')
BEGIN
    CREATE TABLE cast_info (
        id INTEGER NOT NULL IDENTITY(1,1),
        movie_id INTEGER,
        name VARCHAR(255),
        gender INTEGER,
        known_for_department VARCHAR(50),
        popularity FLOAT,
        cast_id INTEGER,
        character VARCHAR(255),
        PRIMARY KEY (id)
        )
        END
'''

foreign_key_query = '''
ALTER TABLE cast_info
ADD CONSTRAINT fk_movies_cast_id
FOREIGN KEY (movie_id)
REFERENCES movie_info (movie_id);
'''

cursor.execute(create_table_query)
cursor.execute(foreign_key_query)
cnxn.commit()
