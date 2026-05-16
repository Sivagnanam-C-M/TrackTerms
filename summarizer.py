import requests
import os

API_URL = (
    "https://api-inference.huggingface.co/models/"
    "sshleifer/distilbart-cnn-12-6"
)

HEADERS = { "Authorization": f"Bearer {os.getenv('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')}" }

def split_text(text, chunk_size=800):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


def summarize_text(text):

    chunks = split_text(text)

    summaries = []

    for chunk in chunks:

        payload = {
            "inputs": chunk
        }

        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload
        )

        result = response.json()

        if (
            isinstance(result, list)
            and len(result) > 0
            and "summary_text" in result[0]
        ):

            summaries.append(
                result[0]["summary_text"]
            )

    final_summary = " ".join(
        summaries
    )

    return final_summary