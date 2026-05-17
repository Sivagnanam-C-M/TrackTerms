import re

def clean_text(text):

    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_sentences(text):

    return re.split(
        r'(?<=[.!?]) +',
        text
    )

def detect_changes(old_text, new_text):

    old_text = clean_text(old_text)
    new_text = clean_text(new_text)
    old_sentences = split_sentences(old_text)
    new_sentences = split_sentences(new_text)
    changes = []

    for sentence in old_sentences:
        if sentence not in new_sentences:
            changes.append({
                "type": "removed",
                "text": sentence
            })

    for sentence in new_sentences:
        if sentence not in old_sentences:
            changes.append({
                "type": "added",
                "text": sentence
            })
            
    return changes