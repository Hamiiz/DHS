import requests
import json
import random as r

API_KEY = 'CHASECK_TEST-hycufSWVWycBiGYxxKYsKoiKfJhIAyeR'
def txn_gen():
    return f'chapatest{r.randint(0, 9999)*r.randint(1,999)+r.randint(0, 99)}'

def chapa_payment_init(amt, patient,reason):      

    url = "https://api.chapa.co/v1/transaction/initialize"
    payload = {
        "amount": str(amt),
        "currency": "ETB",
        "email": 'abebech_bekele@gmail.com',
        "first_name":patient.name,
        # "last_name": 'Gizachew',
        "phone_number": "0912345678",
        "tx_ref": txn_gen(),
        "callback_url": "https://webhook.site/01fdfa0e-8fd1-48a9-965d-1ffe73948501",
        "return_url": f"http://127.0.0.1:8000/payment_success/{reason}/{patient.id}",
        "customization": {
        "title": "Card fees",
        "description": "A fee for a hospital access card"
        }
        }
    headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
        }
        
    response = requests.post(url, json=payload, headers=headers)
    return response,payload["tx_ref"]

def verify_payment(txn_id):
    url = "https://api.chapa.co/v1/transaction/verify/chewatatest-6669"
    payload = ''
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    response = requests.get(url, headers=headers, data=payload)
    
    return response


