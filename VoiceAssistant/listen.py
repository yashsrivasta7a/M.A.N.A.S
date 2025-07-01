import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk
import requests
import os
from dotenv import load_dotenv
import webbrowser
import threading
import platform
import subprocess
import re

load_dotenv()

tts_thread = None
stop_speaking_flag = False

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-04-01-preview")

AZURE_OPENAI_URL = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
speech_config.speech_synthesis_voice_name = "hi-IN-RehaanNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

def speak(text):
    global tts_thread, stop_speaking_flag
    def speak_text():
        result = speech_synthesizer.speak_text_async(text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesis error:", result.reason)

    stop_speaking_flag = False
    tts_thread = threading.Thread(target=speak_text)
    tts_thread.start()

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        print("Assistant is speaking... (you can interrupt)")
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=2)
            print("Interrupt detected!")
            stop_speaking_flag = True
            return
        except sr.WaitTimeoutError:
            pass

    tts_thread.join()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        print("Listening for your command...")
        try:
            audio = recognizer.listen(source, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, samajh nahi aaya.")
            return ""
        except sr.RequestError:
            speak("Internet problem hai shayad.")
            return ""

def ask_azure_openai(message):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY,
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are MANAS, which stands for Mostly Automated, Naturally Awesome Sidekick. You are a highly intelligent, context-aware voice assistant built to serve your owner, Yash."
            },
            {"role": "user", "content": message}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    response = requests.post(AZURE_OPENAI_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Azure OpenAI error:", response.status_code, response.text)
        return "Sorry, kuch gadbad ho gayi."

def open_site(reply):
    url_verify = re.search(r'(https?://[^\s]+)', reply)
    if url_verify:
        url = url_verify.group(0)
        webbrowser.open(url)
        speak(f"Opening {url}")
    else:
        speak("Sorry, I couldn’t find a link in the response.")

def open_folder(folder_name):
    folder_map = {
        "downloads": r"C:\\Users\\ysyas\\Downloads",
        "documents": r"C:\\Users\\ysyas\\Documents",
        "project": r"D:\\Code",
        "pictures": r"C:\\Users\\ysyas\\Pictures"
    }
    path = folder_map.get(folder_name.lower())
    if path and os.path.exists(path):
        os.startfile(path)
        speak(f"Opening {folder_name}")
    else:
        speak("Folder nahi mila, thoda clearly bol bhai.")

def system_control(command):
    os_name = platform.system()
    if command == "shutdown":
        speak("System ko shutdown kar raha hoon.")
        if os_name == "Windows":
            subprocess.call("shutdown /s /t 1", shell=True)
        else:
            subprocess.call("shutdown now", shell=True)
    elif command == "restart":
        speak("System ko restart kar raha hoon.")
        if os_name == "Windows":
            subprocess.call("shutdown /r /t 1", shell=True)
        else:
            subprocess.call("reboot", shell=True)
    elif command == "lock":
        speak("System ko lock kar raha hoon.")
        if os_name == "Windows":
            subprocess.call("rundll32.exe user32.dll,LockWorkStation", shell=True)
        else:
            subprocess.call("gnome-screensaver-command -l", shell=True)
    else:
        speak("Yeh system command mujhe nahi aati.")

if __name__ == "__main__":
    speak("Hello Yash, MANAS is online.")
    while True:
        query = take_command()
        if query:
            if any(exit_cmd in query for exit_cmd in ["exit", "goodbye", "stop"]):
                speak("Goodbye, aaka!")
                break
            elif "website" in query:
                reply = ask_azure_openai(query)
                open_site(reply)
            elif "open" in query:
                if "downloads" in query:
                    open_folder("downloads")
                elif "documents" in query:
                    open_folder("documents")
                elif "project" in query:
                    open_folder("project")
                elif "pictures" in query:
                    open_folder("pictures")
                else:
                    speak("Kya kholun bhai? Folder ka naam theek se bol.")
            elif "shutdown" in query:
                system_control("shutdown")
            elif "restart" in query:
                system_control("restart")
            elif "lock" in query:
                system_control("lock")
            else:
                reply = ask_azure_openai(query)
                speak(reply)
