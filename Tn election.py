import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database connection
conn = sqlite3.connect('election.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS voters (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        voted INTEGER DEFAULT 0
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

# Function to send email
def send_email(voter_email, candidate_name):
    smtp_server = 'smtp.example.com'  # Replace with your SMTP server
    smtp_port = 587  # Replace with your SMTP port
    sender_email = 'your_email@example.com'  # Replace with your email
    sender_password = 'your_password'  # Replace with your password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = voter_email
    msg['Subject'] = 'Thank you for voting'

    body = f"Thank you for voting for {candidate_name}. Your vote has been recorded."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, voter_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {voter_email}")
    except Exception as e:
        print(f"Failed to send email to {voter_email}. Error: {str(e)}")

# Function to conduct voting
def conduct_vote(voter_email, candidate_id):
    try:
        cursor.execute("SELECT name FROM candidates WHERE id=?", (candidate_id,))
        candidate_name = cursor.fetchone()[0]
        cursor.execute("UPDATE voters SET voted=1 WHERE email=?", (voter_email,))
        conn.commit()
        send_email(voter_email, candidate_name)
        print(f"Vote successfully cast for {candidate_name} by {voter_email}")
    except Exception as e:
        print(f"Failed to cast vote. Error: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Example of conducting a vote
    voter_email = 'voter1@example.com'
    candidate_id = 1
    conduct_vote(voter_email, candidate_id)

    # Example of sending an email (unrelated to voting but shows email sending functionality)
    # send_email('recipient@example.com', 'Candidate A')

