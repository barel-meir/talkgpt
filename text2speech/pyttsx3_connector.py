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
        desired_voice = 'english-us'
        # Create a TTS engine
        PyttsxConnector._engine = pyttsx3.init()
        # Set the voice
        voice_id = None
        for current_voice in PyttsxConnector._engine.getProperty('voices'):
            if current_voice.name == desired_voice:
                voice_id = current_voice.id
                break

        if voice_id is None:
            #     todo add log error
            raise VoiceNotFoundException.VoiceNotFoundException

        PyttsxConnector._engine.setProperty('voice', voice_id)  # Use the first voice in the list
        # Set the speech rate
        PyttsxConnector._engine.setProperty('rate', 150)

    @staticmethod
    def speak(text: str):
        # Convert text to speech
        PyttsxConnector._engine.say(text)
        # Run the TTS engine
        PyttsxConnector._engine.runAndWait()
