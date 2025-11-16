from gtts import gTTS
from playsound3 import playsound
import os
import time

def speak(text, lang='en'):
    """
    Takes text and speaks it out loud in the specified language.
    'lang' can be 'en' (English) or 'bn' (Bangla).
    """
    try:
        print(f"Robot will say: {text}")
        
        # 1. Create the gTTS object
        tts = gTTS(text=text, lang=lang)
        
        # 2. Save the speech to a temporary .mp3 file
        filename = "temp_speech.mp3"
        tts.save(filename)
        
        # 3. Play the .mp3 file
        # We use playsound3 here as it's more reliable
        playsound(filename)
        
        # 4. Clean up: Give a moment for the file to release, then remove it
        time.sleep(0.5) 
        os.remove(filename)
        
    except Exception as e:
        print(f"Error in speaking: {e}")
        print("Please check your internet connection (gTTS requires it).")

# --- Main Test Loop ---
if __name__ == "__main__":
    
    # Test English
    print("--- Test 1: Speaking ENGLISH ---")
    speak("Hello, this is a test in English.", lang='en')

    # Give a moment between sounds
    time.sleep(1)

    # Test Bangla
    print("\n--- Test 2: Speaking BANGLA ---")
    # Using the Bangla text for "Hello, this is a test in Bangla."
    speak("হ্যালো, এটি একটি বাংলা পরীক্ষা।", lang='bn')
    
    print("\nSpeaking test complete.")