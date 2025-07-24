import whisper
import ollama
import time
import pyttsx3

from ugot import ugot
got = ugot.UGOT()
got.initialize('192.168.1.183')

# Initialize components
# Change model_whisper = whisper.load_model("base") to "medium" or "large" for better accuracy.
# Change model_ollama to whatever model you're using
# I used llama3.2 since it was the first one to download
model_whisper = whisper.load_model("base")
model_ollama = "llama3.2"
engine = pyttsx3.init()

def ugot_record():
    prompt = got.start_audio_asr()
    return prompt

def chat_with_model(prompt):
    print("Sending to Ollama...")
    start_time = time.time()
    response = ollama.chat(model=model_ollama, messages=[{"role": "user", "content": prompt}])
    reply = response["message"]["content"]
    elapsed = time.time() - start_time
    print(f"Ollama responded in {elapsed:.2f} seconds.")
    return reply

def speak(text):
    print("Speaking the response...")
    got.play_audio_tts(text, voice_type=0, wait=True)

text_input = ugot_record() + " Respond in 4 or fewer sentences."

print("\nYou said:", text_input)
model_response = chat_with_model(text_input)

print("\nModel says:", model_response)
speak(model_response)
