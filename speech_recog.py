import speech_recognition as sr
import wave
import contextlib

from os import path

filename = 'resources/direct.wav'
with contextlib.closing(wave.open(filename, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = int(frames / float(rate))
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "resources/direct.wav")

r = sr.Recognizer()  # using the audio file as the audio source

with sr.AudioFile(AUDIO_FILE) as source:
    # r.adjust_for_ambient_noise(source)  # to reduce noise (use it in case there is music/noise in audio book)
    audio = r.record(source)  # reading the entire audio file

try:
    text = r.recognize_sphinx(audio)  # recognizing speech using Google Speech Recognition
    # result = re.sub("(.{64,80} )", "\\1\n", text, 0, re.DOTALL)  # splitting the text to multiple lines
    # result1 = re.sub("(.{64,80} )", "\\1\n", text1, 0, re.DOTALL)
    f = open('recognised_text1.txt', 'a')  # writing recognised audio to .txt file
    f.write(text)
    f.write(' ')

    f.close()
except sr.UnknownValueError:
    raise ValueError("didn't recognise")
except sr.RequestError as e:
    print("smth wrong with service; {0}".format(e))

