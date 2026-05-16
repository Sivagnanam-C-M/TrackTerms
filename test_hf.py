from summarizer import summarize_text

text = """
TrackTerms collects user data including email,
device information, and uploaded documents.
We may share information with third-party
analytics providers to improve services.
Users must accept updated terms regularly.
"""

summary = summarize_text(text)

print("\nSUMMARY:\n")
print(summary)