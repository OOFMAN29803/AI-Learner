import re
import tkinter as tk
from re import search
import os
from gtts import gTTS
import random
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense
import json

with open("dataset.txt", "r", encoding="utf-8") as file:
    dataset = file.read()

data = json.loads(dataset)

all_texts = [item["user_prompt"] + "" + item["ai_response"] for item in data]
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(all_texts)


input_sequences = tokenizer.texts_to_sequences([item['user_prompt'] for item in data])
output_sequences = tokenizer.texts_to_sequences([item['ai_response'] for item in data])

max_sequence_length = max(max(map(len, input_sequences)), max(map(len, output_sequences)))

padded_input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='post')
padded_output_sequences = pad_sequences(output_sequences, maxlen=max_sequence_length, padding='post')

X_train, X_test, y_train, y_test = train_test_split(
  padded_input_sequences,
  padded_output_sequences,
  test_size=0.4,
  random_state=42
)

latent_dim = 256

encoder_inputs = Input(shape=(max_sequence_length,))
encoder_embedding = Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=latent_dim, mask_zero=True)(encoder_inputs)
encoder_lstm = LSTM(latent_dim, return_state=True)
_, state_h, state_c = encoder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

decoder_inputs = Input(shape=(max_sequence_length,))
decoder_embedding = Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=latent_dim, mask_zero=True)(decoder_inputs)
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = Dense(len(tokenizer.word_index) + 1, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.summary()

model.fit(
    [X_train, X_train],
    y_train.reshape(y_train.shape[0], y_train.shape[1], 1),
    epochs=400,
    batch_size=64,
    validation_data=([X_test, X_test], y_test.reshape(y_test.shape[0], y_test.shape[1], 1))
)


predictions = model.predict([X_test, X_test])

sample_index = random.randint(0, len(X_test) - 1)
input_sequence = X_test[sample_index].reshape(1, -1)
predicted_sequence = predictions[sample_index]

input_text = ' '.join([word for word, idx in tokenizer.word_index.items() if idx in input_sequence.flatten()])
predicted_text = ' '.join([word for word, idx in tokenizer.word_index.items() if idx in predicted_sequence.argmax(axis=1)])
print(f"Input: {input_text}\nPredicted: {predicted_text}")
