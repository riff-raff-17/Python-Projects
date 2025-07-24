import whisper
import sounddevice as sd
import scipy.io.wavfile as wavfile
import numpy as np
import tempfile
import ollama
import time
import pyttsx3
import os

# Initialize components
model_whisper = whisper.load_model("base")  # Change to "medium" or "large" for better accuracy
model_ollama = "llama3.2"
engine = pyttsx3.init()

# Record audio
def record_audio(duration=5, samplerate=16000):
    print("Recording... Speak now!")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return samplerate, audio

# Save to temporary WAV file
def save_audio(samplerate, audio):
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_wav.close()  # Close file so it can be written to on Windows
    wavfile.write(temp_wav.name, samplerate, audio)
    return temp_wav.name

# Transcribe using Whisper
def transcribe_audio(audio_path):
    print("Transcribing with Whisper...")
    result = model_whisper.transcribe(audio_path)
    return result["text"]

# Send to Ollama
def chat_with_model(prompt):
    print("Sending to Ollama...")
    start_time = time.time()
    response = ollama.chat(model=model_ollama, messages=[{"role": "user", "content": prompt}])
    reply = response["message"]["content"]
    elapsed = time.time() - start_time
    print(f"Ollama responded in {elapsed:.2f} seconds.")
    return reply

# Text-to-speech
def speak(text):
    print("Speaking the response...")
    engine.say(text)
    engine.runAndWait()

# Run the interaction
def main():
    samplerate, audio = record_audio(duration=6)
    audio_path = save_audio(samplerate, audio)

    try:
        text_input = transcribe_audio(audio_path)
        print("\nYou said:", text_input)

        model_response = chat_with_model(text_input)
        print("\nModel says:", model_response)

        speak(model_response)

    finally:
        # Ensure temp file is deleted even if an error occurs
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"\nTemporary file deleted: {audio_path}")

if __name__ == "__main__":
    main()
