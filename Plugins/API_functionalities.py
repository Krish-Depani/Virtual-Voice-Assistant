import os
import datetime
import wolframalpha
from dotenv import load_dotenv
from newsapi import NewsApiClient
from speak import speak
import re
import requests
from wolframalpha import Client

load_dotenv(dotenv_path='..\\Data\\.env')

NEWS = os.getenv('NEWS_API')
WOLFRAMALPHA = os.getenv('WOLFRAMALPHA_API')
OPENWEATHERMAP = os.getenv('OPENWEATHERMAP_API')
IPSTACK = os.getenv('IPSTACK_API')
TMDB = os.getenv('TMDB_API')
news = NewsApiClient(api_key=NEWS)

def get_ip():
    try:
        response = requests.get(f'http://api.ipstack.com/check?access_key={IPSTACK}').json()
        speak(f'Your IP address is {response["ip"]}')
    except KeyboardInterrupt:
        return
    except requests.exceptions.RequestException:
        return "Request Error"

def get_joke():
    try:
        joke = requests.get('https://v2.jokeapi.dev/joke/Any?format=txt').text
        speak(joke)
    except KeyboardInterrupt:
        return
    except requests.exceptions.RequestException:
        return "Request Error"

def get_news():
    try:
        top_headlines = news.get_top_headlines(language="en", country="in")
        for i in range(10):
            speak(re.sub(r'- [A-Za-z]*', '', top_headlines['articles'][i]['title']).replace("’", "'"))
    except KeyboardInterrupt:
        return
    except requests.exceptions.RequestException:
        return "Request Error"

def get_weather(city):
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP}&units=metric').json()
        speak(f'It\'s {response["main"]["temp"]}° Celsius and {response["weather"][0]["main"]}\n'
              f'But feels like {response["main"]["feels_like"]}° Celsius\n'
              f'Wind is blowing at {round(response["wind"]["speed"] * 3.6, 2)}km/h\n'
              f'Visibility is {int(response["visibility"] / 1000)}km')
    except requests.exceptions.RequestException:
        return "Request Error"
    except KeyboardInterrupt:
        return

def get_general_response(query):
    client = Client(app_id=WOLFRAMALPHA)
    try:
        response = client.query(query)
        speak(next(response.results).text)
    except wolframalpha.ErrorHandler or StopIteration or AttributeError:
        return f'Error with query {query}'
    except KeyboardInterrupt:
        return

def get_latest_movies():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return "Request Error"
    try:
        err = response['results']
        speak("Some of the latest popular movies are as follows :")
        print()
        for movie in response["results"]:
            title = movie['title']
            print(title)
    except KeyError:
        return "Query Not Found"

def get_popular_tvseries():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
        print(response)
    except requests.exceptions.RequestException:
        return "Request Error"
    try:
        err = response['results']
        speak("Some of the latest popular tv series are as follows :")
        print()
        for show in response["results"]:
            title = show['name']
            print(title)
    except KeyError:
        return "Query Not Found"