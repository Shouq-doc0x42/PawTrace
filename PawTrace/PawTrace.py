import tkinter as tk
from tkinter import filedialog
from pynput.mouse import Controller
import threading
import time
import json
import pygame
import matplotlib.pyplot as plt
import math
import hashlib
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

recording = False
mouse_data = []
start_time = None

record_start_time = None
record_end_time = None

mouse_controller = Controller()

# live analysis variables
last_x = None
last_y = None
last_t = None
current_speed = 0

# FIX: initialize hashes
json_sha256 = "N/A"
graph_sha256 = "N/A"

# -------------------------
# RECORD MOUSE
# -------------------------

def record_mouse():
    global recording, mouse_data, last_x, last_y, last_t, current_speed

    while recording:
        x, y = mouse_controller.position
        t = time.time() - start_time

        mouse_data.append((x, y, t))

        if last_x is not None:
            dx = x - last_x
            dy = y - last_y
            dt = t - last_t if t - last_t != 0 else 0.001

            distance = (dx**2 + dy**2)**0.5
            current_speed = distance / dt

        last_x = x
        last_y = y
        last_t = t

        time.sleep(0.005)


def start_recording():
    global recording, mouse_data, start_time, record_start_time

    mouse_data = []
    recording = True
    start_time = time.time()

    record_start_time = time.strftime("%Y-%m-%d %H:%M:%S")

    status_label.config(text="Recording...")

    threading.Thread(target=record_mouse, daemon=True).start()


def stop_recording():
    global recording, record_end_time
    recording = False

    record_end_time = time.strftime("%Y-%m-%d %H:%M:%S")

    status_label.config(text=f"Recorded {len(mouse_data)} points")


# -------------------------
# HASH GENERATING
# -------------------------

def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


# -------------------------
# EXPORT DATA
# -------------------------

def export_data():
    global json_sha256

    if not mouse_data:
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON File", "*.json")]
    )

    data_package = {
        "start_time": record_start_time,
        "end_time": record_end_time,
        "points": mouse_data
    }

    with open(file_path, "w") as f:
        json.dump(data_package, f, indent=4)

    json_sha256 = calculate_sha256(file_path)

    status_label.config(text="Exported successfully")


# -------------------------
# LOAD DATA
# -------------------------

def load_data():
    global mouse_data

    file_path = filedialog.askopenfilename(
        filetypes=[("JSON File", "*.json")]
    )

    with open(file_path) as f:
        data = json.load(f)

    mouse_data = data["points"]

    status_label.config(text=f"Loaded {len(mouse_data)} points")


# -------------------------
# FINAL GRAPH
# -------------------------

def draw_final_result():
    global graph_sha256

    if not mouse_data:
        return

    xs = [p[0] for p in mouse_data]
    ys = [p[1] for p in mouse_data]

    plt.figure(figsize=(10,7))

    plt.plot(xs, ys, color="green", linewidth=2)

    plt.scatter(xs[0], ys[0], color="blue", label="Start")
    plt.scatter(xs[-1], ys[-1], color="red", label="End")

    plt.title("PawTrace Mouse Movement Path")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")

    plt.xlim(0,1920)
    plt.ylim(0,1080)

    plt.gca().invert_yaxis()

    plt.grid(True)
    plt.legend()

    plt.savefig("pawtrace_result.png")

    # FIX: generate hash
    graph_sha256 = calculate_sha256("pawtrace_result.png")

    plt.close()

# -------------------------
# CASE ID GENERATING
# -------------------------

def generate_case_id():
    return "PT-" + time.strftime("%Y-%m-%d-%H%M%S")

# -------------------------
# PDF REPORT
# -------------------------

def generate_report():

    if not mouse_data:
        return

    case_id = generate_case_id()
    generated_time = time.strftime("%Y-%m-%d %H:%M:%S")

    total_distance = 0
    max_speed = 0

    for i in range(1, len(mouse_data)):
        x1, y1, t1 = mouse_data[i-1]
        x2, y2, t2 = mouse_data[i]

        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        time_diff = t2 - t1 if (t2 - t1) != 0 else 0.001

        speed = distance / time_diff

        total_distance += distance
        max_speed = max(max_speed, speed)

    duration = mouse_data[-1][2]
    avg_speed = total_distance / duration if duration != 0 else 0

    styles = getSampleStyleSheet()
    elements = []

    # -------------------------
    # LOGO
    # -------------------------
    if os.path.exists("8998260.png"):
        elements.append(Image("8998260.png", width=50, height=50))

    elements.append(Spacer(1,10))

    # -------------------------
    # HEADER
    # -------------------------
    elements.append(Paragraph("PawTrace Behavioral Analysis Report", styles['Title']))
    elements.append(Spacer(1,10))

    elements.append(Paragraph(f"<b>Case ID:</b> {case_id}", styles['Normal']))
    elements.append(Paragraph("<b>Investigator:</b> Shouq", styles['Normal']))
    elements.append(Paragraph("<b>Tool:</b> PawTrace v1.0", styles['Normal']))
    elements.append(Paragraph(f"<b>Generated:</b> {generated_time}", styles['Normal']))

    elements.append(Spacer(1,20))

    # -------------------------
    # RECORDING INFO
    # -------------------------
    elements.append(Paragraph("<b>Recording Information</b>", styles['Heading2']))
    elements.append(Paragraph(f"Recording Start: {record_start_time}", styles['Normal']))
    elements.append(Paragraph(f"Recording End: {record_end_time}", styles['Normal']))
    elements.append(Paragraph(f"Duration: {duration:.2f} seconds", styles['Normal']))
    elements.append(Paragraph(f"Points Captured: {len(mouse_data)}", styles['Normal']))

    elements.append(Spacer(1,20))

    # -------------------------
    # MOVEMENT ANALYSIS
    # -------------------------
    elements.append(Paragraph("<b>Movement Analysis</b>", styles['Heading2']))
    elements.append(Paragraph(f"Total Distance: {total_distance:.2f} pixels", styles['Normal']))
    elements.append(Paragraph(f"Average Speed: {avg_speed:.2f} pixels/sec", styles['Normal']))
    elements.append(Paragraph(f"Max Speed: {max_speed:.2f} pixels/sec", styles['Normal']))

    elements.append(Spacer(1,20))

    # -------------------------
    # HASHES
    # -------------------------
    elements.append(Paragraph("<b>Evidence Integrity (SHA256)</b>", styles['Heading2']))
    elements.append(Paragraph(f"JSON Dataset SHA256: {json_sha256}", styles['Normal']))
    elements.append(Paragraph(f"Graph Image SHA256: {graph_sha256}", styles['Normal']))

    elements.append(Spacer(1,20))

    # -------------------------
    # GRAPH
    # -------------------------
    if os.path.exists("pawtrace_result.png"):
        elements.append(Image("pawtrace_result.png", width=300, height=180))

    pdf = SimpleDocTemplate("pawtrace_report.pdf", pagesize=letter)
    pdf.build(elements)

# -------------------------
# REPLAY ANIMATION
# -------------------------

def replay_animation():

    if not mouse_data:
        return

    pygame.init()

    screen = pygame.display.set_mode((1920,1080))
    pygame.display.set_caption("PawTrace Replay")

    running = True
    i = 0
    path_points = []

    while running and i < len(mouse_data):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((20,20,20))

        x, y, t = mouse_data[i]

        px = int(x)
        py = int(y)

        path_points.append((px,py))

        if len(path_points) > 1:
            pygame.draw.lines(screen,(0,255,120),False,path_points,3)

        pygame.draw.circle(screen,(255,80,80),(px,py),6)

        pygame.display.update()

        if i < len(mouse_data)-1:
            delay = mouse_data[i+1][2] - t
            time.sleep(delay)

        i += 1

    pygame.quit()

    draw_final_result()
    generate_report()


def replay_thread():
    threading.Thread(target=replay_animation).start()


# -------------------------
# LIVE STATUS PANEL
# -------------------------

def update_status_panel():

    if recording:
        duration = time.time() - start_time

        status_text = f"""
Status: Recording

Points Captured: {len(mouse_data)}
Duration: {duration:.2f} sec
Mouse Speed: {current_speed:.2f} px/sec
"""
    else:
        status_text = f"""
Status: Idle

Points Captured: {len(mouse_data)}
Mouse Speed: {current_speed:.2f} px/sec
"""

    live_status_label.config(text=status_text)

    root.after(200, update_status_panel)


# -------------------------
# GUI
# -------------------------

root = tk.Tk()
root.title("PawTrace - Mouse Behavior Recorder")
root.iconbitmap("5584155.ico")

root.geometry("320x520")

btn_record = tk.Button(root,text="▶ Start Recording",width=24,height=2,command=start_recording)
btn_record.pack(pady=8)

btn_stop = tk.Button(root,text="⏹ Stop Recording",width=24,height=2,command=stop_recording)
btn_stop.pack(pady=8)

btn_export = tk.Button(root,text="💾 Export Recording",width=24,height=2,command=export_data)
btn_export.pack(pady=8)

btn_load = tk.Button(root,text="📂 Load Recording",width=24,height=2,command=load_data)
btn_load.pack(pady=8)

btn_replay = tk.Button(root,text="🎬 Replay Animation",width=24,height=2,command=replay_thread)
btn_replay.pack(pady=8)

status_label = tk.Label(root,text="")
status_label.pack(pady=6)

status_title = tk.Label(root,text="Live Status",font=("Arial",10,"bold"))
status_title.pack()

live_status_label = tk.Label(root,text="Status: Idle",justify="left",fg="blue")
live_status_label.pack()

update_status_panel()

root.mainloop()