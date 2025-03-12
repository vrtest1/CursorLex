import tkinter as tk
import pyperclip
import requests

# Function to get text from clipboard, fetch meaning from API, and display it

def get_text_from_clipboard():
    text = pyperclip.paste()
    print(f"Received text: {text}")
    meaning = get_word_meaning(text)
    print(f"Meaning: {meaning}")
    # Display the meaning in a label or popup
    result_label.config(text=f"Meaning: {meaning}")

# Function to get word meaning from Free Dictionary API
def get_word_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        meanings = data[0]['meanings'][0]['definitions'][0]['definition']
        return meanings
    else:
        return "Meaning not found."

# Create the main application window
root = tk.Tk()
root.title('CursorLex')
root.geometry('300x200')

# Add a button to get text from clipboard
button = tk.Button(root, text='Get Text from Clipboard', command=get_text_from_clipboard)
button.pack(pady=20)

# Label to display the result
result_label = tk.Label(root, text='')
result_label.pack(pady=10)
    else:
        return "Meaning not found."

# Create the main application window
root = tk.Tk()
root.title('CursorLex')
root.geometry('300x200')

# Add a button to get text from clipboard
button = tk.Button(root, text='Get Text from Clipboard', command=get_text_from_clipboard)
button.pack(pady=20)

# Run the application
root.mainloop()