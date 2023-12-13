import re

for i in range(200):

    def sanitize_filename(filename):

        sanitized_filename = re.sub(r'[<>:"/\\|?*.]', '', filename)
        return sanitized_filename

prompt = input("Answer from the bot: ").lower()

sanitized_prompt = sanitize_filename(prompt)

with open(sanitized_prompt + ".txt",'r') as file:
    updated_content = file.read()
    print(updated_content)
