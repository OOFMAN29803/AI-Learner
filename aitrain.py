import re

for i in range(200):

  def sanitize_filename(filename):
    filename = filename[:255]
    sanitized_filename = re.sub(r'[<>:"/\\|?*.,]', '', filename)
    return sanitized_filename
    prompt = input("Input desired prompt for AI: ").lower()
    answer = input("Input desired answer for AI: ")
    sanitized_prompt = sanitize_filename(prompt)
    prompt = prompt[:255]

    with open(sanitized_prompt + '.txt','w') as file:
      file.write(answer)
      sanitize_filename(filename)

