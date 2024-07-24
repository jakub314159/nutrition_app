import smtplib
import os
from random import randint

from email.message import EmailMessage

# from dotenv import load_dotenv
#
# load_dotenv()


class Sender:
    SENDER_EMAIL = "jakub31415926@gmail.com"
    SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
    CODE_MESSAGE = "Here is your verification code {} for NutritionApp."

    def __init__(self, receiver_email):
        self.receiver_email = receiver_email

    def send_verification_message(self) -> str:
        code = "".join([str(randint(0, 9)) for _ in range(4)])

        # msg = EmailMessage()
        # msg.set_content(self.CODE_MESSAGE.format(code))
        # msg["Subject"] = "NutritionApp verification code"
        # msg["From"] = self.SENDER_EMAIL
        # msg["To"] = self.receiver_email
        #
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)
        # server.send_message(msg)
        # server.quit()
        print(code)

        return code
