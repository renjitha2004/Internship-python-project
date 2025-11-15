import imaplib
import email
from  dotenv import load_dotenv
import os

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD=os.getenv("PASSWORD")
  # Use App Password if 2FA is enabled

def get_emails_with_pdfs():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    typ, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    
    pdf_attachments = []

    for e_id in reversed(email_ids):
        typ, msg_data = mail.fetch(e_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        for part in msg.walk():
            filename=part.get_filename()
            if part.get_content_maintype() == 'application' and part.get_filename().endswith('.pdf'):
                pdf_attachments.append((e_id, filename, part.get_payload(decode=True)))

    return pdf_attachments,mail

if __name__ == "__main__":
    attachments = get_emails_with_pdfs()
    print(f"\nTotal PDFs found: {len(attachments)}")

