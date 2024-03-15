UnityAlert Backend
Welcome to the UnityAlert Backend repository! The backend of UnityAlert is the core engine driving our community alert system, handling subscriptions, alert dissemination, and the implementation of the gossip protocol for efficient, scalable communication.

Features
Publish-Subscribe Mechanism: Manages subscriptions and facilitates the distribution of alerts to subscribed users.
Gossip Protocol: Ensures reliable and scalable propagation of alerts across the network.
Lamport Timestamps: Provides a mechanism for ordering events in the distributed system.
Data Replication: Enhances system reliability through data redundancy.
Getting Started
Follow these instructions to get a copy of the UnityAlert backend running on your local machine.

Prerequisites
Python 3.x
Flask
Requests library

Installation
Clone the repository:
Navigate to the broker directory:
cd broker
Install dependencies:
pip install
Start the Flask server:
python broker.py
The backend server should now be running on http://localhost:5000.



Installation
Clone the repository:
Navigate to the subscriber directory:
cd subscriber
Install dependencies:
pip install
Start the Flask server:
python subscriber.py
The backend server should now be running on http://localhost:8000.
