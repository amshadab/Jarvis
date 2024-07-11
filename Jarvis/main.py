import speech_recognition as sr
import webbrowser
import pyttsx3
import Library
import requests
import os
from datetime import datetime
from hugchat import hugchat

# pip install pocketsphinx
# pip install ibm-watson

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "a988fc6991da4716967b8d384ae2ef97"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def chatBot(query):
    try:
        user_input = query.lower()
        chatbot = hugchat.ChatBot(cookie_path="cookies.json")
        conversation_id = chatbot.new_conversation()
        chatbot.change_conversation(conversation_id)
        response = chatbot.chat(user_input)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

def processcommand(c):
    if "open google" in c.lower():
        speak("Google is opening...")
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        speak("Youtube is opening...")
        webbrowser.open("https://youtube.com")
        song = c.lower().replace("play", "").strip()
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = Library.music[song]
        webbrowser.open(link)
    elif "open vs code" in c.lower():
        speak("VS code is opening")
        codepath = "C:\\Users\\shada\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codepath)
    elif "current time" in c.lower():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        speak(f"Current time is {current_time}")
    elif "current date" in c.lower():
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        speak(f"Current date is {current_date}")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            news_data = r.json()
            articles = news_data['articles']
            for article in articles:
                speak(article['title'])
    elif "jarvis stop" in c.lower():
        speak("Good Bye, Sir")
        return False  
    else:
        response = chatBot(c)
        print(f"Chatbot response: {response}")  # Debugging line to check response
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes")
                with sr.Microphone() as source:
                    print("Jarvis Active")
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                    command = recognizer.recognize_google(audio)
                    
                    result = processcommand(command)
                    if result == False:
                        break
                    
        except Exception as e:
            print("Error: {0}".format(e))
