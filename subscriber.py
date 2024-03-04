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
            print(f"Topic: {data['topic']}, Subscriber ID: {data['subscriber_id']}")
        else:
            print(f"Failed to subscribe. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
base_url = "http://127.0.0.1:5000"  # Change this to the actual base URL of your Flask app
topic = "example_topic"

# Try subscribing without specifying a subscriber ID (to test ID generation)
subscribe_to_topic(base_url, topic)

# Try subscribing with a specific subscriber ID
subscribe_to_topic(base_url, topic, "specific_sub_id")