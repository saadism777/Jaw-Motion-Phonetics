import os
import signal
import socket
import sys
import time
from subprocess import Popen

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDesktopWidget,
                             QFileDialog, QHBoxLayout, QLabel, QVBoxLayout)

from keywords import *

#Initializign variables
front_proc = None
phonetics = None
path = None
marker_diameter = None

class MainWindow(QtWidgets.QWidget):
    
    def start_or_stop_processes(self):
        print(default_output_filename)
        global front_proc
        global marker_diameter
        marker_diameter = float(self.entry.text())
    
        # Use the face_width value in your application
        print(f"The marker diameter is: {marker_diameter}mm")
        
        # Start the two subprocesses and return the objects
        front_proc = Popen(['python', 'face_app.py', str(path), str(default_output_filename), str(marker_diameter)])
        #phonetics = Popen(['python', 'phonetics.py', str(front_path), str(default_output_filename)])

    def __init__(self):
        super().__init__()
        # Set the window icon for the application
        icon_path = '..\images\logo.ico'  # Replace with the path to your icon file
        self.setWindowIcon(QIcon(icon_path))
        self.resize(300, 100)
        self.center()
        self.setWindowTitle("Dental Loops SnP")
        try:
            self.label = QtWidgets.QLabel("Enter tracking marker diameter value(mm):")
            self.entry = QtWidgets.QLineEdit()
            self.entry.setText("15")

            self.labelB = QLabel("Select Input File: ")
            self.buttonB = QtWidgets.QPushButton('Browse File')
            self.buttonB.clicked.connect(self.showFileDialog)

            font = QtGui.QFont()
            font.setPointSize(12)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setFont(font)
            self.buttonS = QtWidgets.QPushButton("Settings", clicked=self.loadSettings)
            self.button = QtWidgets.QPushButton("OK", clicked=self.start_or_stop_processes)
            self.button2 = QtWidgets.QPushButton("Exit", clicked=self.close_app)
        except Exception as e:
            print("Error: " + str(e))
     
        # Set a default image for the thumbnail label (optional)

       # Create a QLabel to show the thumbnail image
        self.thumbnail_label = QLabel(self)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        default_thumbnail = QPixmap('../images/thumbnail.jpg')
        default_thumbnail = default_thumbnail.scaled(200, 100)
        self.thumbnail_label.setPixmap(default_thumbnail)
        layout = QVBoxLayout(self)
        # Add the thumbnail label to the layout
        layout.addWidget(self.thumbnail_label)
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.labelB)
        layout.addWidget(self.buttonB)
        layout.addWidget(self.buttonS)
        layout.addWidget(self.button)
        
        layout.addWidget(self.button2)
 
        

        

    def generate_video_thumbnail(self, filepath):
        try:
            # Open the video file
            cap = cv2.VideoCapture(filepath)

            # Read the first frame
            ret, frame = cap.read()

            # Release the video capture object
            cap.release()

            # Return the first frame as the thumbnail
            return frame
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return None
        
    def convert_to_qpix(self, frame):
        # Resize the frame to the desired dimensions (200x100)
        frame_resized = cv2.resize(frame, (200, 100))
        # Convert the OpenCV frame to QImage
        image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        
        # Convert QImage to QPixmap
        return QPixmap.fromImage(q_image)   
      
    def loadSettings(self):
        # Import the necessary dictionaries from keywords.py
        
        
        # Launch keywords.py to edit the dictionaries
        settings = Popen(['python', 'settings.py'])
        settings.wait()  # Wait for the keywords.py to close


    def showFileDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.fileSelected.connect(self.fileSelectedAction)
        file_dialog.exec_()
    
    def fileSelectedAction(self, filepath):
        # Do something with the filepath
        global path, default_output_filename
        path=filepath
        self.labelB.setText(f"Selected file: {path}")
        # Extract the path from the last backslash up to the file extension
        filename = os.path.basename(filepath)
        index_of_last_backslash = filename.rfind("\\")
        index_of_extension = filename.rfind(".")
        # Generate the thumbnail using OpenCV
        thumbnail = self.generate_video_thumbnail(filepath)

        # Check if the thumbnail is valid
        if thumbnail is not None:
            # Convert the thumbnail to a QPixmap and set it as the QLabel's image
            thumbnail_pixmap = self.convert_to_qpix(thumbnail)
            self.thumbnail_label.setPixmap(thumbnail_pixmap)
        else:
            # If the thumbnail cannot be generated, display a placeholder image or show an error message
            placeholder_thumbnail = QPixmap('../images/thumbnail.jpg')
            placeholder_thumbnail = placeholder_thumbnail.scaled(100, 100, Qt.KeepAspectRatio)
            self.thumbnail_label.setPixmap(placeholder_thumbnail)

        if index_of_last_backslash != -1 and index_of_extension != -1:
            default_output_filename = filename[index_of_last_backslash + 1:index_of_extension]
        else:
            # If there's no backslash or no file extension, set the entire filename as default
            default_output_filename = filename
 
    def center(self):
        # Get the geometry of the screen
        screen = QDesktopWidget().screenGeometry()

        # Calculate the center position of the screen
        center_x = screen.width() // 2
        center_y = screen.height() // 2

        # Move the window to the center of the screen
        self.move(center_x - self.width() // 2, center_y - self.height() // 2)


    
    def close_app(self):
        # Stop the two subprocesses
        #if front_proc and side_proc is not None:
        #    start_or_stop_processes(False)
        timer = QTimer(self)
        timer.timeout.connect(QApplication.quit)
        timer.start(500)

    def get_entry_value(self):
        global marker_diameter
        marker_diameter = float(self.entry.text())
    
        # Use the face_width value in your application
        print(f"The marker diameter is: {marker_diameter}mm")
        # Launch both apps
        # Example usage:
        self.start_or_stop_processes()
        #self.start_subprocess()
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
