import azure.cognitiveservices.speech as speechsdk
import time

# Replace these with your actual Azure credentials
speech_key = "FIZgt0bMPG5Fcd91D6RnOEJ8LfKpBSrKGLCwVKpLRDWovbc4bRgvJQQJ99BGACYeBjFXJ3w3AAAYACOGgkQt"
service_region = "eastus"  # e.g., "eastus"

male_voices = [
    "en-IN-AaravNeural",
    "en-IN-ArjunNeural", 
    "en-IN-KunalNeural",
    "en-IN-PrabhatNeural",
    "en-IN-RehaanNeural",
    "en-IN-ArjunIndicNeural1",
    "en-IN-PrabhatIndicNeural1",
    "hi-IN-AaravNeural",
    "hi-IN-ArjunNeural",
    "hi-IN-KunalNeural",
    "hi-IN-RehaanNeural", 
    "hi-IN-MadhurNeural"
]

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

def synthesize_voice(voice_name, text="Hello, voice test hori hai."):
    speech_config.speech_synthesis_voice_name = voice_name
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    print(f"Playing voice: {voice_name}")
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Done playing: {voice_name}\n")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

if __name__ == "__main__":
    for voice in male_voices:
        synthesize_voice(voice)
          # Pause 1 second between voices
