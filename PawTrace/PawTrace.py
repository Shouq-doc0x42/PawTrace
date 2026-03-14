import tkinter as tk
from tkinter import filedialog
from pynput.mouse import Controller
import threading
import time
import json
import pygame
import matplotlib.pyplot as plt

recording = False
mouse_data = []
start_time = None

mouse_controller = Controller()

# -------------------------
# RECORD MOUSE (HIGH SAMPLING)
# -------------------------

def record_mouse():
    global recording, mouse_data

    while recording:
        x, y = mouse_controller.position
        t = time.time() - start_time
        mouse_data.append((x, y, t))

        time.sleep(0.005)  # 200Hz sampling


def start_recording():
    global recording, mouse_data, start_time

    mouse_data = []
    recording = True
    start_time = time.time()

    status_label.config(text="Recording...")

    threading.Thread(target=record_mouse, daemon=True).start()


def stop_recording():
    global recording
    recording = False
    status_label.config(text=f"Recorded {len(mouse_data)} points")


# -------------------------
# EXPORT DATA
# -------------------------

def export_data():
    if not mouse_data:
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON File", "*.json")]
    )

    with open(file_path, "w") as f:
        json.dump(mouse_data, f)

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
        mouse_data = json.load(f)

    status_label.config(text=f"Loaded {len(mouse_data)} points")


# -------------------------
# FINAL GRAPH VISUALIZATION
# -------------------------

def draw_final_result():

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
    plt.show()


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

        screen.fill((20,20,20))  # dark background

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


def replay_thread():
    threading.Thread(target=replay_animation).start()


# -------------------------
# GUI
# -------------------------

root = tk.Tk()
root.title("PawTrace - Mouse Behavior Recorder")
root.iconbitmap("5584155.ico")

root.geometry("320x380")

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


root.mainloop()