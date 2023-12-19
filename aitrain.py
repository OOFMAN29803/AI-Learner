import re
from gtts import gTTS

def sanitize_filename(filename):
    filename = filename[:255]
    sanitized_filename = re.sub(r'[<>:"/\\|?*!@#$%^&().,]', '', filename)
    return sanitized_filename

prompt = input("Input desired prompt for AI: ").lower()
answer = input("Input desired answer for AI: ")
prompt = prompt[:255]

sanitized_prompt = re.sub(r'[<>:"/\\|?*!@#$%^&().,]', '', prompt)

with open(sanitized_prompt + '.txt','w') as file:
  file.write(answer)

text = answer
tts = gTTS(text=text, lang='en')
tts.save(sanitized_prompt + ".mp3")


