from flask import Flask, request, jsonify
import requests
import threading
from collections import defaultdict
import uuid
from flask_cors import CORS
import argparse

app = Flask(__name__)
CORS(app)
messages = {}
broker_url = "http://127.0.0.1:5000"
local_timestamp = 0
sub_id = ""
sub_port = ""
callback_url = ""
broker_url = "http://127.0.0.1:5000"  # Change this to the actual base URL of your Flask app
info = defaultdict()

@app.route('/c_register', methods=['POST'])
def register_user():
    global sub_id
    global info
    data = request.get_json()
    username = data.get('username')
    email = data.get('email') 
    sub_id = str(uuid.uuid4())
    # Optionally, store the UUID in your database associated with user details
    info[sub_id] = {"email": email, "username": username}
    return jsonify({'user_uuid': sub_id}), 200

@app.route('/c_subscribe', methods=['POST'])
def subscribe_to_topic():
    global info
    data = request.get_json()
    topic = data['topic']
    sub_id = data['sub_id']
    global local_timestamp
    local_timestamp += 1
    url = f"{broker_url}/subscribe"
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {'callback_url': callback_url, 'timestamp': local_timestamp, 'topic': topic, 'sub_id': sub_id}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data), 200
        else:
            print(f"Failed to subscribe. Status code: {response.status_code}, Message: {response.json()['error']}")
            return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while subscribing to a topic'}), 500

@app.route('/c_create_topic', methods=['POST'])
def create_topic():
    global local_timestamp
    local_timestamp += 1
    data = request.get_json()
    topic = data['topic']
    try:
        response = requests.post(f"{broker_url}/create_topic/{topic}")
        if response.status_code == 200:
            print(f"Topic {response.json()['topic']} created successfully.")
            return response.json(),200
        else:
            print(f"Failed to create topic. Status code: {response.status_code}, Message: {response.json()['error']}")
            return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while creating a new topic'}), 500

@app.route('/c_publish', methods=['POST'])
def publish_to_topic():
    global local_timestamp
    try:
        local_timestamp += 1
        data = request.get_json()
        topic = data['topic']
        content = data['content']
        response = requests.post(f"{broker_url}/publish/{topic}", json={'timestamp': local_timestamp, 'content': content})
        if response.status_code == 200:
            print(f"Message published to topic {response.json()['topic']} with message ID {response.json()['message_id']}.")
            return jsonify(response.json()), 200
        else:
            print(f"Failed to publish message. Status code: {response.status_code}, Message: {response.json()['error']}")
            return jsonify({'error': "Failed to publish message"}), response.status_code
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while publishing message'}), 500

@app.route('/c_get_topics', methods=['GET'])
def get_topics():
    try:
        response = requests.get(f"{broker_url}/get_topics")
        if response.status_code == 200:
            topics = response.json().get('topics', [])
            print(f"Topics: {response.json()['topics']}")
            return jsonify({'topics': topics}), 200
        else:
            print(f"Failed to get topics. Status code: {response.status_code}, Message: {response.json()['error']}")
            return jsonify({'error': 'Failed to get topics'}), response.status_code
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while fetching topics'}), 500

@app.route('/c_get_subscribed_topics', methods=['GET'])
def get_subscribed_topic():
    try:
        data = request.get_json()
        sub_id = data['sub_id']
        response = requests.get(f"{broker_url}/get_subscribed_topics", json={'sub_id': sub_id})
        if response.status_code == 200:
            print(f"Subscribed Topics: {response.json()['subscribed_topics']}")
            return jsonify(response.json()), 200
        else:
            print(f"Failed to get subscribed topics. Status code: {response.status_code}, Message: {response.json()['error']}")
            return jsonify({'error': 'Failed to get subscribed topics'}), response.status_code
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while getting subscribed topics'}), 500

@app.route('/enqueue', methods=['POST'])
def enqueue():
    global local_timestamp
    data = request.get_json()
    local_timestamp = max(local_timestamp, data['timestamp']) + 1
    message = data['message']
    message_id = message['message_id']
    messages[message_id] = message
    print(f"Message {message_id} received. at timestamp {local_timestamp}")
    return jsonify({'message_id': message_id, 'status': 'received'}), 200

@app.route('/c_get_missed', methods=['GET'])
def get_missed():
    global local_timestamp
    timestamp = request.args.get('timestamp', default=0, type=int)
    local_timestamp = max(local_timestamp, timestamp) + 1
    if not sub_id:
        return jsonify({'error': 'sub_id is required',}), 400
    try:
        response = requests.get(f"{broker_url}/get_missed_messages/{sub_id}")
        if response.status_code == 200:
            print(f"Missed messages received: {response.json()['messages']}")
            return jsonify(response.json()), 200
        else:
            print(f"Failed to get missed messages. Status code: {response.status_code}, Message: {response.json()['error']}")
            return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while getting messages'}), 500

def set_sub_id(uuid):
    global sub_id
    sub_id = uuid

@app.route('/c_unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.get_json()
    topic = data['topic']
    sub_id = data['sub_id']
    global local_timestamp
    local_timestamp += 1
    try:
        response = requests.post(f"{broker_url}/unsubscribe", json={'timestamp': local_timestamp, 'topic': topic, 'sub_id': sub_id})
        if response.status_code == 200:
            print(f"Unsubscribed from topic {response.json()['topic']}.")
            return jsonify(response.json()), 200
        else:
            print(f"Failed to unsubscribe. Status code: {response.status_code}, Message: {response.json()['error']}")
            return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while unsubscribing'}), 500

# def make_api_calls():  
#     # Example usage
#     broker_url = "http://127.0.0.1:5000"  # Change this to the actual base URL of your Flask app
#     topic1 = "example_topic3"
#     topic2 = "example_topic2"

#     create_topic(topic1)
#     create_topic(topic2)
#     # Try subscribing without specifying a subscriber ID (to test ID generation)
#     get_topics()
#     response = subscribe_to_topic(topic1)

#     subscribe_to_topic(topic2)
#     get_subscribed_topic()
    
#     publish_to_topic(topic1, "Hello, world!")

def run_flask_app():
    app.run(port = sub_port, debug=False)
    
if __name__ == "__main__":
    # Run Flask app in a separate thread   parser = argparse.ArgumentParser(description='Run the Flask app on a specified port.')
    parser = argparse.ArgumentParser(description='Run the Flask app on a specified port.')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the Flask app on.')
    # Parse command-line arguments
    args = parser.parse_args()
    # setup broker_id (port)
    sub_port = args.port
    callback_url = f'http://localhost:{sub_port}/enqueue'
    
    # init sub_id
    sub_id = str(uuid.uuid4())
    
    #read info.txt to get user info
    try:
        with open('info.txt', 'r') as f:
            lines = f.readlines()
            # skip the first line
            for line in lines[1:]:
                line = line.strip()
                if line:
                    key, value = line.split()
                    # replace the sub_id if specified
                    if key == 'sub_id':    
                        sub_id = value
    except FileNotFoundError:
        print("info.txt not found. Using auto-generated sub_id.")
    
    # run the flask app
    threading.Thread(target=run_flask_app).start()
    # app.run(port = 8000, debug=True)
    # Make API calls
    # make_api_calls()