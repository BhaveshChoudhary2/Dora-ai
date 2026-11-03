"""Dora, a small voice-or-typing assistant built from the existing Jarvis project."""
import datetime
import os
import random
import subprocess
import threading
import time
import urllib.parse
import webbrowser

try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import pyttsx3
    _speech_engine = pyttsx3.init()
    _speech_engine.setProperty("rate", 170)
except Exception:
    _speech_engine = None

from v2_weather import get_weather
from v4_brain import ask as brain_ask

REMINDERS = []


def speak(text):
    print("Dora:", text)
    if _speech_engine is not None:
        try:
            _speech_engine.say(text)
            _speech_engine.runAndWait()
        except Exception:
            pass


def listen():
    """Use the microphone when available, otherwise accept typed commands."""
    if sr is None:
        return input("You: ").strip().lower()
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=12)
        return recognizer.recognize_google(audio).lower()
    except Exception:
        speak("Mic available nahi hua ya samajh nahi aaya. Type karke try karo.")
        return input("You: ").strip().lower()


def _weather_city(command):
    for keyword in ("weather", "mausam"):
        if keyword in command:
            return command.split(keyword, 1)[1].strip() or "Delhi"
    return "Delhi"


def _add_reminder(command):
    words = command.split()
    amount_index = next((i for i, word in enumerate(words) if word.isdigit()), None)
    if amount_index is None:
        speak('Aise bolo: "remind me in 10 minutes chai"')
        return
    amount = int(words[amount_index])
    unit = words[amount_index + 1].lower() if amount_index + 1 < len(words) else "hours"
    minutes = amount if unit.startswith("min") else amount * 60
    tail_start = amount_index + 2 if amount_index + 1 < len(words) else amount_index + 1
    reminder_text = " ".join(words[tail_start:]) or "kaam"
    fire_at = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    REMINDERS.append((fire_at, reminder_text))
    speak(f"Theek hai, {fire_at.strftime('%I:%M %p')} pe yaad dilaungi: {reminder_text}")


def handle(command):
    command = command.strip().lower()
    if not command:
        return True
    if command in ("exit", "bye", "band", "quit"):
        speak("Bye!")
        return False
    if "time" in command or "samay" in command:
        speak("Abhi " + datetime.datetime.now().strftime("%I:%M %p"))
    elif "date" in command or "aaj" in command:
        speak(datetime.datetime.now().strftime("%A, %d %B %Y"))
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("YouTube khol rahi hoon.")
    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Google khol rahi hoon.")
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("WhatsApp khol rahi hoon.")
    elif command.startswith("search"):
        query = command.split("search", 1)[1].strip()
        if query:
            url = "https://www.google.com/search?" + urllib.parse.urlencode({"q": query})
            webbrowser.open(url)
            speak(f"Searching {query}")
        else:
            speak("Search ke baad kya dhoondhna hai, woh bolo.")
    elif "weather" in command or "mausam" in command:
        speak(get_weather(_weather_city(command)))
    elif command.startswith(("ask ", "dora ", "jarvis ", "batao ")) or ("?" in command and len(command.split()) > 2):
        question = command.split(" ", 1)[1] if command.startswith(("ask ", "dora ", "jarvis ", "batao ")) else command
        speak("Sochne do...")
        speak(brain_ask(question)[:800])
    elif "remind" in command or "yaad" in command:
        _add_reminder(command)
    elif "battery" in command:
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery is None:
                speak("Battery status is device par available nahi hai.")
            else:
                status = "charging" if battery.power_plugged else "battery par"
                speak(f"{round(battery.percent)} percent, {status}")
        except Exception:
            speak("Battery status ke liye psutil install karo: pip install psutil")
    elif command.startswith("open "):
        app = command.replace("open", "", 1).strip()
        try:
            if os.name == "nt":
                os.startfile(app)
            else:
                subprocess.Popen([app.lower().replace(" ", "-")])
            speak(f"Opening {app}")
        except Exception:
            speak(f"{app} nahi khula, naam check karo.")
    elif "joke" in command:
        speak(random.choice([
            "Aapka code chal raha hai. Miracle hi samjho.",
            "Main 90% confident hoon. Baaki 10% confidence bhi main hoon.",
        ]))
    else:
        speak("Try: time, date, weather <city>, ask <question>, search <query>, open YouTube/Google/WhatsApp, joke, remind, battery, exit.")
    return True


def reminder_loop():
    while True:
        now = datetime.datetime.now()
        for reminder in list(REMINDERS):
            fire_at, text = reminder
            if fire_at <= now:
                REMINDERS.remove(reminder)
                speak(f"Reminder: {text}")
        time.sleep(10)


def main():
    threading.Thread(target=reminder_loop, daemon=True).start()
    speak("Dora online. Type or speak a command.")
    while handle(listen()):
        pass


if __name__ == "__main__":
    main()
