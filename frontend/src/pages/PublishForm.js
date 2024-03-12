import React, { useState, useEffect } from "react";
import { Form, Button, Alert, Container, Card } from "react-bootstrap";
import axios from "axios";
import backgroundImage from "../wallpaper.png";

const PublishForm = () => {
  const [selectedTopic, setSelectedTopic] = useState("");
  const [message, setMessage] = useState("");
  //   const [feedback, setFeedback] = useState("");
  const [topics, setTopics] = useState([]);
  const [alertMessage, setAlertMessage] = useState("");

  useEffect(() => {
    // Fetch topics list from backend API
    axios
      .get("http://127.0.0.1:8000/c_get_topics")
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
    setAlertMessage("");
    setSelectedTopic(e.target.value);
  };
  const handleMessageChange = (e) => {
    setAlertMessage("");
    setMessage(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedTopic || !message) {
      setAlertMessage("Please select a topic and write a message.");
      return;
    }
    axios
      .post("http://127.0.0.1:8000/c_publish", {
        topic: selectedTopic,
        content: message,
        timestamp: Date.now(),
      })
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          // setFeedback("Message published successfully!");
          setMessage("");
          setAlertMessage({
            text: `Message published successfully!`,
            variant: "success",
          });
        } else {
          console.error("Failed to publish message");
          setAlertMessage({
            text: `Failed to publish message. Please try again. `,
            variant: "danger",
          });
        }
      })
      .catch((error) => {
        //   setFeedback("Failed to publish message. Please try again.");
        console.error("Publish error:", error);
        setAlertMessage({
          text: `${error}, Please try again.`,
          variant: "danger",
        });
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
      <Card
        bg="dark"
        text="white"
        className="w-100"
        style={{ maxWidth: "50%", padding: "20px", borderRadius: "15px" }}
      >
        {alertMessage && (
          <Alert variant={alertMessage.variant}>{alertMessage.text}</Alert>
        )}
        <Card.Header>Publish a message</Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            {/* {feedback && <Alert variant="info">{feedback}</Alert>} */}
            <Form.Group className="mb-3">
              <Form.Label>Topic</Form.Label>
              <Form.Select
                aria-label="Select topic"
                value={selectedTopic}
                onChange={handleTopicChange}
              >
                <option>Select a topic</option>
                {topics &&
                  topics.map((topic) => (
                    <option key={topic} value={topic}>
                      {topic}
                    </option>
                  ))}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Message</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={message}
                onChange={handleMessageChange}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Publish
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default PublishForm;
