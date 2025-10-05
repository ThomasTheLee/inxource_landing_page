import os
import smtplib
from email.message import EmailMessage

class Communication:
    """Handles all communication functions (e.g., sending emails from the landing page)."""

    def __init__(self, smtp_user, smtp_password, smtp_server="smtp.gmail.com", smtp_port=465):
        """
        Initialize communication handler.

        :param smtp_user: The email address used to send (your Gmail business email).
        :param smtp_password: App password or SMTP password.
        :param smtp_server: SMTP server host (default: Gmail).
        :param smtp_port: SMTP port (465 for SSL).
        """
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        if not self.smtp_user or not self.smtp_password:
            raise ValueError("SMTP user and password must be provided (or set as env vars).")

    def send_email(self, subject, body, visitor_email, receiver_email=None):
        """
        Send an email via SMTP.

        :param subject: Email subject
        :param body: Email message body
        :param visitor_email: The email of the person who filled the form
        :param receiver_email: Where to send the email (defaults to smtp_user self-email)
        """
        receiver_email = receiver_email or self.smtp_user

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = receiver_email
        msg["Reply-To"] = visitor_email   # so you can reply directly to the visitor
        msg.set_content(f"From: {visitor_email}\n\n{body}")

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True, "Email sent successfully."
        except Exception as e:
            return False, f"Failed to send email: {e}"

