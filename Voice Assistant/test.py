import pyttsx3
engine=pyttsx3.init()
engine.setProperty('rate', 190)
engine.say("Enter your text here...")
engine.runAndWait()