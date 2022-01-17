import speech_recognition as sr
import numpy as np
import cv2
from ffpyplayer.player import MediaPlayer
import keyboard

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success":True,
        "error":None,
        "transcription":None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language="fr-FR")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        if ret == True:
            if cv2.waitKey(31) & 0xFF == ord('q'):
                break
            cv2.imshow('Frame', frame)
            if val != 'eof' and audio_frame is not None:
                img, t = audio_frame
        else: 
            break

    player.close_player()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    video_path = 'sarko_cut.webm'
    trigger_word = 'bonjour'

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Ready to work")

    i = True

    while i is True:
        guess = recognize_speech_from_mic(recognizer, microphone)

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break
        print("u said: {}".format(guess["transcription"]))

        word_is_trigger = guess["transcription"].lower() == trigger_word.lower()

        if word_is_trigger:
            print("nice word")
            play_video(video_path)

