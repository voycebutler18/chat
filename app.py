from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

OPENAI_API_KEY = 'sk-...'  # ← paste your real OpenAI API key here

@app.route('/sms', methods=['POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '')
    from_number = request.values.get('From', '')

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {}',
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
