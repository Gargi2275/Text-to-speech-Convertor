import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import pyttsx3
import os

# ------------------ INITIALIZATION ------------------

app = Tk()
app.title("Voice Generator")
app.state("zoomed")  # Fullscreen (maximized)
app.configure(bg="#F9F4EF")

# ------------------ LOGIC FUNCTIONS ------------------

def get_configured_engine():
    engine = pyttsx3.init()

    # Speed
    rate_option = rate_dropdown.get()
    rate_map = {'Fast': 250, 'Normal': 150, 'Slow': 60}
    engine.setProperty('rate', rate_map.get(rate_option, 150))

    # Voice
    voices = engine.getProperty('voices')
    voice_type = voice_dropdown.get()

    chosen_voice = None
    for voice in voices:
        if voice_type.lower() in voice.name.lower():
            chosen_voice = voice.id
            break

    if not chosen_voice:
        if voice_type == 'Male':
            chosen_voice = voices[0].id
        else:
            chosen_voice = voices[1].id if len(voices) > 1 else voices[0].id

    engine.setProperty('voice', chosen_voice)
    return engine


def play_voice():
    content = input_box.get(1.0, END).strip()
    if not content:
        messagebox.showwarning("Warning", "Please enter some text first!")
        return

    try:
        engine = get_configured_engine()
        engine.say(content)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        messagebox.showerror("Error", f"Speech Error: {e}")


def save_audio():
    content = input_box.get(1.0, END).strip()
    if not content:
        messagebox.showwarning("Warning", "Please enter some text first!")
        return

    directory = filedialog.askdirectory()
    if directory:
        try:
            os.chdir(directory)
            engine = get_configured_engine()
            filename = "audio.mp3"
            engine.save_to_file(content, filename)
            engine.runAndWait()
            messagebox.showinfo("Success", f"File saved successfully in {directory}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")


# ------------------ HEADER ------------------

header = Frame(app, bg="#292C7B", height=100)
header.pack(fill="x")

Label(
    header,
    text="VOICE GENERATOR",
    font=("Arial", 26, "bold"),
    bg="#292C7B",
    fg="white"
).pack(pady=25)


# ------------------ MAIN CONTAINER ------------------

main_frame = Frame(app, bg="#F9F4EF")
main_frame.pack(fill="both", expand=True, padx=40, pady=30)


# ------------------ LEFT: TEXT AREA ------------------

text_frame = Frame(main_frame, bg="white", bd=2, relief=GROOVE)
text_frame.pack(side="left", fill="both", expand=True, padx=20)

scrollbar = Scrollbar(text_frame)
scrollbar.pack(side=RIGHT, fill=Y)

input_box = Text(
    text_frame,
    font=("Roboto", 16),
    bg="white",
    wrap=WORD,
    yscrollcommand=scrollbar.set
)
input_box.pack(expand=True, fill=BOTH)
scrollbar.config(command=input_box.yview)


# ------------------ RIGHT: CONTROLS ------------------

control_frame = Frame(main_frame, bg="#F9F4EF")
control_frame.pack(side="right", fill="y", padx=40)

# Voice Dropdown
Label(control_frame, text="VOICE", font=("Arial", 14, "bold"), bg="#F9F4EF").pack(anchor="w", pady=(10, 5))
voice_dropdown = Combobox(control_frame, values=['Male', 'Female'], font=('Arial', 12), state='readonly', width=15)
voice_dropdown.pack(anchor="w", pady=5)
voice_dropdown.set('Male')

# Speed Dropdown
Label(control_frame, text="SPEED", font=("Arial", 14, "bold"), bg="#F9F4EF").pack(anchor="w", pady=(20, 5))
rate_dropdown = Combobox(control_frame, values=['Slow', 'Normal', 'Fast'], font=('Arial', 12), state='readonly', width=15)
rate_dropdown.pack(anchor="w", pady=5)
rate_dropdown.set('Normal')

# Buttons
speak_button = Button(
    control_frame,
    text="Speak",
    width=15,
    height=2,
    bg="white",
    font=("Arial", 12, "bold"),
    command=play_voice
)
speak_button.pack(pady=30)

save_button = Button(
    control_frame,
    text="Save",
    width=15,
    height=2,
    bg="white",
    font=("Arial", 12, "bold"),
    command=save_audio
)
save_button.pack(pady=10)


# ------------------ RUN APP ------------------

app.mainloop()
