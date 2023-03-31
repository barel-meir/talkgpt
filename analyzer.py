from openai_connector.chatgpt import request_gpt_answer
from text2speech import pyttsx3_connector
from speech2text import speech_recognition_connector

class Analyzer:
    @staticmethod
    def initialize():
        pyttsx3_connector.PyttsxConnector.create()
        speech_recognition_connector.SpeechRecognition.create()

    @staticmethod
    def analyze():
        message, is_success = speech_recognition_connector.SpeechRecognition.get_input()
        if is_success:
            answer = request_gpt_answer(message)
            pyttsx3_connector.PyttsxConnector.speak(answer)
        else:
            pyttsx3_connector.PyttsxConnector.speak(message)
