import requests

def search_movie(api_key, query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": query
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]
    else:
        print(f"Failed to retrieve data: {response.status_code} - {response.text}")
        return []

def add_movie(cnxn,cursor, movie_info, movie_id):
    try:
        ## Define insert statement
        cursor.execute(""" 
            SET IDENTITY_INSERT movie_info ON;
            INSERT INTO movie_info (
            movie_id, 
            original_language, 
            original_title, 
            overview,
            popularity,
            release_date,
            title           
            ) values (?, ?, ?, ?, ?, ?, ?)""", (
            movie_id,
            movie_info["original_language"],
            movie_info["original_title"],
            movie_info["overview"],
            movie_info["popularity"],
            movie_info["release_date"],
            movie_info["title"]
        ))

        ## Execute insert of data into database
        cnxn.commit()

    except Exception as e:
        print(f"An error occurred when inserting data: {str(e)}")

def add_movie_genre(cnxn,cursor, genre_id, movie_id):
    try:
        ## Define insert statement
        cursor.execute("""          
            INSERT INTO movie_genre (
            movie_id, 
            genre_id         
            ) values (?, ?)""", (
            movie_id,
            genre_id
        ))

        ## Execute insert of data into database
        cnxn.commit()

    except Exception as e:
        print(f"An error occurred when inserting data: {str(e)}")


def get_movie_credits(api_key, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['cast']
    else:
        print(f"Failed to retrieve data: {response.status_code} - {response.text}")
        return None

def add_cast(cnxn,cursor, cast_info, movie_id):
    try:
        ## Define insert statement
        cursor.execute(""" 
            INSERT INTO cast_info (
            movie_id, 
            name, 
            gender, 
            known_for_department,
            popularity,
            cast_id,
            character           
            ) values (?, ?, ?, ?, ?, ?, ?)""", (
            movie_id,
            cast_info["name"],
            cast_info["gender"],
            cast_info["known_for_department"],
            cast_info["popularity"],
            cast_info["cast_id"],
            cast_info["character"]
        ))

        ## Execute insert of data into database
        cnxn.commit()

    except Exception as e:
        print(f"An error occurred when inserting data: {str(e)}")