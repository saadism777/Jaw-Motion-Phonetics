import sys
import tkinter as tk
from tkinter.ttk import Label
import subprocess
from PIL import Image, ImageTk, ImageSequence

def close_app():
    root.destroy()

def check_backend_status():
    global backend_process

    if backend_process.poll() is None:  # If the process is still running (return code is None)
        root.after(1000, check_backend_status)  # Check again after 1000 milliseconds (1 second)
    else:
        root.after(1000, close_app)  # Delay added for demonstration purposes (2 seconds)

def update_gif(frame_index):
    label.config(image=frames[frame_index])
    root.after(100, update_gif, (frame_index + 1) % len(frames))

root = tk.Tk()
root.title("Phonetics Process")

# Insert your loading GIF here
loading_gif_path = "../images/loading.gif"

# Load GIF and extract frames
gif = Image.open(loading_gif_path)
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

label = Label(root)
label.pack()

# Label for "Processing Phonetics" text
processing_label = tk.Label(root, text="Processing Phonetics", font=("Arial", 14))
processing_label.pack()

# Start the backend process
backend_process = subprocess.Popen(["python", "phonetics.py", str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])])

# Check the backend status
root.after(10000, check_backend_status)

# Animate the GIF
update_gif(0)

# Center the window on the screen
window_width = 300  # Replace with the desired window width
window_height = 400  # Replace with the desired window height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

root.mainloop()
