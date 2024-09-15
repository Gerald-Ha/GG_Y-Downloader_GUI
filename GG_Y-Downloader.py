import os
import time
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import messagebox, ttk

# Function to create the directory if it doesn't exist
def create_download_directory():
    download_path = os.path.join(os.getcwd(), "Media-Youtube")
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return download_path

# Progress hook to update the GUI progress bar
def progress_hook(d):
    if d['status'] == 'downloading':
        percent = float(d['_percent_str'].strip('%'))
        progress_var.set(percent)
        root.update_idletasks()  # Update the GUI to reflect the progress
    elif d['status'] == 'finished':
        progress_var.set(100)  # Set to 100% when finished
        messagebox.showinfo("Download Complete", "Download completed successfully!")

# Function to download YouTube videos based on type
def download_youtube_video(url, download_type):
    download_path = create_download_directory()

    # Initial options for the video download
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook]  # Use the progress hook to update the GUI
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
        # First, download both video and audio in MP4 format
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # If "both" is selected, now extract audio to MP3 with a different name
        if download_type == "both":
            mp3_opts = {
                'format': 'bestaudio',
                'outtmpl': os.path.join(download_path, '%(title)s-audio.mp3'),  # Save MP3 with a different name
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
            with YoutubeDL(mp3_opts) as ydl_mp3:
                ydl_mp3.download([url])
            messagebox.showinfo("Success", "Video and MP3 Download completed!")
        else:
            messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {e}")

# GUI Setup with Tkinter
def start_gui():
    def download_video():
        url = url_entry.get()
        download_type = var.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a valid YouTube URL.")
            return
        progress_var.set(0)  # Reset progress bar to 0%
        download_youtube_video(url, download_type)
    
    global root, progress_var
    root = tk.Tk()
    root.title("GG Y-Downloader")
    root.geometry("400x300")

    # URL Input
    tk.Label(root, text="YouTube URL:").pack(pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    # Download type selection
    var = tk.StringVar(value="video")
    tk.Radiobutton(root, text="Video Download", variable=var, value="video").pack()
    tk.Radiobutton(root, text="Audio Download", variable=var, value="audio").pack()
    tk.Radiobutton(root, text="Video & Audio Download", variable=var, value="both").pack()

    # Progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(pady=20, fill=tk.X, padx=10)

    # Download button
    tk.Button(root, text="Download", command=download_video).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_gui()

