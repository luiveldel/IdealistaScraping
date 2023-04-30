import requests
import creds
import json
from requests.auth import HTTPBasicAuth
import pandas as pd
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=100, ttl=300)  # create a cache with a maximum of 100 entries and a time-to-live (TTL) of 300 seconds (5 minutes)

# Define here the criteria
loc = '37.3653401,-5.9878376' # Seville coordenates
op = 'sale'
ptype = 'homes'
country = 'es'
dist = '5000' #in meters from centre


def get_auth(key, secret, oathurl):
    """
    Gets token from API_KEY provided by idealista https://developers.idealista.com/access-request
    """
    payload = {"grant_type": "client_credentials"}
    r = requests.post(oathurl,
                    auth=HTTPBasicAuth(key, secret),
                    data=payload)
    # If the request fails, we print an error message.
    if r.status_code == 200:
        print(f"API credentials successfully retrieved from {oathurl}")
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


def get_df(data_json):
    return pd.DataFrame.from_dict(data_json['elementList'])

def parse_df(df):
    return df[['price', 'size', 'rooms', 'bathrooms', 'district', 'neighborhood']].astype({"price":int,"size":int})

def get_csv(df):
    return df.to_csv('output/houses.csv', index=False)

def get_excel(df):
    return df.to_excel('output/houses.xlsx', index=False)

def main():
    # Error handling
    try:
        token = json.loads(get_auth(creds.API_KEY, creds.API_SECRET, creds.OATH_URL))
        sess = create_session(token['access_token'])
        resp = sess.post(creds.BASE_URL + "?center={0}&operation={1}&propertyType={2}&country={3}&maxItems=50&distance={4}".format(loc,op,ptype,country,dist))
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
    except Exception as error:
        print(f"Other error occurred: {error}")
        
    search_response = json.loads(resp.text)
    dataframe = get_df(search_response)
    df_final = parse_df(dataframe)
    get_csv(df_final)
    get_excel(df_final)
            
if __name__ == "__main__":
    main()