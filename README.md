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
