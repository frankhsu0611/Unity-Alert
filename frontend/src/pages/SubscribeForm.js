import React, { useState } from "react";
import { Form, Container, Button } from "react-bootstrap";

const SubscribeForm = () => {
  const [email, setEmail] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("");

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleTopicChange = (e) => {
    setSelectedTopic(e.target.value);
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission to backend
    fetch("/subscribe/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        topic: selectedTopic,
      }),
    })
      .then((response) => {
        if (response.ok) {
          // Subscription successful
          console.log("Subscription successful");
        } else {
          // Handle error
          console.error("Subscription failed");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <Container fluid>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Select aria-label="Default select example">
            <option>Select the topic</option>
            <option value="1">Topic1</option>
            <option value="2">Topic2</option>
            <option value="3">Topic3</option>
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
