import tkinter as tk
import pyperclip
import requests

def get_text_from_clipboard():
    try:
        text = pyperclip.paste().strip()
        print(f"Received text: {text}")
        meaning = get_word_meaning(text)
        print(f"Meaning: {meaning}")
        result_label.config(text=f"Meaning: {meaning}")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def get_word_meaning(word):
    try:
        url = f"https://jisho.org/api/v1/search/words?keyword={word}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data['data'][0]['senses'][0]['english_definitions'][0]
        return f"Error: {response.status_code} - {response.text}"
    except (KeyError, IndexError):
        return "解析エラー：データ構造が異なります"
    except Exception as e:
        return f"予期せぬエラー: {str(e)}"

# GUI設定
root = tk.Tk()
root.title('CursorLex')
root.geometry('300x200')

button = tk.Button(root, text='Get Text from Clipboard', command=get_text_from_clipboard)
button.pack(pady=20)

result_label = tk.Label(root, text='', wraplength=250)
result_label.pack(pady=10)

root.mainloop()


# Create the main application window
root = tk.Tk()
root.title('CursorLex')
root.geometry('300x200')

# Add a button to get text from clipboard
button = tk.Button(root, text='Get Text from Clipboard', command=get_text_from_clipboard)
button.pack(pady=20)

# Run the application
root.mainloop()