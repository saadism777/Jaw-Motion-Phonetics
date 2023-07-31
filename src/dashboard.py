#date_string = 'Participant 1 Recording.mkv'
import datetime
import sys
import tkinter as tk
from tkinter import filedialog, ttk

import pygame
from PIL import Image, ImageTk
from tkVideoPlayer import TkinterVideo

from keywords import *

# Variables
showplayer = False

# Getting the name of the output directory from phonetics.py
date_string = str(sys.argv[1])
#date_string = 'Participant 7 video recording.mkv'

# Function to update the duration of the video recording
def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration

# Function to update the scale
def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())

# Function to load the video file
def load_video():
    selected_option = dropdown_var.get()
    video_path = f'../outputs/{date_string}/front_recorded_{date_string}.mp4'
    
    # Show the video player only for when phonetics available
    vid_player.grid(row=4, column=0, columnspan=4, rowspan=6, padx=10, pady=10)  # Adjust columnspan and rowspan
   
    if video_path:
        vid_player.load(video_path)

        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)

# Function for video seek
def seek(value):
    """ used to seek a specific timeframe """
    vid_player.seek(int(value))

# Function for video skip
def skip(value: int):
    """ skip seconds """
    vid_player.seek(int(progress_slider.get())+value)
    progress_value.set(progress_slider.get() + value)

# Function to play and pause the video
def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"

# Function to handle event on video end
def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)

# Function to craete collage
def create_collage(image_paths):
    collage_width = 1000
    collage_height = 800

    # Create a blank image for the collage
    collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))
    global showplayer
    showplayer = True
    # Calculate the size of each image in the collage
    image_width = collage_width // 2
    image_height = collage_height // 2

    # Open and resize each image, and paste them into the collage
    for i, image_path in enumerate(image_paths):
        image = Image.open(image_path)
        image.thumbnail((image_width, image_height))
        x_offset = (i % 2) * image_width
        y_offset = (i // 2) * image_height
        collage.paste(image, (x_offset, y_offset))

    return collage

def display_collage():
    selected_option = dropdown_var.get()
    selected_images = image_paths[selected_option]['images']
    collage = create_collage(selected_images)

    # Convert the PIL image to a Tkinter PhotoImage
    photo = ImageTk.PhotoImage(collage)
    vid_player.grid(row=10, column=10, columnspan=2, padx=10, pady=10)
    # Update the image label
    image_label.configure(image=photo)
    image_label.image = photo

def play_audio(audio_file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

def on_seek(event):
    seek_position = progress_slider.get()
    if seek_position != 0:
        if vid_player.is_loaded():
            vid_player.seek(seek_position)
        seek_position /= 1000  # Convert to seconds
        pygame.mixer.music.set_pos(seek_position)

def get_image_paths(phonetic_type):
    return {
        'images': [
             f'../outputs/{date_string}/audio/{phonetic_type}/{phonetic_type}_Graph.png',
             f'../outputs/{date_string}/audio/{phonetic_type}/{phonetic_type}_histogram_of_amplitude.png',
             f'../outputs/{date_string}/audio/{phonetic_type}/{phonetic_type}_Spectogram.png',
             f'../outputs/{date_string}/audio/{phonetic_type}/{phonetic_type}_time_vs_amplitude.png',
        ],
        'audio': f'../outputs/{date_string}/audio/{phonetic_type}/{phonetic_type}_Audio.wav',
    }

# Create the dictionary like images_path using a for loop
image_paths = {}
for phonetic_type in keywords_dict:
    image_paths[phonetic_type] = get_image_paths(phonetic_type)


# Create the Tkinter root window and maximize it
root = tk.Tk()
root.title('Dental Loop SnP Dashboard')
root.state('zoomed')

# Set the window icon
icon_path = '..\images\logo.ico'   # Replace with the path to your icon file
root.iconbitmap(icon_path)

# Create a frame to contain the left-side components (collages and dropdown)
left_frame = ttk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a frame to contain the right-side components (video and audio)
right_frame = ttk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Audio Play Button
play_button = ttk.Button(left_frame, text='Play Audio', command=lambda: play_audio(image_paths[dropdown_var.get()]['audio']))
play_button.grid(row=0, column=0, padx=10, pady=10)

# Audio Seek Functionality (seeking)
seek_bar = ttk.Progressbar(left_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
#seek_bar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Label for "Processing Phonetics" text
processing_label = tk.Label(left_frame, text="Select Phoneme Type", font=("Arial", 14))
processing_label.grid(row=1, column=0)

# Create a dropdown menu for the options "Fricative" and "Sibilant"
dropdown_var = tk.StringVar()
dropdown_menu = ttk.Combobox(left_frame, textvariable=dropdown_var, values=list(image_paths.keys()), state="readonly")
dropdown_menu.grid(row=2, column=0, padx=10, pady=10)

# Create a button to generate the collage
generate_button = ttk.Button(left_frame, text='View Results', command=display_collage)
generate_button.grid(row=3, column=0, padx=10, pady=10)

# Create a label to display the collage
image_label = ttk.Label(left_frame)
image_label.grid(row=4, column=0, padx=10, pady=10)



# Video Player Code
load_btn = tk.Button(right_frame, text="Load Video", command=load_video)
load_btn.grid(row=0, column=0, padx=10, pady=10)

vid_player = TkinterVideo(scaled=True, master=right_frame, width=500)
vid_player.grid(row=1, column=0, columnspan=2, padx=10, pady=10)  # Set columnspan to 2

play_pause_btn = tk.Button(right_frame, text="Play", command=play_pause)
play_pause_btn.grid(row=2, column=0, padx=10, pady=10)

skip_minus_5sec = tk.Button(right_frame, text="Skip -5 sec", command=lambda: skip(-5))
skip_minus_5sec.grid(row=2, column=1, padx=10, pady=10)

start_time = tk.Label(right_frame, text=str(datetime.timedelta(seconds=0)))
start_time.grid(row=2, column=2, padx=10, pady=10)

progress_value = tk.IntVar(right_frame)

progress_slider = tk.Scale(right_frame, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
progress_slider.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

end_time = tk.Label(right_frame, text=str(datetime.timedelta(seconds=0)))
end_time.grid(row=2, column=3, padx=10, pady=10)

# Bind the on_audio_seek function to the seek bar

progress_slider.bind("<ButtonRelease-1>", on_seek)
seek_bar.bind("<ButtonRelease-1>", on_seek)

# Start the Tkinter main loop
root.mainloop()