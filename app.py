import os
from flask import Flask, request
import requests
import google.generativeai as genai

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "yasir_bot_123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "1408926285639564")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def receive():
    data = request.get_json()
    print(data)
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            from_number = msg['from']
            text = msg['text']['body']
            print("User:", text)
            try:
                reply = model.generate_content(f"Tum Yasir ka helpful WhatsApp assistant ho. Roman Urdu me short aur friendly jawab do. User: {text}").text
            except Exception as e:
                print(e)
                reply = "Sorry, abhi thora masla hai, dobara try karein."
            url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
            payload = {"messaging_product": "whatsapp", "to": from_number, "type": "text", "text": {"body": reply}}
            requests.post(url, headers=headers, json=payload)
    except Exception as e:
        print(e)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
