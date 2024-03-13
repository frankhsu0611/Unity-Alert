import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, ListGroup, Card } from "react-bootstrap";
import backgroundImage from "../wallpaper.png";

const MessageFeed = () => {
  const [messages, setMessages] = useState([]);
//   const sub_id = "sub1"; // This should ideally come from a user's session or authentication context

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/c_get_missed`, {
          params: { timestamp: Date.now() },
        });
        if (response.data && response.data.messages) {
          // Create a map of existing message IDs for quick lookup
          const existingMessageIds = new Set(messages.map((msg) => msg.id)); // Assuming each message has a unique 'id'

          // Filter out any messages that are already in the state
          const newMessages = response.data.messages.filter(
            (msg) => !existingMessageIds.has(msg.id)
          );

          // Append new messages to the existing messages state
          setMessages((prevMessages) => [...prevMessages, ...newMessages]);
        } else {
          console.error("Unexpected response structure:", response.data);
        }
      } catch (error) {
        console.error("Failed to fetch messages:", error);
      }
    };

    fetchMessages(); // Fetch messages on component mount
    const intervalId = setInterval(fetchMessages, 20000); // Poll for new messages every 10 seconds

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  return (
    <Container
      fluid
      className="vh-100 d-flex justify-content-center align-items-center"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
      }}
    >
      <Card
        bg="dark"
        text="white"
        className="w-100"
        style={{ maxWidth: "50%", padding: "20px", borderRadius: "15px" }}
      >
        <Card.Header>Message Feed</Card.Header>
        <Card.Body>
          <ListGroup>
            {messages.map((message, index) => (
              <ListGroup.Item key={index}>
                <Card>
                  <Card.Body>
                    <Card.Title>{message.topic}</Card.Title>
                    <Card.Text>{message.content}</Card.Text>
                    <Card.Footer className="text-muted">
                      Sent at {new Date(message.timestamp).toLocaleString()}
                    </Card.Footer>
                  </Card.Body>
                </Card>
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default MessageFeed;
