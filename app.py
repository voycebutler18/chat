from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '')
    from_number = request.values.get('From', '')

    # Get your API key securely from environment
    openai_api_key = os.getenv("CHATGPT_API_KEY")

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {openai_api_key}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': incoming_msg}]
        }
    )

    reply = response.json()['choices'][0]['message']['content']

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == '__main__':
    app.run()
