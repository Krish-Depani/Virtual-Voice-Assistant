import json
import numpy as np
import os
import logging
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import keras

import pickle

with open("..\\Data\\intents.json") as file:
    data = json.load(file)


def chat(text):
    # load trained model
    model = keras.models.load_model('..\\Data\\chat_model')

    # load tokenizer object
    with open('..\\Data\\tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('..\\Data\\label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    while True:

        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text]),
                                                                          truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]

        for i in data['intents']:
            if i['tag'] == tag:
                response = np.random.choice(i['responses'])
                return tag, response

print(chat("Get me some news"))