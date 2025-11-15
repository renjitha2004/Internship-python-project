from pdf2image import convert_from_path
from gradio_client import Client, handle_file
from project import get_emails_with_pdfs
import os
from pdf2image import convert_from_bytes

import io
from PIL import Image
import tempfile



client = Client("prithivMLmods/Multimodal-OCR")

def run_ocr_from_image(pil_image):
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            pil_image.save(tmp.name, format="PNG")
            temp_path = tmp.name

        result = client.predict(
            model_name="Nanonets-OCR-s",
            text="Extract the text from this image",
            image=handle_file(temp_path),
            max_new_tokens=1024,
            temperature=0.6,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.2,
            api_name="/generate_image"
        )
        print("✅ OCR Output:", result[:200])  # Print first 200 chars
        return result

    except Exception as e:
        print(f"❌ OCR Failed:", e)
        return ""

# ✅ Step 3: Process PDF and run OCR page by page
def run_ocr_on_pdf(pdf_data, pdf_name="output"):
    pdf_buffer = io.BytesIO(pdf_data)
    pages = convert_from_bytes(pdf_buffer.read(), poppler_path=r"C:\Users\renji\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin")

    combined_text = ""
    print(f"📄 Total pages extracted: {len(pages)}")

    for i, page in enumerate(pages, 1):
        print(f"🔍 Running OCR on page {i}")
        try:
            result = run_ocr_from_image(page)
            if result:
                combined_text += f"\n--- PAGE {i} ---\n{result}\n"
        except Exception as e:
            print(f"❌ Failed on page {i}: {e}")

    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", f"{pdf_name}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(combined_text)

    print(f"🧠 Combined text length: {len(combined_text)}")
    print("🔍 Full path:", os.path.abspath(output_path))
    print(f"✅ OCR output saved to: {output_path}")

# ✅ MAIN EXECUTION
if __name__ == "__main__":
    attachments = get_emails_with_pdfs()
    print(f"\n📬 Total PDFs found: {len(attachments)}")

    if attachments:
        filename, pdf_data = attachments[0]  # Process the first attachment
        run_ocr_on_pdf(pdf_data, pdf_name=filename.replace(".pdf", ""))
    else:
        print("❌ No PDF attachments found.")