import re
import dns.resolver
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_jwt_extended import create_access_token
from datetime import timedelta
import time
import uuid
from datetime import datetime
def is_valid_email(email):
    """
    Validate the format of an email address and check if the domain has valid MX records.
    Returns True if the email is valid, False otherwise.
    """
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    if not email_pattern.match(email):
        return False

    _, domain = email.split('@')

    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return True
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.Timeout:
        return False
def send_email(to_email, subject, body):
    """
    Send an email using Gmail's SMTP server.
    Returns True if the email is sent successfully, False otherwise.
    """
    sender_email = 'warzone20082003@gmail.com'
    app_password = 'gljuewbykblyyyzv'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def is_valid_password(password):
    # Check if the password is at least 8 characters long
    if len(password) < 8:
        return False

    # Check if the password contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check if the password contains at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # Check if the password contains at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # Check if the password contains at least one special character
    special_characters = r'[!@#$%^&*(),.?":{}|<>]'
    if not re.search(special_characters, password):
        return False

    # If all checks pass, the password is valid
    return True

def generate_access_token(username):
    # Set the expiration time for 24 hours
    expires = timedelta(hours=24)

    # Create and return the access token
    access_token = create_access_token(identity=username, expires_delta=expires)
    return access_token

def generate_unique_filename(file_extension):
    # Use timestamp and UUID to create a unique filename
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4().hex)[:8]  # Use the first 8 characters of the UUID
    filename = f"{timestamp}_{unique_id}.{file_extension}"
    return filename

def set_true_after_5_minutes():
    flag = False
    time.sleep(120)
    flag = True
    return flag