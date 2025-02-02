from flask_mail import Message
from ..db import mail 

def send_email_notification(user_email, message):
  msg = Message("Low Stock Alert", recipients=[user_email])
  msg.body = message

  try:
    mail.send(msg)
    print(f"Email sent to {user_email}")
  except Exception as e:
    print(f"Failed to send email to {user_email}: {e}")