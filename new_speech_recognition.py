import speech_recognition as sr
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence


def silence_based_conversion(path):
    """
    a function that divides the audio file into pieces
    """
    song = AudioSegment.from_wav(path)

    f = open("recognised_text.txt", "w+")
    pieces = split_on_silence(song, min_silence_len=400, silence_thresh=-50)
    # split file where silence is at least 1 second

    # store little audio files
    try:
        os.mkdir('audio_pieces')
    except(FileExistsError):
        pass

    i = 0
    for piece in pieces:

        piece_silent = AudioSegment.silent(duration=2000)
        # add a few seconds silence to the beginning and to the end of audio file
        # it's necessary, because we don't want to miss any word
        audio_piece = piece_silent + piece + piece_silent

        print("saving piece{0}.wav".format(i))
        audio_piece.export("./audio_pieces/piece{0}.wav".format(i), bitrate='192k', format="wav")

        filename = 'piece' + str(i) + '.wav'
        print("Processing piece " + str(i))

        file = filename
        r = sr.Recognizer()  # using the audio file as the audio source

        # recognize the file
        with sr.AudioFile(file) as source:
            # r.adjust_for_ambient_noise(source)  # to reduce noise (use it in case there is music/noise in audio book
            audio_listened = r.record(source)

        try:
            rec = r.recognize_sphinx(audio_listened)
            f.write(rec + ". ")

        except sr.UnknownValueError:
            raise ValueError("didn't recognise")

        except sr.RequestError as e:
            print("smth wrong with service; {0}".format(e))

        i += 1



silence_based_conversion('resources/chapter1.wav')
