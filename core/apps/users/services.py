import requests
from requests.exceptions import Timeout
import os
from dotenv import load_dotenv
load_dotenv()

NIKITA_LOGIN = 'navis'
NIKITA_PASSWORD = '5zBQ31XH'
NIKITA_SENDER = 'Navis'

def send_sms(phone, message, code):
    # user = User.objects.get(phone=phone)
    new_phone = "".join(filter(str.isdigit, phone))
    xml_data = f"""<?xml version="1.0" encoding="UTF-8"?><message><login>{NIKITA_LOGIN}</login><pwd>{NIKITA_PASSWORD}</pwd><sender>{NIKITA_SENDER}</sender><text>{message}:\n{code}</text><phones><phone>{new_phone}</phone></phones></message>"""

    headers = {"Content-Type": "application/xml"}

    url = "https://smspro.nikita.kg/api/message"

    response = requests.post(url, data=xml_data.encode("utf-8"), headers=headers)

    print(f"\n\n{response.text}\n\n")
    with open("nikita.log", "a") as file:
        file.write(response.text + "\n\n")

    if response.status_code == 200:
        return True
    return False
