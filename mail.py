import smtplib, ssl

port = 465  # For SSL
password = "BHRlFykv7T/eLNvZCpfNxrk0g+0THszM+5Bd7jv71bQU"

sender_email = "benfelip@amazon.com"  # Enter your address
receiver_email = "benfelip@amazon.com"  # Enter receiver address

message = """\
Subject: Hi there

This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("email-smtp.us-east-1.amazonaws.com", port, context=context) as server:
    server.login("AKIAQ47O74YG7YXIQCR7", password)
    server.sendmail(sender_email, receiver_email, message)
