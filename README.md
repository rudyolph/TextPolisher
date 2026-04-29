# TextPolisher 🪄

A lightweight Windows System Tray application that uses Google's Gemini AI to instantly polish and refine your text.

## Features

- **Global Hotkey**: Press `Ctrl + Alt + P` to polish selected text in any application.
- **AI-Powered**: Uses Gemini 3.1 Flash Lite for high-quality rewriting.
- **Settings GUI**: Easily update your API Key, Model, and Hotkey via a modern tray-based interface.
- **Visual Feedback**: The system tray icon changes color while the AI is "thinking."
- **Windows Notifications**: Built-in toast notifications for errors or empty selections.
- **Dynamic Config**: The app reloads settings instantly without a restart when `.env` or `prompt.txt` changes.

## 🚀 Quick Start (No Python Required)

If you just want to use the app without touching any code:

1.  Download the latest `TextPolisher.zip` from the [Releases](https://github.com/YOUR_USERNAME/TextPolisher/releases) page.
2.  Extract the folder to a permanent location (e.g., `C:\Tools\TextPolisher`).
3.  Run `TextPolisher.exe`.
4.  Right-click the blue **P** icon in your system tray and select **Settings** to enter your [Gemini API Key](https://aistudio.google.com/).

---

## 🛠️ Developer Setup

### 1. Installation

Clone the repository and set up a virtual environment:

```powershell
git clone https://github.com/YOUR_USERNAME/TextPolisher.git
cd TextPolisher
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration

You can configure the app using the **Settings** menu in the tray icon, or manually via a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
HOTKEY=ctrl+alt+p
```

### 3. Customizing the AI Persona

You can change exactly how the AI rewrites your text by editing `prompt.txt`. The app watches this file and will use your new instructions the very next time you press the hotkey.

### 4. Building the EXE

To build your own standalone executable, simply run:
```powershell
.\build.bat
```
The output will be in the `dist/` folder.

---

## Auto-Start on Boot (Windows)

To have TextPolisher start automatically when you log in, run the following in an Administrator PowerShell:

```powershell
$WorkingDir = "C:\Projects\TextPolisher" # Update to your actual path
$PythonPath = "$WorkingDir\venv\Scripts\pythonw.exe"
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "text_polisher.py" -WorkingDirectory $WorkingDir
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "TextPolisher" -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force
```

## License

MIT
