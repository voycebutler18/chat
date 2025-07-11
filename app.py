from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

# Securely get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('CHATGPT_API_KEY')

@app.route('/sms', methods=['POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '')
    from_number = request.values.get('From', '')

    # Send message to OpenAI ChatGPT
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': incoming_msg}]
        }
    )

    reply = response.json()['choices'][0]['message']['content']

    # Create Twilio response to send back
    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == '__main__':
    app.run()
