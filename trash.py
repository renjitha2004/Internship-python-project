import imaplib
from dotenv import load_dotenv
import os

# ✅ Load email credentials
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def move_email_to_trash(email_id: bytes):
    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        # Copy to Gmail Trash
        mail.copy(email_id, '[Gmail]/Trash')

        # Mark original email as deleted
        mail.store(email_id, '+FLAGS', r'(\Deleted)')
        mail.expunge()

        print(f"🗑️ Email {email_id.decode()} successfully moved to Trash.")

        mail.logout()
    except Exception as e:
        print(f"❌ Failed to move email to Trash: {e}")

# ✅ Optional test run (remove or comment this when importing)
if __name__ == "__main__":
    # Example usage: move the most recent email to trash
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    typ, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    if email_ids:
        latest_email_id = email_ids[-1]
        move_email_to_trash(latest_email_id)
    else:
        print("📭 No emails found.")
