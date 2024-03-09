from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import requests
import threading
from collections import defaultdict

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
messages = {}
local_timestamp = 0
sub_id_at_broker = defaultdict(str) # key is broker_url

def subscribe_to_topic(broker_url, topic, callback_url):
    global local_timestamp
    local_timestamp += 1
    # Construct the URL based on whether a sub_id is provided
    url = f"{broker_url}/subscribe"
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {'callback_url': callback_url, 'timestamp': local_timestamp, 'topic': topic, 'sub_id': sub_id_at_broker[broker_url]}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Subscription successful.")
            data = response.json()
            print(data)
            sub_id_at_broker[data['broker_url']] = data['sub_id']
            return response
        else:
            print(f"Failed to subscribe. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def create_topic(broker_url, topic):
    global local_timestamp
    local_timestamp += 1
    try:
        response = requests.post(f"{broker_url}/create_topic/{topic}")
        if response.status_code == 200:
            print(f"Topic {response.json()['topic']} created successfully.")
            return response
        else:
            print(f"Failed to create topic. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def publish_to_topic(broker_url, topic, content):
    global local_timestamp
    try:
        local_timestamp += 1
        response = requests.post(f"{broker_url}/publish/{topic}", json={'timestamp': local_timestamp, 'content': content})
        if response.status_code == 200:
            print(f"Message published to topic {response.json()['topic']} with message ID {response.json()['message_id']}.")
            return response
        else:
            print(f"Failed to publish message. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def get_topics(broker_url):
    try:
        response = requests.get(f"{broker_url}/get_topics")
        if response.status_code == 200:
            print(f"Topics: {response.json()['topics']}")
            return response
        else:
            print(f"Failed to get topics. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        
def get_subscribed_topic(broker_url):
    try:
        response = requests.get(f"{broker_url}/get_subscribed_topics/{sub_id_at_broker[broker_url]}")
        if response.status_code == 200:
            print(f"Subscribed Topics: {response.json()['subscribed_topics']}")
            return response
        else:
            print(f"Failed to get subscribed topics. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

@app.route('/enqueue', methods=['POST'])
@cross_origin()
def enqueue():
    global local_timestamp
    data = request.get_json()
    local_timestamp = max(local_timestamp, data['timestamp']) + 1
    message = data['message']
    message_id = message['message_id']
    messages[message_id] = message
    print(f"Message {message_id} received. at timestamp {local_timestamp}")
    return jsonify({'message_id': message_id, 'status': 'received'}), 200
    

def make_api_calls():  
    # Example usage
    broker_url = "http://127.0.0.1:5000"  # Change this to the actual base URL of your Flask app
    callback_url = "http://127.0.0.1:8000/enqueue"
    topic1 = "example_topic1"
    topic2 = "example_topic2"

    create_topic(broker_url, topic1)
    create_topic(broker_url, topic2)
    # Try subscribing without specifying a subscriber ID (to test ID generation)
    get_topics(broker_url)
    response = subscribe_to_topic(broker_url, topic1, callback_url)

    subscribe_to_topic(broker_url, topic2, callback_url)
    get_subscribed_topic(broker_url)
    
    publish_to_topic(broker_url, topic1, "Hello, world!")

def run_flask_app():
    app.run(port = 8000, debug=False)
    
if __name__ == "__main__":
    # Run Flask app in a separate thread
    threading.Thread(target=run_flask_app).start()
    # Make API calls
    make_api_calls()