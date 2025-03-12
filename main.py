import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title('CursorLex')
root.geometry('300x200')

# Add a label to the window
label = tk.Label(root, text='Welcome to CursorLex!')
label.pack(pady=20)

# Run the application
root.mainloop()