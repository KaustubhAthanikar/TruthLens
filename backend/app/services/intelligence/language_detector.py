from langdetect import detect


def detect_language(text: str):

    try:
        language = detect(text)

        return language

    except:

        return "unknown"