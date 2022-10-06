from send_email import send_email
import os
from datetime import datetime


myaddres = 'cuenta de gmail'
mypasswrd = 'pass de gmail apps'

script_title = 'test mails'
script_config = os.path.basename(
    os.path.dirname(os.path.realpath(__file__)))

# send mail

subject = f'Resultados de {script_title} - config {script_config}'
dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
body = f"""Enviado el {dt}."""

files = ['send_email.py', 'enviar_files.py', 'pytest.py', 'bashtest.sh']

send_email(myaddres, mypasswrd, myaddres,
           subject, body,
           files)

