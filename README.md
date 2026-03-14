🐾 PawTrace

Mouse Movement Recorder & Visualization Tool

PawTrace is a Python GUI application that records mouse movement and visualizes it through an animated replay and trajectory graph. It allows users to capture cursor behavior, replay it visually, and export the movement data for later analysis.

✨ Features

Record real-time mouse movement

Animated replay of cursor movement

Export recordings to JSON

Load previous recordings

Generate a movement trajectory graph

Export visualization as an image

🛠 Requirements

Python 3.11

pip

Libraries used:

pynput

pygame

matplotlib

tkinter (included with Python)

📦 Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/PawTrace.git
cd PawTrace

Install dependencies:

pip install pynput pygame matplotlib
▶️ Run the Application
python PawTrace.py

The graphical interface will open and allow you to record and replay mouse movement.

📊 Output

Mouse recordings are stored as JSON:

[x_position, y_position, timestamp]

The visualization graph is exported as:

pawtrace_result.png
📁 Project Structure
PawTrace
│
├── PawTrace.py
├── requirements.txt
└── README.md
