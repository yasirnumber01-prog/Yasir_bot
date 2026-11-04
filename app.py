from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "yasir_bot_123"
WHATSAPP_TOKEN = "EAAgrV7WxZCSsBS6lByrwcZCxhJ5ravsUv9ZCouUcGSwyzu30yIocGHrINmhZCUjXGpU8hZA9WwAd1NYcfOd30dvwVNnZBzW8A1vXnyhDypSKPcklXDOXwudBe8u3JvYIGWCCbCWZAD59KZAji2DgXTVo6tZCt7N51VJN3axqd7UAE3pfiIoUC9LOvS1cfdHmV0TAWHwZAPSmZBbDo9IxR6PWolSQJCqnHFL6foyhZA4TggZDZD"
PHONE_NUMBER_ID = "1408926285639564"

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
            text = msg['text']['body'].lower()
            if 'hi' in text or 'hello' in text or 'salam' in text:
                reply = "Assalam-o-Alaikum! Yasir Bot me khush amdeed. Apna order likh kar bhejein."
            else:
                reply = "Apka message mil gaya: " + msg['text']['body']
            url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
            payload = {"messaging_product": "whatsapp", "to": from_number, "type": "text", "text": {"body": reply}}
            requests.post(url, headers=headers, json=payload)
    except Exception as e:
        print(e)
    return 'OK', 200

@app.route('/')
def home():
    return 'Yasir Bot Live Hai!'

if __name__ == '__main__':
    app.run(port=10000)
