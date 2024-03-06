from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime
import requests
import uuid
import argparse


app = Flask(__name__)

broker_id = None
topics = set()
messages = {}
recent_propagate_messages = {}
subscribers = {}
topic_subscribers = defaultdict(set)
broker_endpoints = {}


@app.route('/create_topic/<topic>', methods=['POST'])
def create_topic(topic):
    if topic in topics:
        return jsonify({'error': 'Topic already exists'}), 400
    topics.add(topic)
    print(f"Topic {topic} has been created.")
    return jsonify({'topic': topic, 'message': 'topic has been created'}), 200

@app.route('/get_topics/<topic>', methods=['GET'])
def get_topics():
    # return all key in messages
    return jsonify({'topics': list(topics)}), 200

@app.route('/subscribe/<topic>', defaults={'sub_id': None}, methods=['POST'])
@app.route('/subscribe/<topic>/<sub_id>', methods=['POST'])
def subscribe(topic, sub_id):
    if topic not in topics:
        return jsonify({'error': 'Topic does not exist'}), 404
    # create a new subscriber
    if not sub_id:
        sub_id = str(uuid.uuid4())
        subcriber = {'callback_url': request.get_json().get('callback_url'), 'message_ids': set()}
        subscribers[sub_id] = subcriber
        print(f"Subscriber {sub_id} has been created.")
    elif sub_id not in subscribers:
        return jsonify({'error': 'Subscriber does not exist'}), 404
    topic_subscribers[topic].add(sub_id)
    print(f"Subscriber {sub_id} has been subscribed to topic {topic}.")
    return jsonify({'topic': topic, 'subscriber_id': sub_id}), 200
        

@app.route('/publish/<topic>', methods=['POST'])
def publish(topic):
    data = request.get_json()
    message_id = str(uuid.uuid4())
    print('content:', data['content'])
    message = {'message_id': message_id, 'topic': topic, 'content': data['content'], 'publisher': request.remote_addr, 
               'created_at': datetime.now().isoformat(), 'propagate_from': broker_id, 'to_deliver': len(topic_subscribers[topic])}
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
    data = request.get_json()
    if not data:
        print('no json found')
        return jsonify({'error': 'no json found'}), 400
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
    return jsonify({'topic': topic, 'message_id': message_id}), 200

    

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
    payload = messages[message_id]
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
    log = {'propagate_from': messages[message_id]['propagate_from'], 'message_id': message_id, 'topic': topic, 'timestamp': datetime.now()}
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
                                     json={'message':messages[message_id], 'avaliable_hops':avaliable_hops})
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
    
    # set up broker_endpoints
    broker_endpoints[5000 + (broker_id % 10 + 1) % 3] = f'http://localhost:{5000 + (broker_id % 10 + 1) % 3}'
    broker_endpoints[5000 + (broker_id % 10 + 2) % 3] = f'http://localhost:{5000 + (broker_id % 10 + 2) % 3}'
    app.run(port=broker_id, debug=True)
