# 🐾 PawTrace

**Mouse Movement Recorder & Visualization Tool**

![Python](https://img.shields.io/badge/python-3.11-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

PawTrace is a Python GUI application that records mouse movement and visualizes it through an animated replay and trajectory graph. It allows users to capture cursor behavior, replay it visually, and export the movement data for later analysis.

---

## Features

- Record real-time mouse movement
- Replay cursor movement with animation
- Export recordings to JSON
- Load previous recordings
- Generate a movement trajectory graph
- Export visualization as an image

---
##Demo
![PawTrace Demo](PawTrace/Screenshot%202026-03-14%20062333.png)


---
## Requirements

- Python 3.11
- pip

Libraries used:

- pynput
- pygame
- matplotlib
- tkinter (included with Python)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/PawTrace.git
cd PawTrace
```

Install dependencies:
```bash
pip install pynput pygame matplotlib
Run the Application
python PawTrace.py
```

The graphical interface will open and allow you to record and replay mouse movement.

Output

Mouse recordings are stored in JSON format:

[x_position, y_position, timestamp]

The movement visualization is exported as:
```bash
pawtrace_result.png
```
