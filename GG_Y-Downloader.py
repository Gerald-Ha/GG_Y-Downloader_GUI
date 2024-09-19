import os
import json
import time
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from threading import Thread
from yt_dlp import YoutubeDL

current_download = None
download_thread = None
cancel_download = False
total_filesize = 0
url_cleared = False

settings_file = "settings.json"

fake_progress_thread = None
fake_progress_running = False

def create_download_directory(path=None):
    if path:
        download_path = path
    else:
        download_path = os.path.join(os.getcwd(), "Media-Youtube")
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return download_path

def fake_progress():
    global fake_progress_running, progress_var
    progress_steps = [3, 15, 25, 37, 50, 70]
    time_intervals = [7, 6, 10, 15, 20]
    wait_times = [2, 1, 1, 1, 1]

    fake_progress_running = True

    for step, interval, wait in zip(progress_steps, time_intervals, wait_times):
        if not fake_progress_running:
            break
        while progress_var.get() < step:
            progress_var.set(min(progress_var.get() + 1, step))
            progress_label.config(text=f"{progress_var.get():.1f}%")
            root.update_idletasks()
            time.sleep(wait)
        time.sleep(interval)

    while fake_progress_running and progress_var.get() < 100:
        root.update_idletasks()
        time.sleep(0.5)

def progress_hook(d):
    global cancel_download, fake_progress_running, total_filesize
    if cancel_download:
        fake_progress_running = False
        raise Exception("Download Aborted by User")
    
    if d['status'] == 'finished':
        progress_var.set(100)
        progress_label.config(text="100%")
        fake_progress_running = False

def download_youtube_video(url, download_type):
    global cancel_download, total_filesize
    download_path = create_download_directory(selected_path.get())

    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_color': True
    }

    if download_type == "video":
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    elif download_type == "audio":
        ydl_opts['format'] = 'bestaudio'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif download_type == "both":
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            if str(e) != "Download Aborted by User":
                messagebox.showerror("Error", f"Failed to download video: {e}")
            return False

        audio_opts = {
            'format': 'bestaudio',
            'outtmpl': os.path.join(download_path, '%(title)s-audio.mp3'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_color': True,
            'progress_hooks': [progress_hook]
        }
        try:
            with YoutubeDL(audio_opts) as ydl_audio:
                ydl_audio.download([url])
            return True
        except Exception as e:
            if str(e) != "Download Aborted by User":
                messagebox.showerror("Error", f"Failed to download audio: {e}")
            return False
        return True

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
    except Exception as e:
        if str(e) != "Download Aborted by User":
            messagebox.showerror("Error", f"Failed to download: {e}")
        return False

def handle_download():
    global download_thread, cancel_download, url_cleared, fake_progress_running
    url = url_entry.get()
    download_type = var.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid YouTube URL.")
        return
    progress_var.set(0)
    progress_label.config(text="0%")
    cancel_download = False
    url_cleared = False

    global fake_progress_thread
    fake_progress_thread = Thread(target=fake_progress)
    fake_progress_thread.start()

    download_button.config(state=tk.DISABLED)
    cancel_button.config(state=tk.NORMAL)

    success = download_youtube_video(url, download_type)
    if success:
        fake_progress_running = False
        messagebox.showinfo("Download Complete", "Download completed successfully!")
        progress_var.set(100)
        progress_label.config(text="100%")
        add_to_download_list(url)

    download_button.config(state=tk.NORMAL)
    cancel_button.config(state=tk.DISABLED)
    fake_progress_running = False

def start_download():
    global download_thread
    download_thread = Thread(target=handle_download)
    download_thread.start()

def cancel_download_func():
    global cancel_download, fake_progress_running
    cancel_download = True
    fake_progress_running = False
    messagebox.showinfo("Cancel", "Download will be canceled shortly.")

def clear_url_entry(event):
    global url_cleared
    if not url_cleared:
        url_entry.delete(0, tk.END)
        url_cleared = True

def add_to_download_list(url):
    download_path = create_download_directory(selected_path.get())
    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if download_list.size() >= 5:
            download_list.delete(0)
        download_list.insert(tk.END, info['title'])
        save_settings()

def select_download_path():
    path = filedialog.askdirectory()
    if path:
        selected_path.set(path)
        save_settings()

def save_settings():
    settings = {
        "download_path": selected_path.get(),
        "latest_downloads": download_list.get(0, tk.END)
    }
    with open(settings_file, 'w') as file:
        json.dump(settings, file)

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            settings = json.load(file)
            selected_path.set(settings.get("download_path", os.path.join(os.getcwd(), "Media-Youtube")))
            for item in settings.get("latest_downloads", []):
                download_list.insert(tk.END, item)

def style_widgets():
    root.configure(bg='#2b2b2b')
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', background='#3c3f41', foreground='#ffffff', relief='flat', font=('Helvetica', 12))
    style.map('TButton', background=[('active', '#4b4f51'), ('hover', '#4caf50')])
    style.configure('TLabel', background='#2b2b2b', foreground='#ffffff', font=('Helvetica', 14))
    style.configure('TEntry', fieldbackground='#3c3f41', foreground='#ffffff', relief='flat')
    style.configure('TRadiobutton', background='#2b2b2b', foreground='#ffffff', font=('Helvetica', 12), indicatoron=0, width=20, padding=(5,5))
    style.map('TRadiobutton', background=[('selected', '#005A99'), ('hover', '#3c3f41')], relief=[('pressed', 'sunken'), ('!pressed', 'flat')], foreground=[('selected', '#ffffff')])
    style.configure('TFrame', background='#2b2b2b')
    style.configure('TListbox', background='#3c3f41', foreground='#ffffff')
    style.configure('TProgressbar', background='#4caf50', troughcolor='#3c3f41')
    style.configure('SmallLabel.TLabel', font=('Helvetica', 10), background='#2b2b2b', foreground='#ffffff')

def start_gui():
    global root, url_entry, var, progress_var, progress_label, download_button, cancel_button, download_list, selected_path
    
    root = tk.Tk()
    root.title("GG Y-Downloader")
    root.geometry("561x534")
    root.resizable(False, False)
    
    style_widgets()

    ttk.Label(root, text="YouTube URL:").pack(pady=10)
    url_entry = ttk.Entry(root, width=50)
    url_entry.pack(pady=5)
    url_entry.bind("<FocusIn>", clear_url_entry)

    var = tk.StringVar(value="video")
    ttk.Radiobutton(root, text="Video Download", variable=var, value="video").pack()
    ttk.Radiobutton(root, text="Audio Download", variable=var, value="audio").pack()
    ttk.Radiobutton(root, text="Video & Audio Download", variable=var, value="both").pack()

    selected_path = tk.StringVar(value=os.path.join(os.getcwd(), "Media-Youtube"))
    path_frame = ttk.Frame(root)
    ttk.Label(path_frame, text="Download Path:").pack(side=tk.LEFT, padx=5)
    ttk.Entry(path_frame, textvariable=selected_path, width=40).pack(side=tk.LEFT)
    ttk.Button(path_frame, text="Change", command=select_download_path).pack(side=tk.LEFT, padx=5)
    path_frame.pack(pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(pady=(20, 5), fill=tk.X, padx=10)
    progress_label = ttk.Label(root, text="0%", background='#2b2b2b', foreground='#ffffff', font=('Helvetica', 12))
    progress_label.pack(pady=(0, 10))

    download_button = ttk.Button(root, text="Download", command=start_download)
    download_button.pack(pady=5)

    cancel_button = ttk.Button(root, text="Cancel", command=cancel_download_func, state=tk.DISABLED)
    cancel_button.pack(pady=5)

    ttk.Label(root, text="Latest Downloads", style='SmallLabel.TLabel').pack(pady=(15, 0), anchor='w', padx=36)

    download_list = tk.Listbox(root, height=8, width=60, bg='#3c3f41', fg='#ffffff')
    download_list.pack(pady=5)

    load_settings()

    root.protocol("WM_DELETE_WINDOW", lambda: (save_settings(), root.destroy()))

    root.mainloop()

if __name__ == "__main__":
    start_gui()
