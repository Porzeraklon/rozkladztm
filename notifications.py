import smtplib, ssl, imaplib, email, traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def notify(subject):
    sender = 'GdzieJestKluczGRAL@gmail.com'
    rec = 'beldegrin.damian@gmail.com'
    passwd = 'nbvjmotbtsfhggxf'
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = rec
    message['Subject'] = str(subject)
    print(subject)
    html = '<h1>Zmiana pozycji klucza</h1>'
    message.attach(MIMEText(html, "html"))
    message = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, passwd)
        print("Zalogowano")
        server.sendmail(sender, rec, message)
        print("Wyslano")
