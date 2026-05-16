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
        You are a Terms and Conditions simplifier.

        Your job is to COMPLETELY REWRITE legal text into
        simple modern English.

        STRICT RULES:
        - ONLY return bullet points
        - DO NOT add explanations
        - DO NOT add extra paragraphs
        - DO NOT say "Let's break this down"
        - DO NOT repeat headings from the document
        - DO NOT copy legal wording
        - Rewrite everything naturally
        - Convert passive/legal voice into active human voice
        - Sound like you are explaining to a normal app user
        - Keep it short and clean
        - Maximum 120 words

        OUTPUT FORMAT:

        ## Quick Summary
        • point
        • point
        • point

        ## Important Note
        • one important warning or privacy concern

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

            temperature=0.2,
            max_tokens=400
        )

        summary = response.choices[0].message.content

        return summary.strip()

    except Exception as e:

        print("Summarization Error:", str(e))

        return "Unable to generate summary."