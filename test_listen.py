import speech_recognition as sr
from banglaspeech2text import Speech2Text
import time

# --- Setup the Recognizers ---

# 1. This is the main "listener" from SpeechRecognition
r = sr.Recognizer()

# 2. This is the special model for understanding Bangla
# We load the "base" model, which is a good balance of speed and accuracy.
# This download might take a minute the very first time you run it.
print("Loading Bangla AI model... (This may take a minute)")
stt = Speech2Text("base")
print("Bangla model loaded.")

def listen_and_recognize(language="en"):
    """
    Listens via the microphone and turns speech into text.
    'language' can be 'en' (English) or 'bn' (Bangla).
    """
    # Use the computer's default microphone
    with sr.Microphone() as source:
        print("\nAdjusting for ambient noise...")
        # This is a crucial step to ignore background noise
        r.adjust_for_ambient_noise(source, duration=1)
        
        print(f"Speak in {language} now...")
        
        # Listen for the user's audio
        audio = r.listen(source)
        
    print("Got it! Recognizing...")
    
    try:
        text = ""
        # --- This is the key logic ---
        if language == "bn":
            # Use the special Bangla model
            text = stt.recognize(audio)
        else:
            # Use Google's online recognizer for English
            # This requires an internet connection
            text = r.recognize_google(audio, language="en-US")
        
        # Return the recognized text in lowercase
        return text.lower()
        
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        return ""

# --- Main Test Loop ---
if __name__ == "__main__":
    
    # Test English
    print("--- Test 1: ENGLISH ---")
    english_text = listen_and_recognize(language="en")
    if english_text:
        print(f"\nYou said (EN): {english_text}")

    # Give a moment to get ready
    time.sleep(1)

    # Test Bangla
    print("\n\n--- Test 2: BANGLA ---")
    bangla_text = listen_and_recognize(language="bn")
    if bangla_text:
        print(f"\nTime bolchhen (BN): {bangla_text}")