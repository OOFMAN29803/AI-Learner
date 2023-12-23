import tkinter as tk
from tkinter import scrolledtext, Button, Entry, messagebox
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

try:
    model = tf.keras.models.load_model("Silico LMM v0.7.h5")
    tokenizer_layer = None

    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Embedding):
            tokenizer_layer = layer
            break

    if tokenizer_layer:
        tokenizer = Tokenizer(oov_token="<OOV>")
        tokenizer_config = model.get_config()['layers'][0]['config']
        tokenizer.word_index = tokenizer_config.get('word_index', {})
        tokenizer.index_word = tokenizer_config.get('index_word', {})
    else:
        print("Embedding layer not found in the model.")

    print("Model input shape:", model.input_shape)
    max_sequence_length = 58  

    def generate_response():
        user_input = user_entry.get()

        if user_input:
            input_sequence = tokenizer.texts_to_sequences([user_input])

            if input_sequence and input_sequence[0]:
                input_sequence[0] = [word_idx for word_idx in input_sequence[0] if word_idx is not None]


                padded_input_sequence = pad_sequences([input_sequence[0]], maxlen=max_sequence_length, padding='post', truncating='post', value=0)

                prediction = model.predict([np.array(padded_input_sequence), np.array(padded_input_sequence)])[0]

                predicted_text = ' '.join([word for word, idx in tokenizer.word_index.items() if idx in prediction.argmax(axis=1)])

                print(f"User: {user_input}")
                print(f"AI Response: {predicted_text}")

                response_text.config(state=tk.NORMAL)
                response_text.insert(tk.END, f"User: {user_input}\nAI: {predicted_text}\n\n")
                response_text.config(state=tk.DISABLED)
                user_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Error", "Please enter a valid input.")
        else:
            messagebox.showinfo("Error", "Please enter a valid input.")

    window = tk.Tk()
    window.title("AI Language Model Chat")

    user_entry = Entry(window, width=50)
    user_entry.pack(pady=10)

    generate_button = Button(window, text="Generate Response", command=generate_response)
    generate_button.pack(pady=10)

    response_text = scrolledtext.ScrolledText(window, width=60, height=20, state=tk.DISABLED)
    response_text.pack(pady=10)

    window.mainloop()

except Exception as e:
    print(f"An error occurred: {e}")
