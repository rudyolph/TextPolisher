# TextPolisher 🪄

A lightweight Windows System Tray application that uses Google's Gemini AI to instantly polish and refine your text.

## Features

- **Global Hotkey**: Press `Ctrl + Alt + P` to polish selected text in any application.
- **AI-Powered**: Uses Gemini 3.1 Flash Lite for high-quality rewriting.
- **Visual Feedback**: The system tray icon changes color while the AI is "thinking."
- **Windows Notifications**: Built-in toast notifications for errors or empty selections.
- **Dynamic Config**: Update your `.env` file and the app reloads settings instantly without a restart.

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- A Google Gemini API Key (get one at [aistudio.google.com](https://aistudio.google.com/))

### 2. Installation

Clone the repository and set up a virtual environment:

```powershell
git clone https://github.com/YOUR_USERNAME/TextPolisher.git
cd TextPolisher
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.1-flash-lite-preview
```

### 4. Running the App

```powershell
python text_polisher.py
```

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
