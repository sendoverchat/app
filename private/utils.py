import smtplib, ssl, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import session, request, render_template

config = json.load(open("config.json", "r"))

def verify_token():

    if "user" in session:
        return True

    return False

class NavBarType:
    nonavbar = 0
    navbar = 1
    sidebar = 2

class StatusType:
    offline = 0
    online = 1
    do_not_distrub = 2
    invisible = 3 

def custom_template(
    site_page : str,
    title : str,
    description : str,
    styles : list,
    navbar_type : int = NavBarType.nonavbar,
    **context
):
    
    theme = request.cookies.get("theme")
    return render_template("index.html", site_page=site_page,title=title,description=description,styles=styles, navbar_type=navbar_type, theme=theme, **context)



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

    message.attach(MIMEText(body, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
