from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def summarize_text(text):

    try:

        if not text or len(text.strip()) == 0:
            return "No content available for summarization."

        text = text[:4000]

        prompt = f"""
You are an AI Terms & Conditions summarizer.

Generate a concise, attractive, and easy-to-read summary.

Rules:
- Use short bullet points
- Keep the summary user-friendly
- Avoid long paragraphs
- Highlight important privacy, payment, subscription,
  account, or security concerns
- Mention risks if any
- Keep the output under 150 words

Format:

## Quick Summary
- point
- point
- point

## Important Note
short warning or concern if applicable

Terms and Conditions:
{text}
"""

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional legal document "
                        "and Terms & Conditions summarizer."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,
            max_tokens=400
        )

        summary = response.choices[0].message.content

        return summary.strip()

    except Exception as e:

        print("Summarization Error:", str(e))

        return (
            "Unable to generate summary at the moment."
        )