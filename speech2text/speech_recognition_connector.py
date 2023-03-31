import time
import speech_recognition as sr
import logging
from beepy import beep


class SpeechRecognition:
    _recognizer = None

    @staticmethod
    def create():
        if SpeechRecognition._recognizer is None:
            # Initialize recognizer
            SpeechRecognition._recognizer = sr.Recognizer()

    @staticmethod
    def get_input():
        text = ""
        is_success = False
        beep(sound='coin')
        time.sleep(0.5)
        with sr.Microphone() as source:
            logging.debug("waiting for voice input")
            # Use microphone as audio source
            audio = SpeechRecognition._recognizer.listen(source)
        try:
            # Recognize speech using Google Speech Recognition API
            text = SpeechRecognition._recognizer.recognize_google(audio)
            logging.debug(f"recognized input: {text}")
            is_success = True
            beep(sound='ping')
        except sr.UnknownValueError:
            is_success = False
            text = "FAILURE! Google Speech Recognition could not understand audio"
            logging.error(text)
            beep(sound='error')
        except sr.RequestError as e:
            is_success = False
            text = "FAILURE! Could not request results from Google Speech Recognition service"
            logging.error(f"{text} ; {e}")
            beep(sound='error')
        finally:
            return text, is_success

