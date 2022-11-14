import webbrowser
import re
import wikipedia
from Data.websites import websites_dict
import speedtest
from speak import speak
from youtubesearchpython import VideosSearch

def googleSearch(query):
	if 'image' in query:
		query += "&tbm=isch"
	query = query.replace('images', '')
	query = query.replace('image', '')
	query = query.replace('search', '')
	query = query.replace('show', '')
	webbrowser.open("https://www.google.com/search?q=" + query)
	return "Here you go..."

def youtube(query):
	query = query.replace('play', ' ')
	query = query.replace('on youtube', ' ')
	query = query.replace('youtube', ' ')

	print("Searching for videos...")
	videosSearch = VideosSearch(query, limit=1)
	results = videosSearch.result()['result']
	print("Finished searching!")

	webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
	return "Enjoy..."

def open_website(url):
	webbrowser.open(url)

def open_specified_website(query):
	website = query[5:]#re.search(r'[a-zA-Z]* (.*)', query)[1]
	if website in websites_dict:
		url = websites_dict[website]
	else:
		return None
	open_website(url)

def get_speedtest():
	try:
		internet = speedtest.Speedtest()
		speak(f"Your network's Download Speed is {round(internet.download() / 8388608, 2)}MBps")
		speak(f"Your network's Upload Speed is {round(internet.upload() / 8388608, 2)}MBps")
	except speedtest.SpeedtestException:
		print("Speedtest Exception")
	except KeyboardInterrupt:
		return

def tell_me_about(query):
	try:
		topic = re.search(r'([A-Za-z]* [A-Za-z]* [A-Za-z]* [A-Za-z]*)$', query)[1]
		result = wikipedia.summary(topic, sentences=3)
		result = re.sub(r'\[.*]', '', result)
		speak(result)
	except wikipedia.WikipediaException or Exception:
		return "Wikipedia Error"

def get_map(query):
	open_website(f'https://www.google.com/maps/search/{query}')

open_specified_website('open netflix')