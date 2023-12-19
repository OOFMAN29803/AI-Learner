import re
import tkinter as tk
from re import search
import os
import speech_recognition as sr

recognizer = sr.Recognizer()
source = sr.Microphone()

def sanitize_filename():
  filename = filename[:255]
  sanitized_filename = re.sub(r'[<>:"/\\|?*!@#$%^&().,]', '', filename)
  return sanitized_filename
def read_file():
    text = ""
    updated_content = ""
    try:
        audio_data = recognizer.listen(source)
        text = recognizer.recognize_google(audio_data)
        sanitized_prompt = sanitize_filename(text)
        with open(sanitized_prompt + ".txt", 'r') as file:
            updated_content = file.read()
            updated_content = updated_content[:255]
    except FileNotFoundError:
        error = "SilicoLM: I am sorry I do not understand, You may not have trained the AI to understand  >" + "'" + text + "'" + "<, try again once you have trained it."
        listbox.insert(tk.END, "     ")
        listbox.insert(tk.END, error)
        listbox.insert(tk.END, "     ")
    except Exception as e:
        error = "An Error Occurred, if this continues, post an issue in Github on the Issues page"
        listbox.insert(tk.END, "     ")
        listbox.insert(tk.END, error)
        listbox.insert(tk.END, "     ")     
    finally:
        print("Successful Prompt with 0 known errors")
        listbox.insert(tk.END, "You: " + text)
        listbox.insert(tk.END, "     ")          
        listbox.insert(tk.END, "SilicoLM: " + updated_content)
        listbox.insert(tk.END, "     ")
        listbox.delete(0, tk.END)
        entry.insert(tk.END, text)


def trainingopen():
  file_path = "aitrain.py"
  os.system(f"start {file_path}")

root = tk.Tk()
root.title("SilicoLM AI")

prompt_button = tk.Button(root, text="Enter", command=read_file)
prompt_button.grid(row=2, column=1, padx=1, pady=10)

train_button = tk.Button(root, text="Train", command=trainingopen)
train_button.grid(row=2, column=2, padx=1, pady=10)

listbox = tk.Listbox(root, height=40, width=140)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

entry = tk.Entry(root, width=30)
entry.grid(row=2, column=0, padx=2, pady=2)

root.mainloop()
