import json
from keras_preprocessing.sequence import pad_sequences
import numpy as np
import os
import logging
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#from tensorflow import keras
from keras.models import load_model
from pickle import load

with open("Data\\intents.json") as file:
    data = json.load(file)

# load trained model
model = load_model('Data\\chat_model')

# load tokenizer object
with open('Data\\tokenizer.pickle', 'rb') as handle:
    tokenizer = load(handle)

# load label encoder object
with open('Data\\label_encoder.pickle', 'rb') as enc:
    lbl_encoder = load(enc)

def chat(text):
    # parameters
    max_len = 20

    while True:

        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]),
                                                                          truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]

        for i in data['intents']:
            if i['tag'] == tag:
                response = np.random.choice(i['responses'])
                return tag, response


if __name__ == "__main__":
    while True:
        ip = input("Enter input : ")
        print(chat(ip))