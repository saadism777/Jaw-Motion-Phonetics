import csv
import datetime
import os
import subprocess
import sys
import pylab
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import whisper
from halo import Halo
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.utils import make_chunks
from sklearn.preprocessing import MinMaxScaler
import cv2
import pyaudio
import wave
import threading
from keywords import *

# Printing Keywords Dictionary
print("Keywords Dictionary:")
for phonetic_type, keywords in keywords_dict.items():
    print(f"{phonetic_type}: {keywords}")

# Variables Declaration
phonetics_output_file = None
graph_output_file = None
amplitude_output_file = None
histogram_output_file = None
spectogram_output = None

# Function to convert video to audio file
def convert_video_to_wav(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_file)

def plot_time_vs_amplitude(audio_file, name):
    phonetic_output_dir = os.path.join(audio_output_dir, f'{name}')
    amplitude_output_file = os.path.join(phonetic_output_dir, f'{name}_time_vs_amplitude.png')
    histogram_output_file = os.path.join(phonetic_output_dir, f'{name}_histogram_of_amplitude.png')
    csv_file = os.path.join(phonetic_output_dir, f'{name}_time_vs_amplitude.csv')
    audio, sr = librosa.load(audio_file)
    time = np.arange(0, len(audio)) / sr
    data = list(zip(time, audio))
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header row if needed
        csv_writer.writerow(["Time", "Amplitude"])
        csv_writer.writerows(data)
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title(f'Time vs Amplitude for {name} Audio')
    plt.savefig(amplitude_output_file, dpi=500)
    plt.close()

    # Plot amplitude histogram
    plt.figure(figsize=(6, 4))
    plt.hist(audio, bins=10, density=True)
    plt.xlabel('Amplitude')
    plt.ylabel('Frequency')
    # Create a range of values with the desired interval (0.01)
    interval = 0.01
    x_interval = np.arange(-0.1, 0.1, interval)

    # Set the x-axis limits based on the interval
    plt.xlim(min(x_interval), max(x_interval))
    plt.title(f'Amplitude Histogram for {name} Audio')
    plt.savefig(histogram_output_file, dpi=500)
    plt.close()

def search(keywords,name):
    phonetic_output_dir = os.path.join(audio_output_dir, f'{name}')
    if not os.path.exists(phonetic_output_dir):
        os.makedirs(phonetic_output_dir)
    try:
        # Store the timestamps of matching rows
        timestamps = []
        # Iterate through the DataFrame rows
        for index, row in df.iterrows():
            text = row['text']
            if any(keyword in text.lower() for keyword in keywords):
                timestamps.append((row['start'], row['end']))

        df2 = pd.DataFrame(timestamps)
        
        # Create a list to store the trimmed audio segments
        trimmed_segments = []

        # Load the original audio file
        audio = AudioSegment.from_file(output_file, format='wav')

        # Iterate through the timestamps and extract the trimmed audio segments
        for start, end in timestamps:
            trimmed_segments.append(audio[int(start * 1000):int(end * 1000)])
        print(timestamps)    
        # Concatenate the trimmed audio segments
        trimmed_audio = sum(trimmed_segments)
        
        # Output file path
        phonetics_output_file = os.path.join(phonetic_output_dir, f'{name}_Audio.wav')
        phonetics_timestamps = os.path.join(phonetic_output_dir,f'{name}_Timestamps.csv')
        spectogram_output =  os.path.join(phonetic_output_dir,f'{name}_Spectogram.png')
        # Save the DataFrame to an CSV file
        df2.to_csv(phonetics_timestamps, index=False)
        
        # Export the trimmed audio to a new file
        trimmed_audio.export(phonetics_output_file, format='wav')

        # Load the audio and its sample rate (sr)
        audio, sr = librosa.load(phonetics_output_file)
        # Calculate the maximum absolute value in the audio
        max_val = np.max(np.abs(audio))
        
        # Normalize the audio by dividing each sample by the maximum value
        normalized_audio = audio / max_val
        S = librosa.feature.melspectrogram(y=normalized_audio, sr=sr)

        librosa.display.specshow(librosa.power_to_db(S, ref=np.max))

        pylab.savefig(spectogram_output, dpi=1200, bbox_inches=None, pad_inches=0)

        # Normalize the pitch
        #audio_normalized = normalize_pitch(audio, sr ,  target_pitch)

        #create_spectrogram(audio_normalized, sr, spectogram_output)
        
        plot_time_vs_amplitude(phonetics_output_file, name)

    except FileNotFoundError:
        print(f"Timestamp file {phonetics_timestamps} not found.")
    except pd.errors.EmptyDataError:
        print(f"Timestamp file {phonetics_timestamps} is empty.")
    except AttributeError:
        print(f"Attribute error occurred. Check if the input data is valid.")

def plot_histogram(name):
    phonetic_output_dir = os.path.join(audio_output_dir, f'{name}')
    if not os.path.exists(phonetic_output_dir):
        os.makedirs(phonetic_output_dir)
    graph_output_file = os.path.join(phonetic_output_dir, f'{name}_Graph.png')
    # Read the start_csv_path and end_csv_path into DataFrames
    phonetics_timestamps = os.path.join(phonetic_output_dir,f'{name}_Timestamps.csv')
    phonetics_distances = os.path.join(phonetic_output_dir,f'{name}_Distances.csv')
    statistics_file = os.path.join(phonetic_output_dir, f'{name}_statistics.txt')
    try:
        df = pd.read_csv(phonetics_timestamps)

        # Extract the start and end times
        start_times = df['0']
        end_times = df['1']

        # Read the data_csv_path
        data_df = pd.read_csv(distance_csv_path)

        # Filter the 'Time(s)' column based on start and end times
        filtered_data = data_df.loc[data_df['Time(s)'].between(start_times.min(), end_times.max())]
        filtered_data.to_csv(phonetics_distances, index=False)
        # Calculate variance and mean of the 'sN-Sn' column
        sn_sn_mean = filtered_data['sN-Sn(mm)'].mean()
        sn_sn_variance = filtered_data['sN-Sn(mm)'].var()
        # Save mean and variance to a text file
        with open(statistics_file, 'w') as f:
            f.write(f"Mean: {sn_sn_mean}\n")
            f.write(f"Variance: {sn_sn_variance}\n")
        # Plot a histogram of the specified column values
        data = filtered_data['sN-Sn(mm)']
        plt.figure()
        plt.hist(data, bins=np.linspace(data.min(), data.max(), 20))
        plt.xlabel(f'sN-Sn(mm) of {name}')
        plt.ylabel('Frequency')
        plt.title(f'Histogram of {name} SN-Sn(mm) Values')
        plt.savefig(graph_output_file, dpi=600)
        print(f'{name} Data Generated')
        plt.close()
    except FileNotFoundError:
        print(f"Timestamp file {phonetics_timestamps} not found.")
    except pd.errors.EmptyDataError:
        print(f"Timestamp file {phonetics_timestamps} is empty.")
    except AttributeError:
        print(f"Attribute error occurred. Check if the input data is valid.")



# Create a directory to store the trimmed audio files
path = str(sys.argv[1])
date_string = str(sys.argv[2])
data_path = str(sys.argv[3])
#path = r'C:\Users\saadi\Videos\Sample recordings for SnP 3.7.23\Participant 1 Recording.mkv'
#date_string = "Participant 1 Recording.mkv"
#data_path = r'C:\Projects\results snp\1\front_eucledian_distances_21-07-2023_02-47PM.csv'

phonetics_timestamps= None

# Get the path to the project's root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the outputs directory in the project's root directory
output_dir = os.path.join(project_root, '..' , 'outputs')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#Timestamp Dir
#date_string = datetime.datetime.now().strftime("%d-%m-%Y_%I-%M%p")
timestamp_dir = os.path.join(output_dir, date_string)
if not os.path.exists(timestamp_dir):
    os.makedirs(timestamp_dir)

# Audio output directory
audio_output_dir = os.path.join(timestamp_dir, 'audio')
if not os.path.exists(audio_output_dir):
    os.makedirs(audio_output_dir)

# Raw audio output directory
output_file = os.path.join(audio_output_dir, 'raw.wav')

# Convert audio (.wav) from video format
convert_video_to_wav(path, output_file)

# Euclidean distance file path
distance_csv_path = os.path.join(timestamp_dir, f'front_eucledian_distances_{date_string}.csv')

# Whisper model size/type among-(tiny.en, small.en, medium.en, large)
model_size = 'tiny.en'

# Specify the keywords to search for
#keywords_fricative = ['father', 'found', 'coffee']
#keywords_sibilant = ['sisters', 'saw', 'zebra','zoo']
#keywords_linguodental = [ 'they', 'thought', 'there', 'were']
#keywords_bilabial = [ 'bobby', 'popped','balloon']
#keywords_mixed = ['sixty','61','62','63','64','65','66','67','68','69', 'city', '1', '2', '4', '6', '7', '8', '9']

# 
model = whisper.load_model(model_size)

# Display spinner animation for model.transcribe()
spinner = Halo(text='Processing', spinner='dots')  # Initialize the spinner

# Your long-running process (example)
spinner.start()  # Start the spinner animation
result = model.transcribe(output_file)
spinner.stop()  # Stop the spinner animation

# segments of all the output files are attached
segments = result["segments"]

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame(segments)

# Saving the output file
save_csv = os.path.join(audio_output_dir, f'phonetics_{date_string}.csv')

# Save the DataFrame to an CSV file
df.to_csv(save_csv, index=False)

for phonetic_type, keywords in keywords_dict.items():
    search(keywords, f"{phonetic_type}")
    plot_histogram(f"{phonetic_type}")

print("Done!")

subprocess.Popen(['python', 'dashboard.py', str(date_string)])