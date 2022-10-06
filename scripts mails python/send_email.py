import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(from_addr, from_pass, to_addr,
               subject, body, attachments=None):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        if attachments is None:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(from_addr, from_pass)

            subject = subject
            body = body

            msg = f'Subject: {subject}\n\n\n{body}'

            smtp.sendmail(from_addr, to_addr, msg)
            return

        elif attachments is not None:
            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = from_addr
            message['To'] = to_addr
            message['Subject'] = subject
            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()  # enable security
            session.login(from_addr, from_pass)  # login
            message.attach(MIMEText(body, 'plain'))

            for filename in attachments:
                # The attachments for the mail
                attach_file = open(filename, 'rb')
                mime_attachment = MIMEBase('application', 'octate-stream',
                                           Name=filename)
                mime_attachment.set_payload((attach_file).read())
                encoders.encode_base64(mime_attachment)
                # add mime_attachment header with filename
                message.add_header('Content-Disposition', 'attachment',
                                   filename=filename)
                message.attach(mime_attachment)

            text = message.as_string()
            session.sendmail(from_addr, to_addr, text)
            session.quit()
            return
