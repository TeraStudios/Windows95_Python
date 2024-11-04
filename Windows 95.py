import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
from datetime import datetime
import subprocess

# Initialize pygame for audio playback
pygame.mixer.init()

# Function to handle login and transition to desktop
def on_login():
    # Clear the screen
    for widget in root.winfo_children():
        widget.destroy()

    # Play the login sound
    pygame.mixer.music.load(os.path.join(current_dir, "win95login.mp3"))
    pygame.mixer.music.play()

    # Load the desktop with taskbar only
    load_taskbar()

# Function to set up the taskbar with a Start button
def load_taskbar():
    # Taskbar frame
    taskbar_frame = tk.Frame(root, bg="#C0C0C0")
    taskbar_frame.pack(side="bottom", fill="x")

    # Load the Start button image
    try:
        start_image = Image.open(os.path.join(current_dir, "WinStart.jpg"))
        start_image = start_image.resize((100, int(start_image.height * (100 / start_image.width))), Image.LANCZOS)
        start_photo = ImageTk.PhotoImage(start_image)
    except Exception as e:
        print(f"Error loading Start button image: {e}")
        start_photo = None

    # Start button
    start_button = tk.Button(
        taskbar_frame, image=start_photo, bg="#C0C0C0",
        command=toggle_start_menu
    )
    start_button.image = start_photo  # Keep reference to avoid garbage collection
    start_button.pack(side="left", padx=(10, 0))

    # Clock label on the taskbar
    time_label = tk.Label(taskbar_frame, bg="#C0C0C0", fg="black", font=("Consolas", 12))
    time_label.pack(side="right", padx=(0, 10))
    update_time(time_label)

# Function to toggle the Start menu popup
def toggle_start_menu():
    if hasattr(root, 'start_menu') and root.start_menu.winfo_ismapped():
        root.start_menu.place_forget()
    else:
        create_start_menu()

# Function to create and display the Start menu
def create_start_menu():
    # Main Start menu frame
    root.start_menu = tk.Frame(root, bg="#C0C0C0", borderwidth=2, relief="raised")
    root.start_menu.place(x=10, y=root.winfo_height() - 305)  # Position near the taskbar

    # Sidebar frame for dark grey box
    sidebar_frame = tk.Frame(root.start_menu, bg="#808080", width=40)
    sidebar_frame.pack(side="left", fill="y")

    # Create a canvas for the "Windows" rotated text
    canvas = tk.Canvas(sidebar_frame, width=40, height=200, bg="#808080", highlightthickness=0)
    canvas.pack()

    # Add the rotated "Windows" text to the canvas
    canvas.create_text(
        20, 100, text="Windows", fill="white", font=("Consolas", 16, "bold"),
        angle=90, anchor="center"
    )

    # Menu options inside the Start menu
    menu_options = [
        ("Programs", create_programs_menu),
        ("Documents", lambda: print("Documents clicked")),
        ("Settings", lambda: print("Settings clicked")),
        ("Find", lambda: print("Find clicked")),
        ("Help", lambda: print("Help clicked")),
        ("Run...", lambda: print("Run... clicked")),
        ("Shut Down", lambda: print("Shut Down clicked"))
    ]

    for option_text, command in menu_options:
        tk.Button(root.start_menu, text=option_text, bg="#C0C0C0", fg="black", font=("Consolas", 12), anchor="w", command=command).pack(fill="x", padx=5, pady=5)

# Function to create the "Programs" submenu
def create_programs_menu():
    programs_menu = tk.Menu(root.start_menu, tearoff=0)
    programs_menu.add_command(label="Accessories")
    programs_menu.add_command(label="StartUp")
    programs_menu.add_command(label="MS-DOS Prompt", command=open_msdos_prompt)
    programs_menu.add_command(label="Windows Explorer")
    programs_menu.post(root.winfo_pointerx(), root.winfo_pointery())

# Function to open the MS-DOS Prompt
def open_msdos_prompt():
    dos_window = tk.Toplevel()
    dos_window.title("MS-DOS Prompt")
    dos_window.geometry("800x600")

    output_text = tk.Text(dos_window, height=25, width=80, font=("Courier New", 10))
    output_text.pack(fill="both", expand=True)

    input_field = ttk.Entry(dos_window)
    input_field.pack(fill="x")

    def run_command():
        command = input_field.get()
        input_field.delete(0, tk.END)
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output_text.insert(tk.END, f"{command}\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            output_text.insert(tk.END, f"{command}\nError: {e}")

    input_field.bind("<Return>", lambda event: run_command())

    run_button = tk.Button(dos_window, text="Run", command=run_command)
    run_button.pack()

# Function to update the time label on the taskbar every second
def update_time(label):
    current_time = datetime.now().strftime("%I:%M %p")
    label.config(text=current_time)
    label.after(1000, update_time, label)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Set up the login screen
root = tk.Tk()
root.title("Windows 95")
root.attributes('-fullscreen', True)
root.configure(bg="#00807F")

# Load the welcome screen image
try:
    welcome_image = Image.open(os.path.join(current_dir, "windows95MSG.jpg"))
    welcome_image = welcome_image.resize((int(welcome_image.width * 0.8), int(welcome_image.height * 0.8)), Image.LANCZOS)
    welcome_photo = ImageTk.PhotoImage(welcome_image)
except Exception as e:
    print(f"Error loading welcome screen image: {e}")
    welcome_photo = None

# Display the welcome screen image
if welcome_photo:
    welcome_label = tk.Label(root, image=welcome_photo)
    welcome_label.pack(expand=True)

# Input frame for username and password
input_frame = tk.Frame(root, bg="#C0C0C0", highlightthickness=0)
input_frame.place(relx=0.5, rely=0.5, anchor="center")

# Font style for input labels
font_style = ("Consolas", 17)

# Username label and entry
tk.Label(input_frame, text="Username:", bg="#C0C0C0", fg="black", font=font_style).pack(anchor="w", pady=5)
entry_username = tk.Entry(input_frame, bg="white", fg="black", font=font_style)
entry_username.pack(pady=5)

# Password label and entry
tk.Label(input_frame, text="Password:", bg="#C0C0C0", fg="black", font=font_style).pack(anchor="w", pady=5)
entry_password = tk.Entry(input_frame, show="*", bg="white", fg="black", font=font_style)
entry_password.pack(pady=5)

# Login button
login_button = tk.Button(input_frame, text="Login", command=on_login, bg="#C0C0C0", fg="black", font=font_style)
login_button.pack(pady=10)

# Run the application
root.mainloop()
