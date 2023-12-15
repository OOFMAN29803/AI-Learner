import re
import tkinter as tk

def sanitize_filename(filename):
  filename = filename[:255]
  sanitized_filename = re.sub(r'[<>:"/\\|?*.,]', '', filename)
  return sanitized_filename
def read_file():
    try:
      prompt = entry.get().lower()
      prompt = prompt[:255]
      sanitized_prompt = sanitize_filename(prompt)
      with open(sanitized_prompt + ".txt", 'r') as file:
        updated_content = file.read()
        updated_content = updated_content[:255]
    except FileNotFoundError:
        error = "SilicoLM: I am sorry I do not understand, You may not have trained the AI to understand  >" + "'" + prompt + "'" + "<, try again once you have trained it."
        listbox.insert(tk.END, "You: " + prompt)
        listbox.insert(tk.END, "     ")
        listbox.insert(tk.END, error)
        listbox.insert(tk.END, "     ")
    except Exception as e:
        error = "SilicoLM: An Error Occurred, if this continues, post an issue in Github on the Issues page"
        listbox.insert(tk.END, "You: " + prompt)
        listbox.insert(tk.END, "     ")
        listbox.insert(tk.END, error)
        listbox.insert(tk.END, "     ")     
    finally:
            print("Successful Prompt with 0 known errors")
            listbox.insert(tk.END, "You: " + prompt)
            listbox.insert(tk.END, "     ")          
            listbox.insert(tk.END,"SilicoLM: " + updated_content)
            listbox.insert(tk.END, "     ")
        
root = tk.Tk()
root.title("SilicoLM AI")


save_button = tk.Button(root, text="Enter", command=read_file)
save_button.grid(row=2, column=1, padx=10, pady=10)

listbox = tk.Listbox(root, height=40, width=90)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

entry = tk.Entry(root, width=30)
entry.grid(row=2, column=0, padx=2, pady=2)

root.mainloop()
