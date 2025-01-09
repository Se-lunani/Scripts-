import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

def send_email(subject, body):
    sender_email = "your_email@example.com"
    receiver_email = "admin@example.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Alert email sent successfully.")
    except Exception as e:
        print("Failed to send email. Error: ", e)
        print("Alert message: ")
        print(body)

def monitor_system():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    alert_message = ""
    if cpu_usage > 10:
        alert_message += f"High CPU usage detected: {cpu_usage}%\n"
    if memory.percent > 10:
        alert_message += f"High memory usage detected: {memory.percent}%\n"
    if disk.percent > 10:
        alert_message += f"High disk usage detected: {disk.percent}%\n"

    if alert_message:
        send_email("System Alert", alert_message)

if __name__ == "__main__":
    while True:
        monitor_system()
        time.sleep(300)  # Wait for 5 minutes (300 seconds) before checking again
