class OpenAiApiKeyNotFoundException(Exception):
    error_message = "open ai api key not found"

    def __init__(self, message=None):
        if message is None:
            message = OpenAiApiKeyNotFoundException.error_message
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
