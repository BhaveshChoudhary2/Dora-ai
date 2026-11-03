# Dora assistant

Dora is the renamed, GitHub-ready package made from the existing Jarvis project. It keeps the original command-line assistant, weather lookup, and OpenRouter-powered Q&A, with a clear `dora.py` entry point.

## Features

- Type commands, or use speech input when microphone support is installed.
- Get the time and date; search Google; open YouTube, Google, or WhatsApp Web.
- Ask for weather with `weather Mumbai` or `mausam Delhi` (Open-Meteo, no key required).
- Ask general questions with `ask <question>` or `dora <question>` (requires an OpenRouter key).
- Set simple in-session reminders, check battery status, and tell a joke.

## Requirements and setup

Use Python 3.9 or newer. From this project folder run:

```bash
python -m venv .venv
```

Activate the environment, then install the listed packages:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
```

Start Dora:

```bash
python dora.py
```

If speech or microphone setup is unavailable, Dora falls back to typed input. Microphone recognition needs PyAudio, which can require separate operating-system setup. Install it only if you want microphone input:

```bash
python -m pip install pyaudio
```

Speech recognition uses Google's online recognition service. Typing mode does not need microphone packages.

## OpenRouter Q&A setup

The weather and basic assistant commands work without an API key. To enable AI answers, create your own OpenRouter key and set it as an environment variable. Do not put a real key in this repository.

```bash
# macOS / Linux, current terminal only
export OPENROUTER_API_KEY="your-key-here"

# Windows PowerShell, current terminal only
$env:OPENROUTER_API_KEY="your-key-here"
```

Then restart Dora in that terminal. `OPENAI_API_KEY` is also accepted as a fallback environment variable. Keys are not included in this project.

## Example commands

```text
time
 date
weather Mumbai
mausam Delhi
ask explain photosynthesis simply
search Python tutorials
open youtube
remind me in 10 minutes chai
battery
joke
exit
```

Reminders stay in memory only while Dora is running. Opening local applications depends on their installed names and the operating system.

## Project files

- `dora.py`: unified assistant entry point, adapted from the original `jarvis.py`.
- `v2_weather.py`: weather service module from the original weather component.
- `v4_brain.py`: OpenRouter question-answering module from the original brain component.
- `requirements.txt`: Python packages for speech output/input and optional battery status.

## Upload to GitHub

Create a new GitHub repository, then upload the files and folders from this `Dora` project directory. Do not upload your virtual environment or API key. The `.gitignore` excludes common local environment files.
