import ollama
import time

from ugot import ugot
got = ugot.UGOT()
got.initialize('192.168.1.183')

model_ollama = "llama3.2"

WAKE_WORD = "you got"

def ugot_record():
    prompt = got.start_audio_asr()
    return prompt.strip().lower()

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

print("UGOT is listening for the wake word. Say 'hey you got' to activate.")
try:
    while True:
        text_input = ugot_record()
        if not text_input:
            time.sleep(0.5)
            continue

        if WAKE_WORD not in text_input:
            print(f"Ignoring input (no wake word): '{text_input}'")
            time.sleep(0.5)
            continue

        processed_input = text_input.replace(WAKE_WORD, "", 1).strip()
        if not processed_input:
            print("Wake word detected but no follow-up.")
            continue

        full_prompt = processed_input + " Respond in 4 or fewer sentences."
        print("\nYou said:", processed_input)
        model_response = chat_with_model(full_prompt)
        print("\nModel says:", model_response)
        speak(model_response)

except KeyboardInterrupt:
    print("\nStopping UGOT listener.")
