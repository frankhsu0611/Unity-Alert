import React, { useState } from "react";
import { Form, Container, Button } from "react-bootstrap";
import axios from "axios";

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

    // Send subscription request using Axios
    // console.log("eeeeeeeeeeeeeeeeeeeeeeeeeeeee", e);
    axios
      .post("http://localhost:5000/subscribe/", {
        email,
        topic: selectedTopic,
      }, {
        headers: {
          'Content-Type': 'application/json',
          // Any other headers as per your requirement
        }
      })
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          // Subscription successful
          console.log("Subscription successful");
        } else {
          // Handle error
          console.error("Subscription failed");
        }
      })
      .catch((error) => {
        // console.log("Error heree: ", error);
        console.error("Error:", error);
      });
  };

  return (
    <Container fluid>
      <Form onSubmit={handleSubmit}>
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
            aria-label="Default select example"
            onChange={handleTopicChange}
          >
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
