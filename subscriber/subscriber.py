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
local_timestamp = 0
sub_id = ""
sub_port = ""
callback_url = ""
broker_url = "http://127.0.0.1:5000"  # Change this to the actual base URL of your Flask app
info = {}
txt_filename = ""

@app.route('/c_register', methods=['POST'])
def register():
    global local_timestamp
    global sub_id
    local_timestamp += 1
    data = request.get_json()
    # parse all data and store it into both info and txt_filename
    if not data:
        return jsonify({'error': 'No data received.'}), 400
    if not data['username']:
        return jsonify({'error': 'No username received.'}), 400
    # store the data into info
    for key, value in data.items():
        info[key] = value
    # write to the file
    txt_filename = info['username'] + '.txt'
    with open(txt_filename, 'w') as f:
        f.write(f'key value\n')
        for key, value in info.items():
            f.write(f"{key} {value}\n")
    sub_id = str(uuid.uuid4())
    info['sub_id'] = sub_id
    
    
@app.route('/c_subscribe', methods=['POST'])
def subscribe_to_topic(topic):
    global local_timestamp
    local_timestamp += 1
    url = f"{broker_url}/subscribe"
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {'callback_url': callback_url, 'timestamp': local_timestamp, 'topic': topic, 'sub_id': sub_id}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response
        else:
            print(f"Failed to subscribe. Status code: {response.status_code}, Message: {response.json()['error']}")
            return response
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

@app.route('/c_create_topic', methods=['POST'])
def create_topic(topic):
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

@app.route('/c_publish', methods=['POST'])
def publish_to_topic(topic, content):
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

@app.route('/c_get_topics', methods=['GET'])
def get_topics():
    try:
        response = requests.get(f"{broker_url}/get_topics")
        if response.status_code == 200:
            print(f"Topics: {response.json()['topics']}")
            return response
        else:
            print(f"Failed to get topics. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

@app.route('/c_get_subscribed_topics', methods=['GET'])
def get_subscribed_topic():
    try:
        response = requests.get(f"{broker_url}/get_subscribed_topics/{sub_id}")
        if response.status_code == 200:
            print(f"Subscribed Topics: {response.json()['subscribed_topics']}")
            return response
        else:
            print(f"Failed to get subscribed topics. Status code: {response.status_code}, Message: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

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

@app.route('/c_get_missed', methods=['POST'])
def get_missed():
    global local_timestamp
    data = request.get_json()
    local_timestamp = max(local_timestamp, data['timestamp']) + 1
    try:
        response = requests.get(f"{broker_url}/get_missed_messages/{sub_id}")
        if response.status_code == 200:
            print(f"Missed messages received: {response.json()['message_ids']}")
            return response
        else:
            print(f"Failed to get missed messages. Status code: {response.status_code}, Message: {response.json()['error']}")
            return response
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def set_sub_id(uuid):
    global sub_id
    sub_id = uuid

@app.route('/c_unsubscribe', methods=['POST'])
def unsubscribe(topic):
    global local_timestamp
    local_timestamp += 1
    try:
        response = requests.post(f"{broker_url}/unsubscribe", json={'timestamp': local_timestamp, 'topic': topic, 'sub_id': sub_id})
        if response.status_code == 200:
            print(f"Unsubscribed from topic {response.json()['topic']}.")
            return response
        else:
            print(f"Failed to unsubscribe. Status code: {response.status_code}, Message: {response.json()['error']}")
            return response
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def make_api_calls():  
    # Example usage
    topic1 = "example_topic1"
    topic2 = "example_topic2"

    create_topic(topic1)
    create_topic(topic2)
    # Try subscribing without specifying a subscriber ID (to test ID generation)
    get_topics()
    response = subscribe_to_topic(topic1)

    subscribe_to_topic(topic2)
    get_subscribed_topic()
    unsubscribe(topic2)
    get_subscribed_topic()
    
    publish_to_topic(topic1, "Hello, world!")

def run_flask_app():
    app.run(port = sub_port, debug=False)
    
if __name__ == "__main__":
    # Run Flask app in a separate thread   parser = argparse.ArgumentParser(description='Run the Flask app on a specified port.')
    parser = argparse.ArgumentParser(description='Run the Flask app on a specified port.')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the Flask app on.')
    parser.add_argument('--username', type=str, default='default_user', help='Username to use for the subscriber.')
    # Parse command-line arguments
    args = parser.parse_args()
    sub_port = args.port
    info['username'] = args.username
    if info['username'] == 'default_user':
        # generate a random uuid
        sub_id = str(uuid.uuid4())
        info['sub_id'] = sub_id
    callback_url = f'http://localhost:{sub_port}/enqueue'
    
    #read {username}.txt to get user info
    try:
        with open(f"{info['username']}.txt", 'r') as f:
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
        print("userfile not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # run the flask app
    threading.Thread(target=run_flask_app).start()
    # Make API calls
    make_api_calls()