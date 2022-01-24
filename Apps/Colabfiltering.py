import streamlit as st
import numpy as np
import pickle
import sqlite3
import requests
import pandas as pd

movies_dict = pickle.load(open('Apps/Data/movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
moviesdf = movies['movieId'].map(str) + "-" + movies['title'].map(str)
abc = []


def fetch_poster(movie_title):
    response = requests.get('https://api.themoviedb.org/3/search/movie/?query={''}&'
                            'api_key=038c689b969cb54e298a1406b400563d&language=en-US&'.format(movie_title))
    data = response.json()
    hasnain = data['results']
    hasnain2 = hasnain[0]
    return "http://image.tmdb.org/t/p/w500" + hasnain2['poster_path']


def getuserId(username):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users where username = ?', [username])
    data = c.fetchall()
    return abc.append(data)


def recommendation(movienamelst, ratinglst):
    last_user = abc[len(abc) - 1]
    first_tupple_element = []
    for a in last_user:
        first_tupple_element.append(a[0])

    for i in range(len(movienamelst)):
        for j in range(len(ratinglst)):
            print()
        last_movie = movienamelst[len(movienamelst) - 1]
        last_movie_remove = last_movie.replace("-", " ")
        split_last_movie = last_movie_remove.split(" ")
        for i in range(len(split_last_movie)):
            updated_lastmovie_id = split_last_movie[0]
        mov_name = split_last_movie.pop(0)
        seperator = " "
        last_mname = seperator.join(split_last_movie)

        slast_movie = movienamelst[len(movienamelst) - 2]
        slast_movie_remove = slast_movie.replace("-", " ")
        split_slast_movie = slast_movie_remove.split(" ")
        for i in range(len(split_slast_movie)):
            updated_slastmovie_id = split_slast_movie[0]
        mov_name = split_slast_movie.pop(0)
        seperator = " "
        slast_mname = seperator.join(split_slast_movie)

        tlast_movie = movienamelst[len(movienamelst) - 3]
        tlast_movie_remove = tlast_movie.replace("-", " ")
        split_tlast_movie = tlast_movie_remove.split(" ")
        for i in range(len(split_tlast_movie)):
            updated_tlastmovie_id = split_tlast_movie[0]
        mov_name = split_tlast_movie.pop(0)
        seperator = " "
        tlast_mname = seperator.join(split_tlast_movie)

        # last movie
        last_rating = ratinglst[len(ratinglst) - 1]
        # second movie
        slast_rating = ratinglst[len(ratinglst) - 2]
        # first movie
        tlast_rating = ratinglst[len(ratinglst) - 3]

    data = {
        'userId': [first_tupple_element[0], first_tupple_element[0], first_tupple_element[0]],
        'movieId': [updated_lastmovie_id, updated_slastmovie_id, updated_tlastmovie_id],
        'rating': [last_rating, slast_rating, tlast_rating],
    }

    df = pd.DataFrame(data)
    df.to_csv('Apps/Data/ratings.csv', mode='a', index=False, header=False)
    st.success('Movies Rated Sucessfully')

    ratings = pd.read_csv('Apps/Data/ratings.csv')
    movies = pd.read_csv('Apps/Data/movies.csv')
    ratings = pd.merge(movies, ratings).drop(['timestamp'], axis=1)
    userRatings = ratings.pivot_table(index=['userId'], columns=['title'], values='rating')
    corrMatrix = userRatings.corr(method='pearson')

    def get_similar(movie_name, rating):
        similar_ratings = corrMatrix[movie_name] * (rating - 2.5)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        return similar_ratings

    mov_title_ratings = [(tlast_mname, tlast_rating), (slast_mname, slast_rating), (last_mname, last_rating)]
    similar_movies = pd.DataFrame()
    for movie, rating in mov_title_ratings:
        similar_movies = similar_movies.append(get_similar(movie, rating), ignore_index=True)

    data_new = pd.DataFrame(similar_movies.sum().sort_values(ascending=False).head(5))
    data_new.to_csv('Apps/Data/prediction.csv', mode='w', header=True)
    predictionData = pd.read_csv('Apps/Data/prediction.csv')
    prediction = pd.DataFrame(predictionData)
    prediction.columns = ['title', 'similarity']
    for column in prediction[['title']]:
        # Select column contents by column name using [] operator
        columnSeriesObj = prediction[column]
        myvar = []
        myvar = columnSeriesObj.values
    movie_title_1 = myvar[0]
    movie_title_2 = myvar[1]
    movie_title_3 = myvar[2]
    movie_title_4 = myvar[3]
    movie_title_5 = myvar[4]

    list1 = Convert(movie_title_1)
    list2 = Convert(movie_title_2)
    list3 = Convert(movie_title_3)
    list4 = Convert(movie_title_4)
    list5 = Convert(movie_title_5)
    del list1[-1]
    del list2[-1]
    del list3[-1]
    del list4[-1]
    del list5[-1]
    mylist =[ConvStr(list1),ConvStr(list2),ConvStr(list3),ConvStr(list4),ConvStr(list5)]
    recommended_movies = []
    recommended_movies_posters = []
    for i in range(len(mylist)):
        recommended_movies.append(mylist[i])
        recommended_movies_posters.append(fetch_poster(mylist[i]))
    return recommended_movies,recommended_movies_posters


def Convert(inp):
    li = list(inp.split(" "))
    return li


def ConvStr(list_name):
    listToStr = ' '.join(map(str, list_name))
    return listToStr


def app():
    selected_movie_name = st.multiselect(
        'Select upto 3 movies you like',
        (moviesdf))

    if len(selected_movie_name) > 3 & len(selected_movie_name) < 3:
        st.error("Select 3 movies")
    elif len(selected_movie_name) == 3:
        st.write("Rate The Movies")
        rating = []
        movie = []
        for i in range(len(selected_movie_name)):
            ratingSliderMov = st.slider(selected_movie_name[i], 1, 5)
            rating.append(ratingSliderMov)
            movie.append(selected_movie_name[i])

        if st.button("Rate"):
            names, posters = recommendation(movie,rating)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.caption(names[0])
                st.image(posters[0])
            with col2:
                st.caption(names[1])
                st.image(posters[1])

            with col3:
                st.caption(names[2])
                st.image(posters[2])
            with col4:
                st.caption(names[3])
                st.image(posters[3])
            with col5:
                st.caption(names[4])
                st.image(posters[4])
