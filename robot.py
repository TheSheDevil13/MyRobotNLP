import google.generativeai as genai
import speech_recognition as sr
from banglaspeech2text import Speech2Text
from gtts import gTTS
from playsound3 import playsound
import os
import time
from dotenv import load_dotenv

# --- 1. SETUP: Load API Key and Models ---

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

genai.configure(api_key=API_KEY)

# This is your robot's "memory"
robot_memory = {
    "user_name": "Ava", # Let's set a default name
    "current_lesson": "Colors",
    "last_quiz_score": 0
}

# === THIS IS THE NEW, BETTER PROMPT ===
robot_personality = f"""
You are a friendly and encouraging robot tutor.
Your user is a primary learner named {robot_memory['user_name']}.
Keep your answers short, simple, and very positive.

DO NOT use emojis or describe actions (e.g., *smiles*).
You have already greeted the user, so DO NOT greet them again.
Just answer their questions directly.
"""
# === END OF NEW PROMPT ===

# Configure Speech Recognizers
r = sr.Recognizer()
print("Loading Bangla AI model... (This may take a minute)")
stt = Speech2Text("base")
print("Bangla model loaded.")

# === CODE CHANGE 1: CONFIGURE THE MODEL AND CHAT ===
# We pass the personality prompt in when we create the model
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    system_instruction=robot_personality # This sets the personality!
)
chat = model.start_chat(history=[]) # Start a chat session to remember
print("Robot is ready!")
# === END OF CODE CHANGE 1 ===


# --- 2. THE "MOUTH" (Text-to-Speech) ---

def speak(text, lang='en'):
    try:
        print(f"Robot: {text}")
        tts = gTTS(text=text, lang=lang)
        filename = "robot_speech.mp3"
        tts.save(filename)
        playsound(filename)
        time.sleep(0.5)
        os.remove(filename)
    except Exception as e:
        print(f"Error in speaking: {e}")

# --- 3. THE "EARS" (Speech-to-Text) ---

def listen_and_recognize(language="en"):
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        
    print("Recognizing...")
    try:
        text = ""
        if language == "bn":
            text = stt.recognize(audio)
        else:
            text = r.recognize_google(audio, language="en-US")
        
        print(f"You: {text}")
        return text.lower()
    except Exception as e:
        print(f"Sorry, I didn't catch that. ({e})")
        return ""

# --- 4. THE "BRAIN" (Smart Prompt Engineering) ---
# We no longer need the 'build_smart_prompt' function!
# The 'system_instruction' handles it all.

# --- 5. THE MAIN LOOP ---

if __name__ == "__main__":
    
    current_language = 'en'
    
    # The first greeting is done ONCE by our code, not the AI
    speak(f"Hello {robot_memory['user_name']}, I am ready to learn!", lang=current_language)
    
    while True:
        user_input = listen_and_recognize(language=current_language)
        
        if not user_input:
            continue

        if "goodbye" in user_input:
            speak("Goodbye, see you next time!", lang=current_language)
            break
        
        if "speak in bangla" in user_input:
            current_language = 'bn'
            speak("OK, I will now speak in Bangla.", lang='en')
            speak("আমি এখন বাংলায় কথা বলবো।", lang='bn')
            continue
            
        if "speak in english" in user_input:
            current_language = 'en'
            speak("OK, I will now speak in English.", lang='bn')
            speak("Okay, I will now speak in English.", lang='en')
            continue

        # === CODE CHANGE 2: USE CHAT.SEND_MESSAGE ===
        # This sends ONLY the user's text. The AI remembers
        # its personality and the chat history all by itself.
        try:
            response = chat.send_message(user_input)
            speak(response.text, lang=current_language)
        except Exception as e:
            print(f"API Error: {e}")
            speak("Oops, I'm having a little trouble thinking right now.", lang=current_language)
        # === END OF CODE CHANGE 2 ===