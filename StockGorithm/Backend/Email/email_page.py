from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
sender_email =  "Provide the Email"
receiver_email = "Provide the Email"
sender_name = "StockGorithm"
password = "Provide the password"

# Email content
subject = "Stockgorithm OTP"

def send_mail(data,otp):
    print('Email Data:', data)
    
    # Email body with placeholders replaced by data from JSON
    body = f"""
    Dear Customer,

    Thank you for signing up with Stockgorithm. Here is your OTP for verification.

    Your SignUp Details:
    Gmail ID: {data['email']}
    OTP: {otp}

    If you have any questions or require further assistance, please feel free to reach out to us at +91 9037074839.

    We look forward to welcoming you and hope you have a wonderful stay with us!

    Warm regards,
    Stockgorithm
    """
    
    # Email configuration
    message = MIMEMultipart()
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = data['email']
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail's SMTP server and send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)  # Log in to your email
            server.sendmail(sender_email, data['email'], message.as_string())  # Send the email
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False