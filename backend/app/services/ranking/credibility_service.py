from urllib.parse import urlparse


TRUSTED_SOURCES = {

    "reuters.com":0.95,

    "apnews.com":0.95,

    "bbc.com":0.90,

    "who.int":0.95,

    "nature.com":0.95,

    "factcheck.org":0.90,

    "politifact.com":0.90,

    "nasa.gov":0.95
}



def calculate_credibility(source):


    if not source:
        return 0.5



    parsed = urlparse(source)


    if parsed.netloc:

        domain = parsed.netloc.lower()


    else:

        domain = source.lower()



    domain = domain.replace(
        "www.",
        ""
    )


    if domain.endswith(".gov"):

        return 0.95


    if domain.endswith(".edu"):

        return 0.90



    for site, score in TRUSTED_SOURCES.items():


        if site in domain:

            return score



    return 0.5