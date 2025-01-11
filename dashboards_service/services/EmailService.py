import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailService:
    @staticmethod
    def send_discount_email(customer_email: str, message: str):
        """
        Send the discount notification as an email.

        Input:
        - customer_email: Email address of the recipient.
        - message: discount messaage.

        Output:
        - None (raises exception on failure).
        """
        sender_email = "bugrayapilmisev@gmail.com"  # Replace with your email
        sender_password = "olee olco ingu upeb"  # Replace with your app-specific password
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email
        subject = "There is a Discount for your Wishlist!"
        body = message

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = customer_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        

        # Send the email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, customer_email, msg.as_string())
            server.quit()
            print(f"Email sent successfully to {customer_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise
