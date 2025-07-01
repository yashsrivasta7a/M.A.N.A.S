import pyttsx3


# Initialize the speech engine
engine = pyttsx3.init()

# Set a slower speech rate
engine.setProperty('rate', 190)  # Default is usually around 200

# Speak a message
engine.say("Hello Yash! I am your voice assistant.")
engine.runAndWait()
