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
        answer = None
        message, is_success = speech_recognition_connector.SpeechRecognition.get_input()
        if is_success:
            answer = request_gpt_answer(message)
            pyttsx3_connector.PyttsxConnector.speak(answer)
        else:
            pyttsx3_connector.PyttsxConnector.speak(message)

        return message, answer, is_success


    @staticmethod
    def speech2text():
        return speech_recognition_connector.SpeechRecognition.get_input()


    @staticmethod
    def ask_gpt(text: str):
        answer = request_gpt_answer(text)
        return answer

    @staticmethod
    def text2speech(text: str):
        pyttsx3_connector.PyttsxConnector.speak(text)
