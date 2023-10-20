import requests


def send_post_request(text):
    url = 'http://localhost:8000/queue_reverse_text'
    payload = {'text': text}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(response.text)
    else:
        print(f'POST request failed. Status Code: {response.status_code}')


if __name__ == '__main__':
    while True:
        user_input = input("Enter text (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        send_post_request(user_input)
