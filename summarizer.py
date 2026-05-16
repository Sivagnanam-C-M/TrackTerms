from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def summarize_text(text):

    text = text[:4000]

    prompt = f"""
    Summarize the following Terms and Conditions
    in a concise and user-friendly way:

    {text}
    """

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,
    )

    summary = (
        response.choices[0]
        .message.content
    )

    return summary