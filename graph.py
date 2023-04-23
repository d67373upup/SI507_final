import json
from flask import Flask, request, render_template, session
import plotly.graph_objs as go
from plotly.subplots import make_subplots


app = Flask(__name__)
app.secret_key = 'louzeyu'

def create_movie_graph(movies, criteria):
    graph = {}
    for movie in movies:
        try: 
            if criteria in movie:
                sub_movies = movie[criteria].split(", ")
                for sub_movie in sub_movies:
                    if sub_movie not in graph:
                        graph[sub_movie] = []
                    graph[sub_movie].append(movie)
        except:
            if movie[criteria] not in graph:
                graph[movie[criteria]] = []
            graph[movie[criteria]].append(movie)

    for cate, movie_list in graph.items():
        graph[cate] = sorted(movie_list, key=lambda movie: movie['average_rating'], reverse=True)  # sort by average rating

    return graph

# calculate the average rating from all sources
def get_rating(movie):
    ratings = movie['rating']
    total_rating = 0
    try:
        for rating in ratings:
            if rating['Source'] == 'Internet Movie Database':
                total_rating += float(rating['Value'].split('/')[0])
            elif rating['Source'] == 'Rotten Tomatoes':
                total_rating += float(rating['Value'].replace('%', '')) / 10
            elif rating['Source'] == 'Metacritic':
                total_rating += float(rating['Value'].split('/')[0]) / 10
    except:
        return 0
    return round(total_rating / len(ratings), 1)

with open('cache_final_1.json', 'r') as f:
    movies = json.load(f)

# update the cache_final_1 with 'average_rating'
for movie in movies:
    id = movie['imdbID']
    movie['average_rating'] = get_rating(movie)
    movie['imdb_url'] = f'https://www.imdb.com/title/{id}/'

with open('movies_updated.json', 'w') as f:
    json.dump(movies, f, indent=4)

# Create graph based on director
director_graph = create_movie_graph(movies, 'director')

# Create graph based on actor
actor_graph = create_movie_graph(movies, 'actor')

# Create graph based on genre
genre_graph = create_movie_graph(movies, 'genre')

# Create graph based on rating
rated_graph = create_movie_graph(movies, 'rated')

with open('rated_graph.json', 'w') as file:
    json.dump(rated_graph, file, indent=4)

with open('director_graph.json', 'w') as file:
    json.dump(director_graph, file, indent=4)

with open('genre_graph.json', 'w') as file:
    json.dump(genre_graph, file, indent=4)

with open('actor_graph.json', 'w') as file:
    json.dump(actor_graph, file, indent=4)

with open('movies_updated.json', 'r') as f:
    movies = json.load(f)

def get_recommendations(genre=None, director=None, actor=None, rated=None):
    
    recommendations = []
    
    if genre:
        for movie in genre_graph[genre]:
            if director and movie['director'] != director:
                continue
            if actor and actor not in movie['actor']:
                continue
            if rated and movie['rated'] != rated:
                continue
            recommendations.append(movie)
    elif director:
        for movie in director_graph[director]:
            if genre and genre not in movie['genre']:
                continue
            if actor and actor not in movie['actor']:
                continue
            if rated and movie['rated'] != rated:
                continue
            recommendations.append(movie)
    elif actor:
        for movie in actor_graph[actor]:
            if genre and genre not in movie['genre']:
                continue
            if director and movie['director'] != director:
                continue
            if rated and movie['rated'] != rated:
                continue
            recommendations.append(movie)
    elif rated:
        for movie in rated_graph[rated]:
            if genre and genre not in movie['genre']:
                continue
            if director and movie['director'] != director:
                continue
            if actor and actor not in movie['actor']:
                continue
            recommendations.append(movie)
    
    recommendations = sorted(recommendations, key=lambda movie: movie['average_rating'], reverse=True)[:10]
    return recommendations

def get_poster(movie_name):
    for movie in movies:
        if movie['title'] == movie_name:
            return movie['poster']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'POST':
        # Get the user input from the form
        genre = request.form.get('genre')
        director = request.form.get('director')
        actor = request.form.get('actor')
        rated = request.form.get('rated')

        recommendations = get_recommendations(genre=genre, director=director, actor=actor, rated=rated)

        if recommendations:
            # Store the user's input and recommendations in session
            session['genre'] = genre
            session['director'] = director
            session['actor'] = actor
            session['rated'] = rated
            session['recommendations'] = recommendations
            return render_template('recommendation.html', recommendations=recommendations)
        else:
            return render_template('recommendation.html', error=True)
    else:
        recommendations = session.get('recommendations')
        if recommendations:
            # Retrieve the user's input from session
            genre = session.get('genre')
            director = session.get('director')
            actor = session.get('actor')
            rated = session.get('rated')
            return render_template('recommendation.html', recommendations=recommendations, genre=genre, director=director, actor=actor, rated=rated)
        else:
            return render_template('index.html')



@app.route('/poster', methods=['GET'])
def poster():
    # Get the recommendations from session
    recommendations = session.get('recommendations')
    if not recommendations:
        return render_template('index.html')
    posters = []
    for movie in recommendations:
        title = movie['title']
        poster = movie['poster']
        imdb_url = movie['imdb_url']
        posters.append((title,imdb_url,poster))
        referrer = request.referrer
    return render_template('poster.html', posters=posters, referrer=referrer)

@app.route('/plot')
def plot():
    if 'recommendations' in session:
        recommendations = session['recommendations']

        movie_titles = [rec['title'] for rec in recommendations]
        avg_ratings = [rec['average_rating'] for rec in recommendations]

        fig = make_subplots()
        fig.add_trace(go.Bar(x=movie_titles, y=avg_ratings))

        fig.update_layout(title='Average Ratings of Recommended Movies', xaxis_title='Movie Title', yaxis_title='Average Rating')

        plot_html = fig.to_html(full_html=False)
        referrer = request.referrer
        return render_template('plot.html', plot_html=plot_html, referrer = referrer)
    else:
        referrer = request.referrer
        return render_template('recommendation.html', referrer = referrer)

@app.route('/logout')
def logout():
    # Clear the user's session data
    session.clear()

    # Redirect the user to the index page
    return render_template('logout.html')
    

# @app.route('/back', methods=['GET'])
# def go_back():
#     return redirect(request.referrer)

if __name__ == '__main__':
    app.run(debug=True)
