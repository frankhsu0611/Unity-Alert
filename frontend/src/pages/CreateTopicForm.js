import React, {useState} from "react";
import { Form, Container, Button, Alert } from "react-bootstrap";
import axios from "axios";

const CreateTopicForm = (props) => {
  const [email, setEmail] = useState("");
  const [topic, setTopic] = useState("");
  const [message, setMessage] = useState("");


  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleTopicChange = (e) => {
    setMessage("")
    setTopic(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("http://127.0.0.1:5000/create_topic", {
        email: email,
        topic: topic,
        timestamp: Date.now()
      })
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          // Subscription successful
          console.log(`${topic} Topic created`);
          props.onNewTopic(topic);
          setMessage({
            text: `${topic} Topic created successfully.`,
            variant: "success"
          });
          setEmail("");
        setTopic("");
        } else {
          // Handle error
          console.error("topic creation failed");
          setMessage({
            text: `Failed to add topic. Please try again.`,
            variant: "danger"
          });
        //   setEmail("");
        // setTopic("");
        }
      })
      .catch((error) => {
        // console.log("Error heree: ", error);
        setMessage({
            text: `${error.response.data.error} Please try again.`,
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
          <Form.Control type="email" placeholder="Enter email" onChange={handleEmailChange}/>
        </Form.Group>
        {/* <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" />
        </Form.Group> */}
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
    </Container>
  );
};

export default CreateTopicForm;
