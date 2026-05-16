import requests
import os

API_URL = "https://router.huggingface.co/hf-inference/models/sshleifer/distilbart-cnn-12-6"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}


def split_text(text, chunk_size=500):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


def summarize_text(text):

    if not text.strip():

        return "No text found in PDF."

    chunks = split_text(text)

    summaries = []

    for chunk in chunks:

        payload = {

            "inputs": chunk,

            "parameters": {

                "max_length": 120,

                "min_length": 30,

                "do_sample": False
            }
        }

        try:

            response = requests.post(

                API_URL,

                headers=HEADERS,

                json=payload,

                timeout=60
            )

            print("STATUS:", response.status_code)
            print("TEXT:", response.text)

            if response.status_code != 200:

                continue

            result = response.json()

            if (
                isinstance(result, list)
                and len(result) > 0
                and "summary_text" in result[0]
            ):

                summaries.append(
                    result[0]["summary_text"]
                )

        except Exception as e:

            print("ERROR:", e)

    final_summary = " ".join(summaries)

    if final_summary.strip() == "":

        return "Summary could not be generated."

    return final_summary