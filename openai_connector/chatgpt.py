import requests
import logging
import os

from exceptions.OpenAiApiKeyNotFoundException import OpenAiApiKeyNotFoundException


class ChatGptConnector:
    _api_key = None
    @staticmethod
    def initialize():
        global _api_key
        # Define the API endpoint URL and API key
        try:
            logging.debug("fetching open ai api key from env")
            if os.environ.get('gptusr') is None:
                raise KeyError
            else:
                _api_key = os.environ.get('gptusr')
        except KeyError:
            logging.error("could not find open ai api key")


    @staticmethod
    def is_api_key_initiated():
        return not(_api_key is None)

    @staticmethod
    def set_api_key(api_key: str):
        global _api_key
        logging.debug("setting open ai api key from user input")
        _api_key = api_key


    @staticmethod
    def request_gpt_answer(message_content: str):
        if not ChatGptConnector.is_api_key_initiated():
            raise OpenAiApiKeyNotFoundException

        url = "https://api.openai.com/v1/chat/completions"

        # Define the payload to send in the API request
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message_content}]
        }

        # Define the headers to send in the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_api_key}"
        }

        logging.debug(f"sending request payload: {payload}")
        # Send the API request and receive the response
        response = requests.post(url, headers=headers, json=payload)

        # Parse the JSON response and extract the generated text
        response_json = response.json()
        if response.status_code == 200:
            generated_text = response_json["choices"][0]["message"]["content"]
            logging.info(generated_text)
        else:
            generated_text = response_json['error']['message']
            logging.error(generated_text)
        return generated_text
