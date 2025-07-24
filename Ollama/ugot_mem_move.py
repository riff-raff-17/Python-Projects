import ollama
import time
import re

from ugot import ugot
got = ugot.UGOT()
got.initialize('192.168.1.177')

model_ollama = "llama3.2"

WAKE_WORD = "hey you got"
EXIT_PHRASE = "goodbye you got"
MAX_MEMORY = 10

conversation = [
    {"role": "system", "content": "You are a helpful robot assistant. Keep your replies short and friendly."}
]

def forward(dist):
    got.balance_move_speed_times(0, 30, dist, 1)

def backward(dist):
    got.balance_move_speed_times(1, 30, dist, 1)

def left(deg):
    got.balance_turn_speed_times(2, 30, deg, 2)

def right(deg):
    got.balance_turn_speed_times(3, 30, deg, 2)

def ugot_record():
    got.play_audio_tts("Listening", 0, wait=True)
    _, prompt = got.start_audio_asr_doa(duration=6)
    return prompt.strip().lower()

def chat_with_model(prompt):
    conversation.append({"role": "user", "content": prompt})
    print("Sending to Ollama...")
    start_time = time.time()
    response = ollama.chat(model=model_ollama, messages=conversation)
    reply = response["message"]["content"]
    elapsed = time.time() - start_time
    print(f"Ollama responded in {elapsed:.2f} seconds.")
    conversation.append({"role": "assistant", "content": reply})

    if len(conversation) > MAX_MEMORY:
        conversation[:] = [conversation[0]] + conversation[-(MAX_MEMORY - 1):]

    return reply

def speak(text):
    print("Speaking the response...")
    got.play_audio_tts(text, voice_type=0, wait=True)

def handle_movement(cmd):
    m = re.match(r"^(?:forwards?|backwards?)\s+(\d+)", cmd)
    if m:
        dist = int(m.group(1))
        if cmd.startswith("forward"):
            speak(f"Moving forward {dist} units")
            forward(dist)
        else:
            speak(f"Moving backward {dist} units")
            backward(dist)
        return True

    m = re.match(r"^(?:left|right)\s+(\d+)", cmd)
    if m:
        deg = int(m.group(1))
        if cmd.startswith("left"):
            speak(f"Turning left {deg} degrees")
            left(deg)
        else:
            speak(f"Turning right {deg} degrees")
            right(deg)
        return True

    return False

print(f"UGOT is listening for the wake word. Say '{WAKE_WORD}' to activate.")
try:
    while True:
        text_input = ugot_record()
        if not text_input:
            time.sleep(0.5)
            continue

        if EXIT_PHRASE in text_input:
            speak("Goodbye! See you later!")
            break

        if WAKE_WORD not in text_input:
            print(f"Ignoring input (no wake word): '{text_input}'")
            time.sleep(0.5)
            continue

        processed_input = text_input.replace(WAKE_WORD, "", 1).strip()
        if not processed_input:
            print("Wake word detected but no follow-up.")
            continue

        print("\nYou said:", processed_input)

        if handle_movement(processed_input):
            continue

        model_response = chat_with_model(processed_input)
        print("\nOllama says:", model_response)
        speak(model_response)

except KeyboardInterrupt:
    print("\nStopping UGOT listener.")
