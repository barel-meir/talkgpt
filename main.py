import requests

def request_gpt_answer(message_content: str):
    # Define the API endpoint URL and API key
    url = "https://api.openai.com/v1/chat/completions"
    api_key = "<api-key>>"

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

    # Send the API request and receive the response
    response = requests.post(url, headers=headers, json=payload)

    # Parse the JSON response and extract the generated text
    response_json = response.json()
    generated_text = response_json["choices"][0]["message"]["content"]
    return generated_text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    message = "Hello, ChatGPT! Can you give me a witty joke?"
    print(request_gpt_answer(message))
