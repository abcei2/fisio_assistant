from django.shortcuts import render

import requests
from twilio.twiml.messaging_response import MessagingResponse

from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC0d15ec2e3c206afdff8251c3b073945d"
auth_token = "36163ffb00825dcb98027c9403add994"

client = Client(account_sid, auth_token)
app = Flask(__name__)


# 1). Sacar número del que envia.
# 2). Intentar enviar el video

def bot(request):
    print(request)
    incoming_msg = request.values.get('Body', '').lower()
    from_who = request.values.get('From', '').lower()
    print(from_who, incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run(host ="0.0.0.0")