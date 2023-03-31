class VoiceNotFoundException(Exception):
    error_message = "voice not found"

    def __init__(self, message=None):
        if message is None:
            message = VoiceNotFoundException.error_message
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
