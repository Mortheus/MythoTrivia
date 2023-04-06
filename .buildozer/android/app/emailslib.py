import smtplib
import ssl

sender = "mytho.trivia@gmail.com"
passw = "mnysakiibjwbrtfb"

port = 465

message = """\
Subject: Welcome to MythoTrivia

Thank you for deciding to try our app, hope you will have lots of fun and learning!!

Best Regards,
MythoTrivia Team
"""
context = ssl.SSLContext()


def send_email_confirmation(email, sender=sender, passw=passw):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, passw)
        server.sendmail(sender, email, message)

