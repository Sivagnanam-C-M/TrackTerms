import os
import time
import requests

API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-base"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def split_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def summarize_text(text):
    chunks = split_text(text)
    summaries = []
    
    for idx, chunk in enumerate(chunks):
        payload = {
            "inputs": f"Summarize this terms and conditions document:\n\n{chunk}",
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.3
            }
        }
        
        while True:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            print(f"Chunk {idx+1}/{len(chunks)} - STATUS:", response.status_code)
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                        summaries.append(result[0]["generated_text"])
                    break
                except Exception as e:
                    print("JSON ERROR:", e)
                    break
            elif response.status_code == 503:
                print("Model loading... Retrying in 5s.")
                time.sleep(5)
                continue
            else:
                print("API ERROR:", response.text)
                break

    final_summary = "\n\n".join(summaries)
    return final_summary if final_summary.strip() else "Summary could not be generated."