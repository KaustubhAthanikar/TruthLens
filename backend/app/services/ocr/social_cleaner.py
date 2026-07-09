import re


def clean_social_text(text):


    text = re.sub(r"@\w+","",text)
    
    words = text.split()

    if len(words) > 3:

        first = words[0].lower()


        remaining = " ".join(words[1:]).lower()

        if first in remaining:
            words = words[1:]

    text = " ".join(words)

    noise_words = [

        "add comment",
        "like",
        "share",
        "follow",
        "subscribe",
        "views",
        "comments"

    ]


    text = text.lower()


    for word in noise_words:

        text = text.replace(word,"")


    return text.strip()