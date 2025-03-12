import tkinter as tk
import pyperclip

# Function to get text from clipboard and print it

def get_text_from_clipboard():
    text = pyperclip.paste()
    print(f"Received text: {text}")
    # Here you can add code to call a dictionary API and display the meaning

# Create the main application window
root = tk.Tk()
root.title('CursorLex')
root.geometry('300x200')

# Add a button to get text from clipboard
button = tk.Button(root, text='Get Text from Clipboard', command=get_text_from_clipboard)
button.pack(pady=20)

# Run the application
root.mainloop()