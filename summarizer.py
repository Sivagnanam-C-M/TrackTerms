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

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code != 200:
            continue

        try:

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

            print("JSON ERROR:", e)

    final_summary = " ".join(summaries)

    if final_summary.strip() == "":
        return "Summary could not be generated."

    return final_summary