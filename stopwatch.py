import tkinter as tk
import time

# Global Variables
running = False
start_time = 0
elapsed_time = 0
lap_number = 1

def update_timer():
    if running:
        current_time = time.time()
        total = current_time - start_time + elapsed_time

        # Format with milliseconds
        ms = int((total - int(total)) * 100)
        formatted = time.strftime("%H:%M:%S", time.gmtime(total)) + f".{ms:02d}"

        label.config(text=formatted)
        root.after(10, update_timer)  # Update every 10 ms for smooth UI

def start():
    global running, start_time
    if not running:
        running = True
        start_time = time.time()
        update_timer()

def pause():
    global running, elapsed_time
    if running:
        running = False
        elapsed_time += time.time() - start_time

def resume():
    global running, start_time
    if not running:
        running = True
        start_time = time.time()
        update_timer()

def reset():
    global running, elapsed_time, lap_number
    running = False
    elapsed_time = 0
    lap_number = 1
    label.config(text="00:00:00.00")
    lap_list.delete(0, tk.END)

def add_lap():
    global lap_number
    if running:
        lap_time = label.cget("text")
        lap_list.insert(tk.END, f"Lap {lap_number}: {lap_time}")
        save_lap_to_file(lap_number, lap_time)
        lap_number += 1

def save_lap_to_file(num, lap_time):
    with open("lap_history.txt", "a") as file:
        file.write(f"Lap {num}: {lap_time}\n")

# ------- UI Enhancements -------- #

def on_enter(e):
    e.widget["bg"] = "#00ffaa"

def on_leave(e):
    e.widget["bg"] = "#00cc99"

# GUI Setup
root = tk.Tk()
root.title("Neon Digital Stopwatch")
root.geometry("450x520")
root.config(bg="#0a0a0a")

# Timer Display
label = tk.Label(root, text="00:00:00.00", font=("Consolas", 48, "bold"),
                 fg="#00ffcc", bg="#0a0a0a")
label.pack(pady=20)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#0a0a0a")
btn_frame.pack()

button_style = {"width": 10, "height": 2, "bg": "#00cc99",
                "fg": "black", "bd": 0, "font": ("Arial", 12, "bold")}

btn_names = [("Start", start), ("Pause", pause), ("Resume", resume),
             ("Reset", reset), ("Lap", add_lap)]

buttons = []

row = 0
col = 0
for name, cmd in btn_names:
    btn = tk.Button(btn_frame, text=name, command=cmd, **button_style)
    btn.grid(row=row, column=col, padx=10, pady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    buttons.append(btn)

    col += 1
    if col == 2:
        row += 1
        col = 0

# Lap Listbox
lap_list = tk.Listbox(root, height=10, fg="#00ffcc", bg="#111",
                      font=("Consolas", 12))
lap_list.pack(fill="both", padx=20, pady=20)

# Keyboard Shortcuts
root.bind("s", lambda e: start())
root.bind("p", lambda e: pause())
root.bind("r", lambda e: resume())
root.bind("l", lambda e: add_lap())
sroot.bind("x", lambda e: reset())

root.mainloop()
