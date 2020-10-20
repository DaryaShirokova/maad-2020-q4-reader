import speech_recognition as sr
import re
from os import path


AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "test.wav")

r = sr.Recognizer()  # using the audio file as the audio source
with sr.AudioFile(AUDIO_FILE) as source:
    # r.adjust_for_ambient_noise(source)  # to reduce noise (use it in case there is music/noise in audio book)
    audio = r.record(source)  # reading the entire audio file


try:
    text = r.recognize_google(audio)  # recognizing speech using Google Speech Recognition
    result = re.sub("(.{64,80} )", "\\1\n", text, 0, re.DOTALL)  # splitting the text to multiple lines
    print(result)
except sr.UnknownValueError:
    print("didn't recognise")
except sr.RequestError as e:
    print("smth wrong with service; {0}".format(e))

