import os
import time
import requests
from pypdf import PdfReader

API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"RENDER LOG: PDF Extraction Error: {e}")
        return ""

def split_text(text, chunk_size=250):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def summarize_text(text):
    if not os.getenv('HF_TOKEN'):
        print("RENDER LOG: HF_TOKEN is missing!")
        return "Error: HF_TOKEN environment variable is not configured in Render."

    chunks = split_text(text)
    summaries = []
    
    for idx, chunk in enumerate(chunks):
        payload = {
            "inputs": f"Summarize this text:\n\n{chunk}",
            "options": {
                "wait_for_model": True
            }
        }
        
        retries = 0
        while retries < 3:
            try:
                print(f"RENDER LOG: Sending chunk {idx+1}/{len(chunks)}")
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=25)
                print(f"RENDER LOG: Chunk {idx+1} response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                        summaries.append(result[0]["generated_text"])
                    else:
                        print(f"RENDER LOG: Unexpected JSON response structure: {result}")
                    break
                elif response.status_code == 503:
                    print("RENDER LOG: Model loading (503). Retrying in 5 seconds...")
                    retries += 1
                    time.sleep(5)
                    continue
                else:
                    print(f"RENDER LOG: API error response: {response.text}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"RENDER LOG: Request failed due to network error: {e}")
                break
        else:
            continue

    final_summary = "\n\n".join(summaries)
    return final_summary if final_summary.strip() else "Summary could not be generated."

def summarize_pdf(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text.strip():
        return "Could not read or extract text from the PDF file."
    return summarize_text(raw_text)