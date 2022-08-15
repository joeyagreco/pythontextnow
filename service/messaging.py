import time

from api.TextNowAPI import TextNowAPI
from util import general


def send_sms(message: str, send_to: str):
    """
    Sends an sms text message to this number.
    """
    message = general.replace_newlines(message)
    text_now_api = TextNowAPI()
    text_now_api.send_message(message, send_to)

    time.sleep(1)
