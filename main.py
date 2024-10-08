import speech_recognition as sr  # for speech-to-text
from gtts import gTTS  # for text-to-speech
import ollama  # for language model
import os
from datetime import datetime
import numpy as np
import pygame  # for audio playback
import time  # To add a delay before deleting the file


# Build the AI
class ChatBot():
    def __init__(self, name):
        print("--- starting up", name, "---")
        self.name = name.lower()

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            print("me --> ", self.text)
        except:
            print("me -->  ERROR")

    @staticmethod
    def text_to_speech(text):
        print("emily --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        
        # Initialize pygame mixer and play the audio
        pygame.mixer.init()
        pygame.mixer.music.load("res.mp3")
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pass
        
        # Stop and quit pygame mixer to release the file
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        # Add a small delay before removing the file to ensure it's no longer in use
        time.sleep(1)
        os.remove("res.mp3")

    # Predetermined commands
    def wake_up(self, text):
        lst = ["wake up " + self.name, self.name + " wake up", "hey " + self.name]
        return True if any(i in text.lower() for i in lst) else False

    def what(self, text):
        lst = ["what are you", "who are you"]
        return True if any(i in text.lower() for i in lst) else False

    @staticmethod
    def action_time():
        return datetime.now().time().strftime('%H:%M')


# Run the AI
if __name__ == "__main__":
    ai = ChatBot(name="Emily")

    while True:
        ai.speech_to_text()

        # Wake up
        if ai.wake_up(ai.text):
            res = "Hello, I am Emily the AI, what can I do for you?"

        # What are you / Who are you
        elif ai.what(ai.text):
            res = "I am an AI created by Souradip."

        # Ask for time
        elif "time" in ai.text:
            res = ai.action_time()

        # Respond politely to thanks
        elif any(i in ai.text for i in ["thank", "thanks"]):
            res = np.random.choice([
                "You're welcome!", "Anytime!", "No problem!", 
                "Cool!", "I'm here if you need me!", "Peace out!"
            ])

        # General conversation using the language model
        else:
            res = ollama.generate(model="emily", prompt=ai.text)["response"]
            res = res.split("\n")[0]

        # Text-to-speech response
        ai.text_to_speech(res)
