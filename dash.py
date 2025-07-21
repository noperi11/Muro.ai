import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import os
import signal

# Paths ke project (sesuaikan)
FASTAPI_DIR = r"./backend"
REACT_DIR   = r"./frontend"

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control Panel — FastAPI & React")
        self.geometry("700x500")

        # Controls frame
        self.frm_controls = tk.Frame(self)
        self.frm_controls.pack(pady=10)

        # FastAPI buttons
        tk.Label(self.frm_controls, text="FastAPI Backend:").grid(row=0, column=0, padx=5)
        self.btn_start_api = tk.Button(self.frm_controls, text="Start", command=self.start_api)
        self.btn_start_api.grid(row=0, column=1, padx=5)
        self.btn_stop_api = tk.Button(self.frm_controls, text="Stop", command=self.stop_api, state=tk.DISABLED)
        self.btn_stop_api.grid(row=0, column=2, padx=5)

        # React buttons
        tk.Label(self.frm_controls, text="React Frontend:").grid(row=1, column=0, padx=5)
        self.btn_start_react = tk.Button(self.frm_controls, text="Start", command=self.start_react)
        self.btn_start_react.grid(row=1, column=1, padx=5)
        self.btn_stop_react = tk.Button(self.frm_controls, text="Stop", command=self.stop_react, state=tk.DISABLED)
        self.btn_stop_react.grid(row=1, column=2, padx=5)

        # Log area
        self.log_widget = scrolledtext.ScrolledText(self, state='disabled')
        self.log_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Process handles
        self.api_process = None
        self.react_process = None

    def log(self, message):
        self.log_widget.config(state='normal')
        self.log_widget.insert(tk.END, message + "\n")
        self.log_widget.see(tk.END)
        self.log_widget.config(state='disabled')

    def start_api(self):
        if self.api_process:
            messagebox.showinfo("Info", "FastAPI sudah berjalan.")
            return
        cmd = ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
        self.api_process = subprocess.Popen(
            cmd, cwd=FASTAPI_DIR,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        threading.Thread(target=self.stream_logs, args=(self.api_process, "API"), daemon=True).start()
        self.btn_start_api.config(state=tk.DISABLED)
        self.btn_stop_api.config(state=tk.NORMAL)
        self.log("[API] Memulai FastAPI server...")

    def stop_api(self):
        if not self.api_process:
            return
        self.log("[API] Menghentikan FastAPI server...")
        self.api_process.send_signal(signal.SIGINT)
        self.api_process.wait()
        self.api_process = None
        self.btn_start_api.config(state=tk.NORMAL)
        self.btn_stop_api.config(state=tk.DISABLED)
        self.log("[API] FastAPI server dihentikan.")

    def start_react(self):
        if self.react_process:
            messagebox.showinfo("Info", "React sudah berjalan.")
            return
        cmd = ["npm", "start"]
        self.react_process = subprocess.Popen(
            cmd, cwd=REACT_DIR,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        threading.Thread(target=self.stream_logs, args=(self.react_process, "React"), daemon=True).start()
        self.btn_start_react.config(state=tk.DISABLED)
        self.btn_stop_react.config(state=tk.NORMAL)
        self.log("[React] Memulai React frontend...")

    def stop_react(self):
        if not self.react_process:
            return
        self.log("[React] Menghentikan React frontend...")
        self.react_process.send_signal(signal.SIGINT)
        self.react_process.wait()
        self.react_process = None
        self.btn_start_react.config(state=tk.NORMAL)
        self.btn_stop_react.config(state=tk.DISABLED)
        self.log("[React] React frontend dihentikan.")

    def stream_logs(self, process, tag):
        for line in process.stdout:
            self.log(f"[{tag}] {line.rstrip()}")
        process.stdout.close()

if __name__ == "__main__":
    Dashboard().mainloop()
