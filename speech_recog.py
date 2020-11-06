import speech_recognition as sr
import re
import wave
import contextlib

from os import path

fname = 'resources/test.wav'
with contextlib.closing(wave.open(fname, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = int(frames / float(rate))
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "resources/test.wav")

r = sr.Recognizer()  # using the audio file as the audio source

with sr.AudioFile(AUDIO_FILE) as source:
    # r.adjust_for_ambient_noise(source)  # to reduce noise (use it in case there is music/noise in audio book
    audio = r.record(source, duration=duration // 2)  # reading the entire audio file
    audio1 = r.record(source)


try:
    text = r.recognize_google(audio, language='en-US')  # recognizing speech using Google Speech Recognition
    text1 = r.recognize_google(audio1, language='en-US')
    final_text = text + ' ' + text1
    # result = re.sub("(.{64,80} )", "\\1\n", text, 0, re.DOTALL)  # splitting the text to multiple lines
    # result1 = re.sub("(.{64,80} )", "\\1\n", text1, 0, re.DOTALL)
    f = open('recognised_text.txt', 'w')
    f.write(final_text)
    f.close()
except sr.UnknownValueError:
    print("didn't recognise")
except sr.RequestError as e:
    print("smth wrong with service; {0}".format(e))

