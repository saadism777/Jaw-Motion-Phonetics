
# Dental Loop SnP

Dental Loop SnP is a cutting-edge Python-based software application designed to revolutionize the analysis of phonetic speech patterns in dental clinic patients. This repository contains the complete source code and related materials for the Dental Loop SnP software.

# What is Dental Loop SnP?

Dental Loop SnP facilitates the extraction and analysis of audio data from video recordings capturing patients uttering various phonetic sentences. By leveraging advanced phonetic analysis techniques and a state-of-the-art text-to-speech engine, "Whisper" from OpenAI, the software generates graphical and statistical data that offer unprecedented insights into speech patterns and phonetic variations.

# Features and Functionalities

1. The software consists of four Python files developed according to PEP-8 coding style guidelines: 'main.py', 'face_app.py', 'phonetics.py', and 'dashboard.py'.

2. 'main.py' initiates a dialogue box using pyQT5, allowing the user to select a video file for processing.

3. 'face_app.py' uses the Dlib library and deep neural networks for facial landmark recognition, calculating maxillofacial landmarks and lines and converting pixel lengths to millimeters.

4. 'phonetics.py' converts the video to a raw audio file (.wav) using pretrained speech-to-text transcriber model "whisper" from OpenAI. Specific phoneme types are extracted from the transcriptions based on predefined keywords, and spectrograms and graphs are generated.

5. The dashboard, opened automatically, presents spectrograms, graphs, and correlation histograms side by side for selected phonetic types, providing an interactive platform for analyzing phonetics, jaw elevation, and speech patterns.

## Installation
The follwing step by steps procedure will aid in installation of the software. Python version : 3.10.11
1. Install Visual Studio Community Edition and Install Desktop C++ Desktop Environment (Including CMake)
2. Download CMake. [Link](https://cmake.org/download/)
3. Download Anaconda or Miniconda.
4. Download ffmpeg from here extract it and add the path of the extracted folder to windows environment variable. [Link](https://ffmpeg.org/download.html)
5. Open conda prompt and enter the following commands

```bash
  pip install cmake
```

```bash
  pip install dlib
```
6. Go to the project root folder and open a cmd prompt. Enter the following command to create a new virtual environment and activate it.
```bash
 python -m venv /path/virtual_environment 
```
7. Install all the necessary requirements for the application using the requirements.txt file.
```bash
 pip install requirements.txt 
```
8. Navigate to the src directory and run the main.py file.
```bash
 cd src 
```
```bash
 python main.py 
```

## Acknowledgements

 - [Whisper](https://github.com/openai/whisper)


