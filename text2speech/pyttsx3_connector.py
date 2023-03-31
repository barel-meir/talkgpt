import logging

import pyttsx3
from exceptions import VoiceNotFoundException


class PyttsxConnector:
    _engine = None

    @staticmethod
    def create():
        if PyttsxConnector._engine is None:
            PyttsxConnector._init_engine()

    @staticmethod
    def _init_engine():
        logging.debug(f"creating pyttsx3 engine")
        desired_voice = 'english-us'
        logging.debug(f"desired voice: {desired_voice}")
        # Create a TTS engine
        PyttsxConnector._engine = pyttsx3.init()
        # Set the voice
        voice_id = None
        for current_voice in PyttsxConnector._engine.getProperty('voices'):
            if current_voice.name == desired_voice:
                voice_id = current_voice.id
                break

        if voice_id is None:
            logging.error(f"could not find desired voice {desired_voice}")
            raise VoiceNotFoundException.VoiceNotFoundException

        PyttsxConnector._engine.setProperty('voice', voice_id)
        # Set the speech rate
        PyttsxConnector._engine.setProperty('rate', 200)

    @staticmethod
    def speak(text: str):
        # Convert text to speech
        PyttsxConnector._engine.say(text)
        # Run the TTS engine
        PyttsxConnector._engine.runAndWait()
