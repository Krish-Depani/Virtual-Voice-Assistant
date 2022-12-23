import subprocess

print("THIS MAY TAKE A WHILE DEPENDING ON YOUR SYSTEM AND INTERNET SPEED\n\nPLEASE WAIT..\n\n")

try:
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
except KeyboardInterrupt:
    print("DOWNLOAD STOPPED")
    exit(0)

import os
import logging
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disabling warnings for gpu requirements

import sqlite3
conn = sqlite3.connect('Data/chats.db')
cursor = conn.cursor()
table = '''CREATE TABLE IF NOT EXISTS ASSISTANT (SERIAL_NO INTEGER PRIMARY KEY,
            QUERY VARCHAR(255) NOT NULL ,
            DATE_TIME VARCHAR(50) NOT NULL );'''
cursor.execute(table)
conn.commit()

try:
    # importing prebuilt modules
    import pyttsx3
    from keras_preprocessing.sequence import pad_sequences
    import numpy as np
    from keras.models import load_model
    from pickle import load
    import speech_recognition as sr
    import sys
    from keras.preprocessing.text import Tokenizer
    from keras_preprocessing.sequence import pad_sequences
    from sklearn.preprocessing import LabelEncoder
    from tensorflow.python.keras.models import Sequential
    from tensorflow.python.keras.layers import Dense, Embedding, GlobalAveragePooling1D
    import datetime
    from dotenv import load_dotenv
    from newsapi import NewsApiClient
    import re
    import requests
    from wolframalpha import Client
    import webbrowser
    import wikipedia
    import speedtest
    from youtubesearchpython import VideosSearch
    import smtplib
    import io
    import warnings
    from PIL import Image
    from stability_sdk import client
    import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
    import math
    import psutil
    import time
    from random import randint
    import AppOpener
    from pynput.keyboard import Key, Controller
    from PIL import ImageGrab
    import wmi
except ImportError:
    print("MODULES NOT INSTALLED!")
    exit(0)
except KeyboardInterrupt:
    print("INTERRUPTED WHILE IMPORTING MODULES")

print("\n\nSETUP SUCCESSFUL")