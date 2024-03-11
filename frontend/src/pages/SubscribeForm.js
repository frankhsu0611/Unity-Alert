import React, { useState, useEffect } from "react";
import { Form, Container, Button, Alert } from "react-bootstrap";
import axios from "axios";

const SubscribeForm = (props) => {
  const [email, setEmail] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("");
  const [message, setMessage] = useState("");
  const topics = props.topics;

  const handleEmailChange = (e) => {
    setMessage("");
    setEmail(e.target.value);
  };

  const handleTopicChange = (e) => {
    setMessage("");
    setSelectedTopic(e.target.value);
  };
  const handleSubmit = (e) => {
    setMessage("");
    e.preventDefault();

    // Send subscription request using Axios
    axios
      .post("http://127.0.0.1:5000/subscribe", {
<<<<<<< HEAD
        email: email,
        topic: selectedTopic,
        timestamp: Date.now()
=======
        email,
        topic: selectedTopic,
        timestamp: 0,
      }, {
        headers: {
          'Content-Type': 'application/json',
          // Any other headers as per your requirement
        }
>>>>>>> bf58639 (current)
      })
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          // Subscription successful
          console.log("Subscription successful");
          setMessage({
            text: `Subscribed to ${selectedTopic} successfully.`,
            variant: "success"
          });
          setEmail("");
        setSelectedTopic("");
        } else {
          // Handle error
          console.error("Subscription failed");
          setMessage({
            text: `Failed to subscribe to topic. Please try again.`,
            variant: "danger"
          });
        }
      })
      .catch((error) => {
        // console.log("Error heree: ", error);
        setMessage({
            text: `${error.response.data.error}, Please try again.`,
            variant: "danger"
          });
        console.error("Error:", error);
      });
  };

  const handleFormClick = () => {
    // Clear the alert message when the form is clicked
    setMessage("");
  };

  return (
    <Container fluid>
        {message && <Alert variant={message.variant}>{message.text}</Alert>}
      <Form onSubmit={handleSubmit} onClick={handleFormClick}>
        <Form.Group className="mb-3">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            onChange={handleEmailChange}
          />
        </Form.Group>
        <Form.Group className="mb-3">
        <Form.Select
            aria-label="Select topic"
            onChange={handleTopicChange}
            value={selectedTopic}
          >
            <option>Select the topic</option>
            {topics.map(topic => (
              <option key={topic} value={topic}>{topic}</option>
            ))}
          </Form.Select>
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </Container>
  );
};

export default SubscribeForm;
