from flask import Flask, request, jsonify
from collections import defaultdict
from flask_cors import CORS
import requests
import uuid
import argparse


app = Flask(__name__)
CORS(app)

broker_id = None
root_url = ''
topics = {"topic1", "topic2"}
messages = {
    "msg1": {"message_id": "msg1", "topic": "topic1", "content": "Hello World from topic1!", "timestamp": 1650000000},
    "msg2": {"message_id": "msg2", "topic": "topic2", "content": "Another message, from topic2.", "timestamp": 1650000600}
}

recent_propagate_messages = {}
subscribers = {
    "sub1": {"callback_url": "http://127.0.0.1:8000/enqueue", "message_ids": {"msg1", "msg2"}},
    "sub2": {"callback_url": "http://127.0.0.1:8001/enqueue", "message_ids": {"msg2"}}
}

topic_subscribers = defaultdict(set, {
    "topic1": {"sub1"},
    "topic2": {"sub1", "sub2"}
})
broker_endpoints = {}
local_timestamp = 0

@app.route('/create_topic/<topic>', methods=['POST'])
def create_topic(topic):
    if topic in topics:
        return jsonify({'error': 'Topic already exists'}), 400
    topics.add(topic)
    print(f"Topic {topic} has been created.")
    return jsonify({'topic': topic, 'message': 'topic has been created'}), 200

@app.route('/get_topics', methods=['GET'])
def get_topics():
    # return all key in messages
    return jsonify({'topics': list(topics)}), 200

@app.route('/subscribe', methods=['POST'])
def subscribe():
    global local_timestamp
    data = request.get_json()
    if not data:
        return jsonify({'error': 'no json found'}), 400
    local_timestamp = max(local_timestamp, data['timestamp']) + 1
    topic = data['topic']
    if topic not in topics:
        return jsonify({'error': 'Topic does not exist'}), 404
    # create a new subscriber
    topic = data['topic']
    sub_id = data['sub_id']
    # empty string
    if not sub_id:
        # should comese with a sub_id
        return jsonify({'error': 'Subscriber ID is missing'}), 400
    if sub_id not in subscribers:
        subscribers[sub_id] = {'callback_url': data['callback_url'], 'message_ids': set()}
    topic_subscribers[topic].add(sub_id)
    print(f"Subscriber {sub_id} has been subscribed to topic {topic} at timestamp {local_timestamp}.")
    return jsonify({'topic': topic,'broker_url':root_url, 'sub_id': sub_id}), 200

@app.route('/unsubscribe/', methods=['POST'])
def unsubscribe():
    global local_timestamp
    data = request.get_json()
    if not data:
        return jsonify({'error': 'no json found'}), 400
    local_timestamp = max(local_timestamp, data['timestamp']) + 1
    topic = data['topic']
    sub_id = data['sub_id']
    if sub_id not in subscribers:
        return jsonify({'error': 'Subscriber does not exist'}), 404
    if topic not in topic_subscribers:
        return jsonify({'error': 'Topic does not exist'}), 404
    if sub_id not in topic_subscribers[topic]:
        return jsonify({'error': f'Subscriber is not subscribed to topic: {topic}'}), 404
    topic_subscribers[topic].remove(sub_id)
    print(f"Subscriber {sub_id} has been unsubscribed from topic {topic}.")
    return jsonify({'topic': topic, 'sub_id': sub_id}), 200

@app.route('/get_subscribed_topics/<sub_id>', methods=['GET'])
def get_subscribed_topics(sub_id):
    lst = [topic for topic in topic_subscribers if sub_id in topic_subscribers[topic]]
    return jsonify({'subscribed_topics': lst}), 200

@app.route('/publish/<topic>', methods=['POST'])
def publish(topic):
    global local_timestamp
    data = request.get_json()
    message_id = str(uuid.uuid4())
    local_timestamp = max(local_timestamp, data['timestamp']) + 1
    message = {'message_id': message_id, 'topic': topic, 'content': data['content'], 'publisher': request.remote_addr, 
               'created_at': data['timestamp'], 'propagate_from': broker_id, 'to_deliver': len(topic_subscribers[topic])}
    print('number of subscribers:', len(topic_subscribers[topic]))
    
    messages[message_id] = message
    # propagate message to other brokers (before sending to local subs and delete the message)
    propagate_message(topic, message_id)
    # add message to all subscribers
    for sub_id in topic_subscribers[topic]:
        subscribers[sub_id]['message_ids'].add(message_id)
    # send message to local subscribers
    for sub_id in topic_subscribers[topic]:
        send_to_subscriber(sub_id, message_id)
    return jsonify({'topic': topic, 'message_id': message_id}), 200

@app.route('/propagate/<topic>', methods=['POST'])
def propagate(topic):
    global local_timestamp
    data = request.get_json()
    if not data:
        print('no json found')
        return jsonify({'error': 'no json found'}), 400
    local_timestamp = max(local_timestamp, data['timestamp']) + 1
    message = data['message']
    message_id = message['message_id']
    # check if message has been propagated
    if message_id in recent_propagate_messages:
        print('message already been propagated')
        return jsonify({'message': 'message already been propagated'}), 200

    # need to change the to_deliver count to it's local subscribers
    message['to_deliver'] = len(topic_subscribers[topic])
    # save to stoage
    messages[message_id] = message
    # propagate
    propagate_message(topic, message_id, data['avaliable_hops'] - 1)
    # send to local subscribers
    for sub_id in topic_subscribers[topic]:
        subscribers[sub_id]['message_ids'].add(message_id)
    for sub_id in topic_subscribers[topic]:
        send_to_subscriber(sub_id, message_id)
    print(f"Message {message_id} has been propagated at timestamp {local_timestamp}.")
    return jsonify({'topic': topic, 'message_id': message_id}), 200

@app.route('/get_missed_messages/<sub_id>', methods=['GET'])
def get_missed_messages(sub_id):
    # data = request.get_json()
    # sub_id = request.args.get('sub_id')
    # sub_id = data['sub_id']
    if sub_id not in subscribers:
        return jsonify({'error': 'Subscriber does not exist'}), 404
    message_ids_copy = subscribers[sub_id]['message_ids'].copy()

    messages_list = [messages[message_id] for message_id in subscribers[sub_id]['message_ids'] if message_id in messages]

    for message_id in message_ids_copy:
        send_to_subscriber(sub_id, message_id)
    return jsonify({'sub_id': sub_id, 'messages': messages_list}), 200
    
    

# broker functions
def send_to_subscriber(sub_id, message_id):
    if sub_id not in subscribers:
        print(f"Subscriber {sub_id} does not exist.")
        return False
    subscriber = subscribers[sub_id]
    
    if message_id not in subscriber['message_ids']:
        print('message has been sent to subscriber once or should not be sent')
        return False
    
    if message_id not in messages:
        print(f"Message {message_id} does not exist.")
        return False
    
    # send message to subscriber
    subscriber['message_ids'].remove(message_id)
    callback_url = subscriber['callback_url']
    if not callback_url:
        print("Subscriber endpoint is missing.")
        return False
    
    headers = {'Content-Type': 'application/json'}
    payload = {'message':messages[message_id], 'timestamp': local_timestamp}
    try:
        response = requests.post(callback_url, headers=headers, json=payload, timeout = 3)
        if response.status_code != 200:
            print(f"Failed to send message to subscriber {callback_url} with status code {response.status_code}.")
            return False
        else:
            print(f"Message sent to subscriber {callback_url}.")
            messages[message_id]['to_deliver'] -= 1
            print("decrease to_deliver count to", messages[message_id]['to_deliver'])
            if messages[message_id]['to_deliver'] <= 0 and message_id in recent_propagate_messages:
                del messages[message_id]
            return True
    except requests.exceptions.RequestException as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Failed to send message to subscriber {callback_url}. Error: {e}")
    
            
def propagate_message(topic, message_id, avaliable_hops = 10):
    print('CALLEDDDDDDDDD')
    log = {'propagate_from': messages[message_id]['propagate_from'], 'message_id': message_id, 'topic': topic, 'timestamp': local_timestamp}
    recent_propagate_messages[message_id] = log
    for id, endpoint in broker_endpoints.items():
        # stop propagating if no more hops
        if avaliable_hops <= 0:
            print(f"Propagate hops exhausted for message {message_id}.")
            return
        try:
            headers = {'Content-Type': 'application/json'}
            if message_id not in messages:
                print(f"Message {message_id} does not exist2.")
                return
            response = requests.post(f"{endpoint}/propagate/{topic}", headers = headers,
                                     json={'message':messages[message_id], 'timestamp': local_timestamp, 
                                           'avaliable_hops':avaliable_hops})
            if response.status_code != 200:
                print(f"Failed to propagate message to {id} with status code {response.status_code}.")
        except requests.exceptions.Timeout as e:
            print(f"propagate message {message_id} timeout. Timeout error: {e}")
        except Exception as e:
            print(f"Unexpected failure. Failed to propagate message to {id}. Error: {e}")
            
def clean_up():
    # clean recent_propagate_messages once in a while
    # clean outdated messages once in a while 
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app on a specified port.')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the Flask app on.')
    # Parse command-line arguments
    args = parser.parse_args()
    # setup broker_id (port)
    broker_id = args.port
    root_url = f'http://localhost:{args.port}'
                    
    # set up broker_endpoints
    broker_endpoints[5000 + (broker_id % 10 + 1) % 3] = f'http://localhost:{5000 + (broker_id % 10 + 1) % 3}'
    broker_endpoints[5000 + (broker_id % 10 + 2) % 3] = f'http://localhost:{5000 + (broker_id % 10 + 2) % 3}'
    app.run(port=broker_id, debug=False)
