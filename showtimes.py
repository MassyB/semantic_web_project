import requests
from pprint import pprint
import re

showtimesApiKey = "RWODqc7MJFOHG7LBb32oKIaxE6OVOVQa"

def sendShowtimesApiRequest(url, verbose=False):
    try:
        response = requests.get(
            url=url,
            headers={
                "X-API-Key": showtimesApiKey,
            }
        )
        if verbose:
            print("Response HTTP Status Code: {status_code}".format(
                status_code=response.status_code))
            print("Response HTTP Response Body: \n")
            pprint(response.json())
            
        if response.status_code == requests.codes.ok:
            return response.json()
        return None
    
    except requests.exceptions.RequestException:
        if verbose: 
            print("HTTP Request failed")
        return None
        
def getTheatersCloseTo(position, distance):
    latitude = position["lat"]
    longitude = position["long"]
    url = "https://api.internationalshowtimes.com/v4/cinemas/?location={latitude},{longitude}&distance={distance}".format(
           latitude= latitude,longitude= longitude, distance= distance)
    theaters = sendShowtimesApiRequest(url, verbose=True)
    return theaters

def getMoviesPlayedInTheaters(theaters, category, verbose=False):
    
    movies = {}
    ## get the genres according to the category
    genresIds= getGenres(category)
    if genresIds:
        genreParam= ",".join(genresIds)
    else:
        if verbose:
            print("Request Failed for genres")
            return None
    url = "https://api.internationalshowtimes.com/v4/movies/?cinema_id={theaterId}&genre_ids="+genreParam
    for theater in theaters:
        moviesResponse = sendShowtimesApiRequest(url.format(theaterId= theater["id"]))
        if moviesResponse:
            theaterMovies = moviesResponse["movies"]
            for movie in theaterMovies:
                movies[movie["id"]] = movie
        else:
            print("Request failed for theater['id'] = \n" + str(theater["id"]) )
            if verbose: 
                pprint(theater)
    return list(movies.values())

def getGenres(category, verbose=False):
    url = "https://api.internationalshowtimes.com/v4/genres"
    genresIds= set()
    genrePattern = ".*"+category+".*"
    categoryRegEx = re.compile(genrePattern, re.IGNORECASE)
    genresResponse = sendShowtimesApiRequest(url)
    if genresResponse:
        genres = genresResponse["genres"]
        for genre in genres:
         
            if (genre["name"] is not None) and categoryRegEx.match(genre["name"]):
                genresIds.add(genre["id"])
        return genresIds
    else:
        if verbose:
            print("Request failed for genres")
        return None
            
        
    
            
        