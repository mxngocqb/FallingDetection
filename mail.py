import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class SMTPClient:
    def __init__(self, smtp_server, smtp_port, username, password):
        """
        Initialize the SMTP client with server details and credentials.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email_to_list_with_attachment(self, from_email, to_emails, subject, body, attachment=None, attachment_filename=None):
        """
        Send an email with an attachment to multiple recipients using Gmail's SMTP server.
        :param from_email: Sender's email address
        :param to_emails: List of recipient email addresses
        :param subject: Email subject
        :param body: Email body content
        :param attachment: Attachment file data (in bytes), optional
        :param attachment_filename: Filename for the attachment, optional
        """
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = from_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Attach the image if provided
        if attachment and attachment_filename:
            image_attachment = MIMEImage(attachment, name=attachment_filename)
            message.attach(image_attachment)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)

                # Danh sách các email người nhận
                message["To"] = ", ".join(to_emails)  # Ghép danh sách email thành chuỗi ngăn cách bởi dấu phẩy
                server.send_message(message)  # Gửi email một lần
                print(f"Email sent successfully to: {', '.join(to_emails)}")
        except Exception as e:
            print(f"Failed to send email: {e}")

