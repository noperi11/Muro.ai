import tkinter as tk
import subprocess
import os
import shutil
import threading
import signal

# === Lokasi Folder Proyek ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FASTAPI_DIR = os.path.join(BASE_DIR, "backend")
REACT_DIR = os.path.join(BASE_DIR, "frontend")

fastapi_process = None
react_process = None

# === Fungsi Menjalankan FastAPI ===
def start_fastapi():
    global fastapi_process
    if not os.path.exists(FASTAPI_DIR):
        log("[ERROR] Folder FastAPI tidak ditemukan.")
        return

    def run():
        global fastapi_process
        if fastapi_process is None:
            log("Menjalankan FastAPI...")
            fastapi_process = subprocess.Popen(
                ["python", "-m", "uvicorn", "backend:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
                cwd=FASTAPI_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            while True:
                line = fastapi_process.stdout.readline()
                if not line:
                    break
                log(line)

    threading.Thread(target=run, daemon=True).start()

def stop_fastapi():
    global fastapi_process
    if fastapi_process:
        try:
            os.kill(fastapi_process.pid, signal.CTRL_C_EVENT)
            log("FastAPI dihentikan.")
        except Exception as e:
            log(f"[ERROR] Gagal menghentikan FastAPI: {e}")
        fastapi_process = None

# === Fungsi Menjalankan React (Dev) ===
def start_react():
    global react_process
    if not os.path.exists(REACT_DIR):
        log("[ERROR] Folder React tidak ditemukan.")
        return

    def run():
        global react_process
        if react_process is None:
            log("Menjalankan React Dev Server...")
            npm = shutil.which("npm")
            if npm is None:
                log("[ERROR] npm tidak ditemukan di PATH.")
                return
            react_process = subprocess.Popen(
                [npm, "start"],
                cwd=REACT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            while True:
                line = react_process.stdout.readline()
                if not line:
                    break
                log(line)

    threading.Thread(target=run, daemon=True).start()

def stop_react():
    global react_process
    if react_process:
        try:
            os.kill(react_process.pid, signal.CTRL_C_EVENT)
            log("React dihentikan.")
        except Exception as e:
            log(f"[ERROR] Gagal menghentikan React: {e}")
        react_process = None

# === Log Ke Output GUI ===
def log(message):
    def append_log():
        if output_text.winfo_exists():
            output_text.insert(tk.END, message + "\n")
            output_text.see(tk.END)
    try:
        root.after(0, append_log)
    except RuntimeError:
        pass

# === GUI Setup ===
root = tk.Tk()
root.title("Control Panel - FastAPI & React (Dev Mode)")
root.geometry("800x500")

frame = tk.Frame(root)
frame.pack(pady=10)

# === Tombol FastAPI ===
tk.Label(frame, text="FastAPI").grid(row=0, column=0, padx=10)
tk.Button(frame, text="Start", command=start_fastapi, bg="lightgreen").grid(row=0, column=1, padx=5)
tk.Button(frame, text="Stop", command=stop_fastapi, bg="tomato").grid(row=0, column=2, padx=5)

# === Tombol React Dev Server ===
tk.Label(frame, text="React (Dev)").grid(row=1, column=0, padx=10)
tk.Button(frame, text="Start", command=start_react, bg="lightgreen").grid(row=1, column=1, padx=5)
tk.Button(frame, text="Stop", command=stop_react, bg="tomato").grid(row=1, column=2, padx=5)

# === Output Console ===
output_text = tk.Text(root, height=25, bg="#111", fg="#0f0", insertbackground="white")
output_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()
