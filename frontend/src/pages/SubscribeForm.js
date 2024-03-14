import React, { useState, useEffect } from "react";
import { Form, Container, Button, Alert, Card, Spinner } from "react-bootstrap";
import axios from "axios";
import backgroundImage from "../wallpaper.png";
import NavBar from "./NavBar";
import { baseURL } from "../config";

const SubscribeForm = () => {
  const [selectedTopic, setSelectedTopic] = useState("");
  const [message, setMessage] = useState("");
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch topics list from backend API
    axios
      .get(`${baseURL}/c_get_topics`)
      .then((response) => {
        if (response && response.data && "topics" in response.data) {
          setTopics(response.data["topics"]);
        } else {
          // Handle the case where 'data' or 'topics' doesn't exist in the response
          console.error("Invalid response structure:", response);
        }
      })
      .catch((error) => {
        console.error("Error fetching topics:", error);
      });
  }, []);

  const handleTopicChange = (e) => {
    setMessage("");
    setSelectedTopic(e.target.value);
  };
  const handleSubmit = (e) => {
    setLoading(true);
    setMessage("");
    e.preventDefault();
    // Send subscription request using Axios
    axios
      .post(`${baseURL}/c_subscribe`, {
        topic: selectedTopic,
        timestamp: Date.now(),
      })
      .then((response) => {
        setLoading(false);
        console.log(response);
        if (response.status === 200) {
          // Subscription successful
          console.log("Subscription successful");
          setMessage({
            text: `Subscribed to ${selectedTopic} successfully.`,
            variant: "success",
          });
          setSelectedTopic("");
        } else {
          // Handle error
          console.error("Subscription failed");
          setMessage({
            text: `Failed to subscribe to topic. Please try again.`,
            variant: "danger",
          });
        }
      })
      .catch((error) => {
        setLoading(false);
        console.log("Error heree: ", error);
        setMessage({
          text: `${error}, Please try again.`,
          variant: "danger",
        });
        console.error("Error:", error);
      });
  };

  return (
    <Container
      fluid
      className="vh-100 d-flex justify-content-center align-items-center"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
      }}
    >
        <NavBar />
      <Card
        bg="dark"
        text="white"
        className="w-100"
        style={{ maxWidth: "50%", padding: "20px", borderRadius: "15px" }}
      >
        <Card.Header>Subscribe to a Topic</Card.Header>
        <Card.Body>
          {message && <Alert variant={message.variant}>{message.text}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Select Topic</Form.Label>
              <Form.Select
                aria-label="Select topic"
                value={selectedTopic}
                onChange={handleTopicChange}
              >
                <option>Select the topic</option>
                {topics.map((topic, index) => (
                  <option key={index} value={topic}>
                    {topic}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Button variant="light" type="submit">
              Submit
            </Button>
            {loading && (
            <div className="text-center">
                <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
                </Spinner>
            </div>
            )}
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default SubscribeForm;
