import requests,json



def get_quotes():
    """
    Function that gets the json response to our url request
    """
    quotes = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    

    return  quotes