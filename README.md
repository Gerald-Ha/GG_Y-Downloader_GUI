
# GG Y-Downloader

**GG Y-Downloader** is an easy-to-use tool that allows you to download YouTube videos or audio files directly from YouTube. It provides a graphical user interface (GUI) and supports downloading **videos**, **audio (MP3)**, or both simultaneously.

![yt](https://github.com/user-attachments/assets/079ce04d-3caa-4920-a789-3d8251a68f0e)

## New Features

- **Enhanced GUI**: The user interface has been improved for a more intuitive experience.
- **Display Last 5 Downloads**: The application now shows the last 5 downloaded items.
- **Manual Path Selection**: Users can now manually set the download path and choose where to save the files.

<br><br>
## Features
- **Video Download** (MP4)
- **Audio Download** (MP3)
- **Video & Audio Download** (MP4 for video, separate MP3 for audio)
- **Display of Recent Downloads**: Shows a list of the last 5 downloaded videos and audio files.
- **Manual Path Selection**: Allows users to specify the location for downloads.

<br><br>
## System Requirements

### For Windows:
- Only **ffmpeg**

### For Linux:
- **Python 3.x** (automatically installed as a dependency)
- **ffmpeg** (automatically installed as a dependency)
- **yt-dlp** (automatically installed as a dependency)

<br><br>
## Installation and Usage

### For **Linux** Users

#### 1. Install System Requirements (Automatically)
When you install the `.deb` package, all dependencies like **Python**, **ffmpeg**, and **yt-dlp** will be automatically installed.

#### 2. Install the Application
Download the **.deb package** and install it with `dpkg`:

```bash
sudo dpkg -i GG_Y-Downloader.deb
```

If dependencies are missing during installation, you can fix them with the following command:

```bash
sudo apt-get install -f
```

#### 3. Start the Application

After installation, you can launch the application from the Applications menu. Alternatively, you can run it from the terminal:

```bash
GG_Y-Downloader
```

### Downloaded Files Location
The videos and audio files will be saved in the `Media-Youtube` directory, created in the current working directory from where the application is launched. For example:

```bash
/home/username/Media-Youtube/
```

<br><br>

### For Windows Users

1. **Install and Run the Application**: 
   Download the `.exe` file and simply run the application by double-clicking on the `.exe` file.

2. **Install ffmpeg**:
   - Go to the [ffmpeg download page](https://www.gyan.dev/ffmpeg/builds/).
   - Select "Windows" and follow the recommended link to a build.
   - Download the zip archive and extract it to a location of your choice (e.g., `C:\ffmpeg`).
   - Add `C:\ffmpeg\bin` to your system path:
     - Open the Start menu and search for "Edit the system environment variables".
     - Edit the "System Variables" and add the path `C:\ffmpeg\bin`.
   - Verify the installation by typing `ffmpeg -version` in the command prompt.

### Downloaded Files Location
The videos and audio files will be saved in the `Media-Youtube` directory, created in the current working directory from where the application is launched. For example:

```bash
c:\Users\yourusername\Desktop\Media-Youtube\
```

<br><br>
## How to Use the Application

1. **Start the application**: Open the application from the Applications menu (Linux) or by double-clicking the `.exe` file (Windows).
2. **Enter the YouTube URL**: Enter the URL of the YouTube video you want to download.
3. **Choose the download option**:
   - **Video Download**: Downloads the video in MP4 format.
   - **Audio Download**: Downloads only the audio in MP3 format.
   - **Video & Audio Download**: Downloads both the video (MP4) and a separate audio file (MP3).
4. **Start the download**: Click on "Download". A progress bar will show how much of the download is complete.
5. **Completion**: After the download is finished, you will receive a notification, and the files will be saved in the `Media-Youtube` folder.

<br><br>

## Troubleshooting

### Missing Dependencies (Linux)
If you encounter errors about missing dependencies when starting the application, ensure that ffmpeg is correctly installed and all necessary libraries are in place:

```bash
sudo apt-get install -f
```

<br><br>

### Download Folder Not Found
The downloaded files are saved in the `Media-Youtube` folder, which is created in the current working directory. Make sure you run the program from the correct directory to easily find the downloaded files.

---

Feel free to customize this text further if needed. Let me know if you need any other modifications!
