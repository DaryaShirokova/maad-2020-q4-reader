import speech_recognition as sr
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence


def silence_based_conversion(path):  # a function that divides the audio file into pieces
    song = AudioSegment.from_wav(path)

    fh = open("recognised_text.txt", "w+")
    pieces = split_on_silence(song, min_silence_len=1000, silence_thresh=-50)
    # split file where silence is at least 1 second

    # store little audio files
    try:
        os.mkdir('audio_pieces')
    except(FileExistsError):
        pass

    os.chdir('audio_pieces')

    i = 0
    for piece in pieces:

        piece_silent = AudioSegment.silent(duration=1000)
        # add a few seconds silence to the beginning and to the end of audio file
        # it's necessary, because we don't want to miss any word
        audio_piece = piece_silent + piece + piece_silent

        print("saving piece{0}.wav".format(i))
        audio_piece.export("./piece{0}.wav".format(i), bitrate='192k', format="wav")

        filename = 'piece' + str(i) + '.wav'
        print("Processing piece " + str(i))

        file = filename
        r = sr.Recognizer()  # using the audio file as the audio source

        # recognize the file
        with sr.AudioFile(file) as source:
            # r.adjust_for_ambient_noise(source)  # to reduce noise (use it in case there is music/noise in audio book
            audio_listened = r.record(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened)
            # write the output to the file.
            fh.write(rec + ". ")

        except sr.UnknownValueError:
            print("didn't recognise")

        except sr.RequestError as e:
            print("smth wrong with service; {0}".format(e))

        i += 1

    os.chdir('..')


silence_based_conversion('resources/chapter1.wav')
