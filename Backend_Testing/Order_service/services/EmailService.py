import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailService:
    @staticmethod
    def send_invoice_email(customer_email: str, invoice_path: str):
        """
        Send the invoice PDF as an email attachment.

        Input:
        - customer_email: Email address of the recipient.
        - invoice_path: Path to the generated invoice PDF.

        Output:
        - None (raises exception on failure).
        """
        sender_email = "bugrayapilmisev@gmail.com"  # Replace with your email
        sender_password = "olee olco ingu upeb"  # Replace with your app-specific password
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email
        subject = "Your Invoice from Our Store"
        body = "Thank you for your purchase! Please find your invoice attached."

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = customer_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Attach the PDF
        with open(invoice_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(invoice_path)}",
        )
        msg.attach(part)

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
