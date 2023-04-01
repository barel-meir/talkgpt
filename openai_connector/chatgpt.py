import requests
import logging
import os


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
    if response.status_code == 200:
        generated_text = response_json["choices"][0]["message"]["content"]
        logging.info(generated_text)
    else:
        generated_text = response_json['error']['message']
        logging.error(generated_text)
    return generated_text
