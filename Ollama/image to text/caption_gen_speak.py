import os
import subprocess
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import platform

# === CONFIGURATION ===
IMAGE_PATH = "cat.jpg"  # Change this to your image file
OLLAMA_MODEL = "llama3.2"
CAPTION_STYLE = "funny haiku"  # Try: "sarcastic", "haiku", "romantic", etc.

# === STEP 1: LOAD BLIP MODEL ===
print("Loading BLIP model for image captioning...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# === STEP 2: LOAD AND CAPTION IMAGE ===
try:
    image = Image.open(IMAGE_PATH).convert('RGB')
except FileNotFoundError:
    print(f"Image file not found: {IMAGE_PATH}")
    exit()

print(f"Generating caption for image: {IMAGE_PATH}")
inputs = processor(image, return_tensors="pt")
output = model.generate(**inputs)
image_caption = processor.decode(output[0], skip_special_tokens=True)
print("Raw caption:", image_caption)

# === STEP 3: GENERATE STYLED TEXT WITH OLLAMA ===
prompt = (
    f"Given this image description: '{image_caption}', "
    f"write a {CAPTION_STYLE} for it."
)

print(f"🤖 Sending prompt to Ollama ({OLLAMA_MODEL})...")
try:
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL, prompt],
        capture_output=True,
        text=True,
        check=True
    )
    ollama_response = result.stdout.strip()
except subprocess.CalledProcessError as e:
    print("Error running Ollama:", e)
    exit()

print("\nFinal Generated Caption:\n")
print(ollama_response)

def speak(text):
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(["say", text])
    elif system == "Linux":
        subprocess.run(["espeak", text])  # You can also try "spd-say"
    elif system == "Windows":
        powershell_script = f"""
        Add-Type –AssemblyName System.Speech
        $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $speak.Speak("{text}")
        """
        subprocess.run(["powershell", "-Command", powershell_script])
    else:
        print("Unsupported OS for speech synthesis.")

# === STEP 4: SPEAK THE FINAL CAPTION ===
print("\nSpeaking the caption aloud...")
speak(ollama_response)
