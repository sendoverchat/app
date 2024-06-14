import smtplib, ssl, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


config = json.load(open("config.json", "r"))

class NavBarType:
    nonavbar = 0
    navbar = 1
    sidebar = 2

class StatusType:
    offline = 0
    online = 1
    do_not_distrub = 2
    invisible = 3 

def sendEmail(sujet, body, email):
    port = config["smtp_port"]
    smtp_server = config["smtp_host"]
    sender_email = config["smtp_email"]
    receiver_email = email
    password = config["smtp_password"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = sujet

    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
