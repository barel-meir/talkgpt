import requests
import logging
import os
from text2speech import pyttsx3_connector


def create_directory(path):
    """
    Create a directory path if it doesn't exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def init_logging():
    log_file_path = "~/.talkgpt/log"
    create_directory(log_file_path)
    log_file_name = "talk.log"
    file_path = os.path.join(log_file_path, log_file_name)

    # Create a logger and set its level to DEBUG
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler that writes to the specified log file
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a console handler that writes to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def request_gpt_answer(message_content: str):
    # Define the API endpoint URL and API key
    try:
        logging.debug("fetching open ai api key from env")
        api_key = os.environ.get('gptusr')
        if api_key is None:
            raise KeyError
    except KeyError:
        logging.error("could not find open ai api key")
        return "(!) Failed to send message"

    url = "https://api.openai.com/v1/chat/completions"

    # Define the payload to send in the API request
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message_content}]
    }

    # Define the headers to send in the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    logging.debug(f"sending request payload: {payload}")
    # Send the API request and receive the response
    response = requests.post(url, headers=headers, json=payload)

    # Parse the JSON response and extract the generated text
    response_json = response.json()
    generated_text = response_json["choices"][0]["message"]["content"]
    logging.info(generated_text)
    return generated_text


def initialize():
    init_logging()
    pyttsx3_connector.PyttsxConnector.create()


def main():
    initialize()
    message = "Hello, ChatGPT! Can you give me a witty joke?"
    answer = request_gpt_answer(message)
    pyttsx3_connector.PyttsxConnector.speak(answer)


if __name__ == '__main__':
    main()

