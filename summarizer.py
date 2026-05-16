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
        Summarize these Terms and Conditions into ONLY 4-6 short points.

        STRICT RULES:
        - Never use "we", "our", or "us"
        - Never speak as the company
        - Never copy original sentences
        - Rewrite everything naturally
        - Keep every point very short
        - No explanations
        - No headings
        - No markdown
        - No extra text
        - Maximum 80 words total

        Example style:
        • User data may be shared with Meta products.
        • Accounts can be suspended for policy violations.
        • Some data may be stored globally.

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