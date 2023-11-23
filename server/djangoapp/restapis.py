import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        dealers = json_result
        for dealer_doc in dealers:
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e06a879c-aa34-4009-9818-82f5d6299f79'
    api_key = 'K61HuXiosknlPuzdmJD_c2dYk-QvLJwVTMMMmH1uIoVq'
    sentiment = requests.get(url, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key), params={'text': text})
    return sentiment
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealer_id=dealer_id)
    if json_result:
        for review in json_result:
            review_text = review['review']
            sentiment = analyze_review_sentiments(review_text)
            print(sentiment.__dict__)
            review_obj = DealerReview(dealership=review['dealership'], name=review['name'], purchase=review['purchase'], review=review_text,
                                      purchase_date=review['purchase_date'], car_make=review['car_make'], car_model=review['car_model'],
                                      car_year=review['car_year'], sentiment=sentiment, id=review['id'])
            results.append(review_obj)
    return results
