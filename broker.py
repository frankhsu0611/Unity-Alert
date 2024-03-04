from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime
import requests
import uuid
app = Flask(__name__)

topics = set()
messages = defaultdict(dict)
subscribers = defaultdict(dict)
topic_subscribers = defaultdict(set())

@app.route('/create_topic', methods=['POST'])
def create_topic(topic):
    if topic in topics:
        return jsonify({'error': 'Topic already exists'})
    return jsonify({'topic': topic})

@app.route('/get_topics/<topic>', methods=['GET'])
def get_topics():
    # return all key in messages
    return jsonify({'topics': list(topics)})

@app.route('/subscribe/<topic>/', defaults={'sub_id': None})
@app.route('/subscribe/<topic>'/'<sub_id>', methods=['POST'])
def subscribe(topic, sub_id):
    if topic not in topics:
        return jsonify({'error': 'Topic does not exist'})
    # create a new subscriber
    if not sub_id:
        sub_id = str(uuid.uuid4())
        subcriber = {'ip': request.remote_addr, 'message_ids': set()}
        subscribers[sub_id] = subcriber
    elif sub_id not in subscribers:
        return jsonify({'error': 'Subscriber does not exist'})
    topic_subscribers[topic].add(sub_id)
    return jsonify({'topic': topic, 'subscriber_id': sub_id})
        

@app.route('/publish/<topic>', methods=['POST'])
def publish_message(topic):
    req = request.get_json()
    message = {'topic': topic, 'content': req['content'], 'publisher': request.remote_addr, 
               'created_at': datetime.now(), 'to_deliver': len(topic_subscribers[topic])}
    message_id = str(uuid.uuid4())
    messages[message_id] = message
    # add message to all subscribers
    for sub_id in topic_subscribers[topic]:
        subscribers[sub_id]['message_ids'].add(message['id'])
    # send message to local subscribers
    for sub_id in topic_subscribers[topic]:
        send_to_subscriber(sub_id, message_id)
    # propagate message to other brokers
    propagate_message(topic, message)
    
    
    pass

# broker functions
def send_to_subscriber(sub_id, message_id):
    subscriber = subscribers[sub_id]
    if message_id not in subscriber['message_ids']:
        print('message has been sent to subscriber or should not be sent')
        return False
    
    # send message to subscriber
    subscriber['message_ids'].remove(message_id)
    ip = subscriber['ip']
    if not ip:
        print("Subscriber endpoint is missing.")
        return False
    
    headers = {'Content-Type': 'application/json'}
    payload = messages[message_id]
    try:
        response = requests.post(ip, headers=headers, data=payload, timeout = 3)
        if response.status_code != 200:
            print(f"Failed to send message to subscriber {ip}.")
        else:
            print(f"Message sent to subscriber {ip}.")
            messages[message_id]['to_deliver'] -= 1
            if messages[message_id]['to_deliver'] <= 0:
                del messages[message_id]
            return True
    except requests.exceptions.RequestException as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Failed to send message to subscriber {ip}. Error: {e}")
    
            

def propagate_message(topic, message):
    pass


if __name__ == '__main__':
    app.run(port=5000)
