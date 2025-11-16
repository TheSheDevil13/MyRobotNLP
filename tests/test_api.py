import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

try:
    # Configure the library with your key
    genai.configure(api_key=API_KEY)

    # Initialize the model using gemini-2.5-flash
    model = genai.GenerativeModel('gemini-2.5-flash')

    print("Sending 'Hello' to the AI...")

    # Send a simple prompt to the model
    response = model.generate_content("Hello")

    # Print the AI's response text
    print("\n--- AI Response ---")
    print(response.text)
    print("--------------------")
    print("\nSuccess! Your API key is working.")

except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"Something went wrong: {e}")
    print("\nPlease check your API key or internet connection.")