# SI507_final
This is a Python Flask web application for movie recommendations. It allows users to search for movies based on different criteria such as 
director, actor, genre, and rating. The recommendations are generated using a dataset of movies and their ratings from different sources.

## APIKey
The yey of OMDB is stored in the file, so user could just simply run the si507_final_project.py to get IMDB top 250 the movies' information.
si507_final_project.py will first get the a list of movies's title from 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'. Then, it will use the title to
search the information from OMDB.

## Required Package
1. flask: Flask is a web framework for Python that allows you to build web applications
2. session: This is a Flask object that provides a way to store data across requests.
3. plotly.graph_objs: This is a package for creating interactive visualizations in Python. 
4. plotly.subplots: This is a package that provides tools for creating subplots.
5. bs4: This is a Python library for pulling data out of HTML file.

## Instruction
1. Run 'si507_final_project.py'
2. Run 'graph.py'
3. Open the browser and enter 'http://127.0.0.1:5000'
4. Have fun!

## Data Structure
The code defines four graphs, each based on a different movie criteria: director, actor, genre, and rating. Each graph is represented as a Python dictionary, with keys representing the category (e.g. director name or genre type) and values representing a list of movies that fit that category.

	The 'create_movie_graph' function is used to create the graphs, by iterating over the list of movies and extracting the relevant category information for each movie. For example, for the director graph, it iterates over the movies and extracts the director's name, then adds the movie to the list for that director's name in the graph dictionary. The resulting graph is then sorted by average rating using the 'get_rating' function and returned.

	The 'get_recommendations' function is used to generate a list of recommended movies based on the specified criteria (genre, director, actor, or rating). It first checks which criteria were specified, then iterates over the relevant graph dictionary and filters the movies based on the specified criteria. The resulting list of recommended movies is then returned.

	The data structure used for the graphs is a dictionary, where the keys represent the category (e.g. director name or genre type) and the values are lists of movies that fit that category.
