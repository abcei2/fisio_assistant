from django.shortcuts import render

import requests
from django.views.decorators.csrf import csrf_exempt



# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ""
auth_token = ""

# 1). Sacar número del que envia.
# 2). Intentar enviar el video

@csrf_exempt 
def bot(request):
    print(request.body)
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
