import ssl
import smtplib
from email.message import EmailMessage
import datetime 

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
            
    @staticmethod
    def get_last_6_months():
        now = datetime.datetime.now()
        result = [{'year':now.strftime("%Y%B")[:4],'month':now.strftime("%Y%B")[4:]}]
        for _ in range(0, 6):
            now = now.replace(day=1) - datetime.timedelta(days=1)
            result.append({'year':now.strftime("%Y%B")[:4],'month':now.strftime("%Y%B")[4:]})
            
        return result
email_sender = "entrepriseproject8@gmail.com"
email_receiver= "entrepriseproject8@gmail.com"
subject="Test Subject"
context="this is a test for ahmed"
email_password = "hustmkrguzpdxptv"
# Utilities.send_mail(email_sender,email_receiver,subject,context,email_password)