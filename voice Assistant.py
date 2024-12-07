import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import requests

# Initialize the Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture audio from the microphone and return as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("There seems to be a problem with the service.")
        except sr.WaitTimeoutError:
            speak("No input received. Please try again.")
    return ""

def perform_task(command):
    """Interpret and execute tasks based on user command."""
    if "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}.")
    
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "weather" in command:
        speak("Fetching weather information...")
        api_key = "your_openweathermap_api_key"  # Replace with your API key
        city = "New York"  # Replace with dynamic city input
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            speak(f"The weather in {city} is {desc} with a temperature of {temp}°C.")
        else:
            speak("Unable to fetch weather details.")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I am not sure how to handle that. Please try another command.")

if __name__ == "__main__":
    speak("Hello! I am your personal assistant. How can I help you today?")
    while True:
        user_command = listen()
        if user_command:
            perform_task(user_command)
