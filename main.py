# Library imports
import requests
import json
from requests.auth import HTTPBasicAuth
from cachetools import cached, TTLCache
import configparser

# Modules from 'app' package
import app.creds as creds
from app.database import ApiDatabase
from app.houseparser import HouseDataParser

cache = TTLCache(maxsize=100, ttl=300)  # create a cache with a maximum of 100 entries and a time-to-live (TTL) of 300 seconds (5 minutes)

# Reading criteria
oc = '37.3653401,-5.9878376' # Seville coordenates
op = 'sale'
ptype = 'homes'
country = 'es'
dist = '5000' #in meters from centre


def get_auth(key, secret, oathurl):
    """
    Gets token from API_KEY provided by idealista https://developers.idealista.com/access-request
    """
    payload = {"grant_type": "client_credentials"}
    authentication = HTTPBasicAuth(key, secret)
    r = requests.post(oathurl,
                    auth=authentication,
                    data=payload)
    # If the request fails, we print an error message.
    if r.status_code == 200:
        print(f"API credentials successfully retrieved from {oathurl}")
        
        # Initiate a database connection to keep the request in memory
        api_db = ApiDatabase(api_key=authentication,db_path='output/api_data.db')
        api_db.connect()
        data = api_db.make_request(oathurl,r)
        print(data)
        # Close the database connection
        api_db.close()
        return r.text
    else:
        raise Exception(f"API request failed with status code {r.status_code}")

@cached(cache)  # will cache the results of the function
def create_session(token):
    """
    With our token in base64 we can create a session to access the API
    """
    s = requests.Session()
    s.headers.update({
        'Authorization' : 'Bearer ' + token,
        'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8'
    })
    return s 


def main():
    # Error handling
    try:
        token = json.loads(get_auth(creds.API_KEY, creds.API_SECRET, creds.OATH_URL))
        sess = create_session(token['access_token'])
        resp = sess.post(creds.BASE_URL + "?center={0}&operation={1}&propertyType={2}&country={3}&maxItems=50&distance={4}".format(loc,op,ptype,country,dist))
        search_response = json.loads(resp.text)
        house_parser = HouseDataParser(search_response)
        house_parser.parse_data()
        house_parser.to_csv()
        house_parser.to_excel()

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
    except Exception as error:
        print(f"Other error occurred: {error}")

            
if __name__ == "__main__":
    main()