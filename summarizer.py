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
You are an AI assistant that explains Terms and Conditions
in SIMPLE everyday language.

Your task:
- Rewrite complex legal language into simple English
- Convert passive/legal tone into active human-friendly tone
- Explain what the company actually means
- Make the summary easy for normal users to understand
- Avoid copying original legal sentences
- Keep it concise and attractive

Format:

## Quick Summary
- short bullet point
- short bullet point
- short bullet point

## Important Note
- mention major privacy, payment, or security concern

IMPORTANT:
Do NOT use difficult legal wording.
Do NOT sound robotic.
Do NOT copy the original sentences directly.

Terms and Conditions:
{text}
"""

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You simplify legal documents into "
                        "clear, modern, human-friendly English."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.5,
            max_tokens=400
        )

        summary = response.choices[0].message.content

        return summary.strip()

    except Exception as e:

        print("Summarization Error:", str(e))

        return "Unable to generate summary."