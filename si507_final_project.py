import requests
import time
import json
from bs4 import BeautifulSoup
import pprint as pp


BASE_URL = 'http://www.omdbapi.com/'
IMDB_URL = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
CACHE_FILE_NAME = 'cache_final_1.json'
CACHE_DICT = {}
OMDB_key = '229fd03a'


def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache, indent=4)
    cache_file.write(contents_to_write)
    cache_file.close()


'''--------------------------------------'''

class MovieInfo:
    def __init__(self, movies):
        self.movies = movies

    def extract_info(self):
        # Loop through each movie dictionary and extract the relevant information
        extracted_info = []
        for movie in self.movies:
            extracted_movie_info = {}
            extracted_movie_info['title'] = movie.get('Title')
            extracted_movie_info['release_year'] = movie.get('Year')
            extracted_movie_info['rated'] = movie.get('Rated')
            extracted_movie_info['runtime'] = movie.get('Runtime')
            extracted_movie_info['genre'] = movie.get('Genre')
            extracted_movie_info['director'] = movie.get('Director')
            extracted_movie_info['actor'] = movie.get('Actors')
            extracted_movie_info['plot'] = movie.get('Plot')
            extracted_movie_info['rating'] = movie.get('Ratings')
            extracted_movie_info['poster'] = movie.get('Poster')
            extracted_movie_info['imdbID'] = movie.get('imdbID')
            extracted_info.append(extracted_movie_info)
        return extracted_info

        
def find_best_250(url, filename=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = []
    table = soup.find('table', {'class': 'chart full-width'})
    for row in table.find_all('tr')[1:]:
        title = row.find_all('td')[1].find('a').text
        titles.append(title)

    with open(filename, 'w') as f:
        json.dump(titles, f)

    return titles

top_250_titles = find_best_250(IMDB_URL, 'top_250_titles.json')
#print(top_250_titles)

with open('top_250_titles.json', 'r') as f:
    movies_data = json.load(f)

def top_movie_info(titles, api_key):
    movies = []
    url = 'omdbapi.com/?apikey=229fd03a&t=pulp+fiction'

    titles = [string.replace(' ', '+').lower() for string in titles]
    for title in titles:
        response = requests.get(f'http://omdbapi.com/?apikey={api_key}&t={title}')
        movie_info = json.loads(response.content)
        movies.append(movie_info)
    return movies
save_cache(top_movie_info(movies_data, OMDB_key))

#pp.pprint(top_movie_info(movies_data, OMDB_key)[0])
cache = load_cache()
top_250_info = top_movie_info(movies_data, OMDB_key)
movie_info = MovieInfo(top_250_info).extract_info()
print(movie_info)

save_cache(movie_info)




