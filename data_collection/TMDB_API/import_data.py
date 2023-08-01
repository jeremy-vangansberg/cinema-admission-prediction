import pyodbc
from dotenv import load_dotenv
import os
import requests
import time
from utils import *

load_dotenv()
server = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
api_key = os.getenv("API_KEY")

cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password)

cursor = cnxn.cursor()

try:
    ## Define insert statement
    cursor.execute(""" SELECT * FROM boxoffice """)

    # cursor.close()
    # cnxn.close()

except Exception as e:
    print(f"An error occurred when inserting data: {str(e)}")


req = False
i = 0
for movie in cursor.fetchall():
    i+=1
    if movie[1] == 'Le Prix à payer (2007)':
        req = True
        print(i)
    
    if req:
        if movie:
            print(movie[1])
            movie_result = search_movie(api_key, movie[1])
            add_movie(cnxn,cursor, movie_result, movie[0])
            if movie_result:
                for genre in movie_result['genre_ids']:
                    add_movie_genre(cnxn,cursor, genre, movie[0])
            
                movie_cast = get_movie_credits(api_key,movie_result['id'])
                for cast_member in movie_cast:
                    add_cast(cnxn,cursor, cast_member, movie[0])
