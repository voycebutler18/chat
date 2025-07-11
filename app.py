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
            'Authorization': f'Bearer {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}',
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
