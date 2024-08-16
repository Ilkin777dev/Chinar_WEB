import os
import smtplib
from email.message import EmailMessage

def send_email(reciever, message, subject, title) -> None:
    """
    Sends an email to the specified receiver with the given message, subject, and title.

    Parameters:
    - receiver (str): The email address of the receiver.
    - message (str): The content of the email message.
    - subject (str): The subject of the email.
    - title (str): The title to be substituted in the email template.

    Returns:
    None
    """
    email = EmailMessage()
    email["from"] = "Abyssara"
    email["to"] = reciever
    email["subject"] = subject

    gmail_username = os.environ.get("MAIL_USERNAME")
    gmail_password = os.environ.get("MAIL_PASSWORD")

    email.set_content(title + "\n\n" + message)
    
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(gmail_username, gmail_password)
        smtp.send_message(email)