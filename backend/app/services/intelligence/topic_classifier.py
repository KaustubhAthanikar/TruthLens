
TOPICS = {

"health":[
    "covid",
    "coronavirus",
    "virus",
    "vaccine",
    "medicine",
    "disease",
    "cure",
    "doctor",
    "health"
],


"science":[
    "nasa",
    "space",
    "planet",
    "alien",
    "research",
    "discovery"
],


"politics":[
    "government",
    "election",
    "minister",
    "president"
],


"finance":[
    "stock",
    "bank",
    "market",
    "money"
]

}


def classify_topic(text):


    text=text.lower()


    for topic,words in TOPICS.items():

        for word in words:

            if word in text:

                return topic


    return "general"