import re

def sanitize_filename(filename):

    sanitized_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return sanitized_filename

prompt = input("Input desired prompt for AI: ")
answer = input("Input  desired answer for AI: ")

sanitized_prompt = sanitize_filename(prompt)


with open(sanitized_prompt + '.txt','w') as file:
    file.write(answer)

