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
        Analyze these Terms and Conditions and generate a clean,
        premium-style executive summary.

        STRICT RULES:
        - Never use "we", "our", or "us"
        - Never speak as the company
        - Rewrite legal wording into modern human language
        - Keep sections concise
        - Avoid repeating the document
        - Focus only on important user-impacting details
        - Do not exceed 180 words total
        - Sound like a professional policy analyst

        Use this EXACT format:

        📱 Terms & Conditions Breakdown

        💡 Quick Take:
        [1-2 sentence overview]

        🔏 Privacy & Data Usage
        • [important point]
        • [important point]

        🛑 Account Risks
        • [important point]
        • [important point]

        ⚠️ Important Note
        • [biggest concern or warning]

        Terms and Conditions Text:
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