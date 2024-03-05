from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def subscribe_to_topic(base_url, topic, sub_id=None):
    # Construct the URL based on whether a sub_id is provided
    if sub_id:
        url = f"{base_url}/subscribe/{topic}/{sub_id}"
    else:
        url = f"{base_url}/subscribe/{topic}/"
    
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print("Subscription successful.")
            data = response.json()
            print(data)
            return response
        else:
            print(f"Failed to subscribe. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def create_topic(base_url, topic):
    try:
        response = requests.post(f"{base_url}/create_topic/{topic}")
        if response.status_code == 200:
            print(f"Topic {response.json()['topic']} created successfully.")
            return response
        else:
            print(f"Failed to create topic. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        
        
        

# Example usage
base_url = "http://127.0.0.1:5000"  # Change this to the actual base URL of your Flask app
topic1 = "example_topic1"
topic2 = "example_topic2"

create_topic(base_url, topic1)
create_topic(base_url, topic2)
# Try subscribing without specifying a subscriber ID (to test ID generation)
response = subscribe_to_topic(base_url, topic1)

# Try subscribing with a specific subscriber ID
if response.status_code != 200:
    print("Failed to subscribe.")
else:
    subscribe_to_topic(base_url, topic2, response.json()['subscriber_id'])