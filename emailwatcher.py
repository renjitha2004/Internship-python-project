import time
from dotenv import load_dotenv
import os
from trash import move_email_to_trash
from ocr import get_emails_with_pdfs, run_ocr_on_pdf  # Update with actual module name

load_dotenv()

CHECK_INTERVAL = 60  # in seconds 
PROCESSED_IDS = set()  # to avoid reprocessing same emails in the same session

def process_new_emails():
    attachments, mail = get_emails_with_pdfs()
    print(f"\n📬 Total PDFs found: {len(attachments)}")

    for e_id, filename, pdf_data in attachments:
        if e_id not in PROCESSED_IDS:
            print(f"🔄 Processing email ID: {e_id.decode()}")
            run_ocr_on_pdf(pdf_data, pdf_name=filename.replace(".pdf", ""))
            move_email_to_trash(e_id)
            PROCESSED_IDS.add(e_id)
        else:
            print(f"⏩ Email {e_id.decode()} already processed.")

def start_watching():
    print("📡 Email watcher started.")
    while True:
        try:
            process_new_emails()
            print(f"⏳ Waiting for {CHECK_INTERVAL} seconds...\n")
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("🛑 Stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Error occurred: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    start_watching()
