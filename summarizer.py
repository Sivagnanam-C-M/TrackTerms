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
        Simplify these Terms and Conditions into clean,
        modern, human-friendly points.

        Rules:
        - Do NOT use headings
        - Do NOT use hashtags
        - Do NOT use markdown
        - Do NOT use "we", "our", or "us"
        - Do NOT sound legal or robotic
        - Rewrite everything naturally
        - Use short bullet points only
        - Keep it concise
        - Maximum 100 words
        - Mention important privacy or payment concerns if present

        Good example:
        • WhatsApp may share some user data with Meta products.
        • Businesses can contact users through the platform.
        • Accounts may be suspended for policy violations.

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