import ssl
import smtplib
from email.message import EmailMessage

class Utilities:
    def __init__(self):
        pass
    @staticmethod
    def send_mail(email_sender,email_receiver,subject,context,email_password):
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(context)

        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls(context=context)
            smtp.login(email_sender, email_password)
            smtp.send_message(em)
            

email_sender = "entrepriseproject8@gmail.com"
email_password = "hustmkrguzpdxptv"
email_receiver= "entrepriseproject8@gmail.com"
subject="Test Subject"
context="this is a test email"

# Utilities.send_mail(email_sender,email_receiver,subject,context,email_password)