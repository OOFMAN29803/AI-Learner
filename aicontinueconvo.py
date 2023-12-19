import re
import tkinter as tk
from re import search
import os


def sanitize_filename():
    filename = filename[:255]
    sanitized_filename = re.sub(r'[<>:"/\\|?*!@#$%^&().,]', '', filename)
    sanitized_folder = re.sub(r'[<>:"/\\|?*!@#$%^&().,]', '', folder)
    return sanitized_filename
    return sanitized_folder
folder_name = input("Enter the continued conversation name")
os.makedirs(folder_name)
prompt = input("Input desired prompt for AI: ").lower()
answer = input("Input desired answer for AI: ")
sanitized_prompt = sanitized_filename(prompt)
sanitized_foldername = sanitized_folder(folder_name)
prompt = prompt[:255]
folder_name = folder_name[:255]
os.makedirs(sanitized_foldername)

with open(sanitized_prompt + '.txt','w') as file:
  file.write(answer)


