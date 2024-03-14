import React, { useState } from "react";
import { Form, Container, Button, Alert, Card, Spinner } from "react-bootstrap";
import axios from "axios";
import backgroundImage from "../wallpaper.png";
import NavBar from "./NavBar";
import { baseURL } from "../config";

const CreateTopicForm = (props) => {
  const [topic, setTopic] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const handleTopicChange = (e) => {
    setMessage("");
    setTopic(e.target.value);
  };

  const handleSubmit = (e) => {
    setLoading(true);
    e.preventDefault();
    axios
      .post(`${baseURL}/c_create_topic`, {
        topic: topic,
        timestamp: Date.now(),
      })
      .then((response) => {
        setLoading(false);
        console.log(response);
        if (response.status === 200) {
          // Subscription successful
          console.log(`${topic} Topic created`);
          setMessage({
            text: `${topic} Topic created successfully.`,
            variant: "success",
          });
          setTopic("");
        } else {
          // Handle error
          console.error("topic creation failed");
          setMessage({
            text: `Failed to add topic. Please try again.`,
            variant: "danger",
          });
        }
      })
      .catch((error) => {
        // console.log("Error heree: ", error);
        setLoading(false);
        setMessage({
          text: `${error.response.data.error}, Please try again.`,
          variant: "danger",
        });
        // console.error("Error:", error);
      });
  };

  const handleFormClick = () => {
    // Clear the alert message when the form is clicked
    setMessage("");
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
        <Card.Header>Create a Topic</Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit} onClick={handleFormClick}>
            <Form.Group className="mb-3">
              <Form.Control
                type="text"
                placeholder="Topic name"
                aria-label="Topic name example"
                onChange={handleTopicChange}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </Card.Body>
        {message && <Alert variant={message.variant}>{message.text}</Alert>}
        {loading && (
        <div className="text-center">
            <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
            </Spinner>
        </div>
        )}
      </Card>
    </Container>
  );
};

export default CreateTopicForm;
