from datetime import datetime

def calculate_freshness(date):
    if not date:
        return 0.5
    
    age = (datetime.now()-date).days    

    if age <= 7:

        return 1.0


    elif age <= 30:

        return 0.8


    elif age <= 365:

        return 0.6


    else:

        return 0.3