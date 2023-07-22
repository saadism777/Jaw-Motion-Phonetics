import os
import signal
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication,QLabel,QDesktopWidget,QHBoxLayout, QCheckBox, QVBoxLayout, QFileDialog
import socket
import time
import sys
from subprocess import Popen
from PyQt5.QtCore import QTimer, Qt

#Initializign variables
front_proc = None
phonetics = None
front_path = None


class MainWindow(QtWidgets.QWidget):
    def start_or_stop_processes(start):
        print(default_output_filename)
        global front_proc
        if start:
            # Start the two subprocesses and return the objects
            front_proc = Popen(['python', 'app.py', str(front_path), str(default_output_filename)])
            #phonetics = Popen(['python', 'phonetics.py', str(front_path)])
        else:
            print("Missing values")

    def __init__(self):
        super().__init__()
        self.resize(300, 300)
        self.center()
        self.setWindowTitle("Dental Loops SnP")

        
        self.labelB = QLabel("Select Input File: ")
        self.buttonB = QtWidgets.QPushButton('Browse File')
        self.buttonB.clicked.connect(self.showFileDialog)


        font = QtGui.QFont()
        font.setPointSize(16)

        self.button = QtWidgets.QPushButton("OK", clicked=self.start_or_stop_processes)
        self.button2 = QtWidgets.QPushButton("Exit", clicked=self.close_app)
     

        layout = QVBoxLayout(self)
        

        layout.addWidget(self.labelB)
        layout.addWidget(self.buttonB)
       
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

    def showFileDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.fileSelected.connect(self.fileSelectedAction)
        file_dialog.exec_()
    
    def fileSelectedAction(self, filepath):
        # Do something with the filepath
        global front_path, default_output_filename
        front_path=filepath
        self.labelB.setText(f"Selected file: {front_path}")
    # Extract the path from the last backslash up to the file extension
        filename = os.path.basename(filepath)
        index_of_last_backslash = filename.rfind("\\")
        index_of_extension = filename.rfind(".")
        
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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
