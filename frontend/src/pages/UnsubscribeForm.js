import React, { useState, useEffect } from "react";
import { Form, Container, Button, Alert } from "react-bootstrap";
import axios from "axios";

const UnsubscribeForm = () => {
  const [email, setEmail] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("");
  const [message, setMessage] = useState("");
  const [topics, setTopics] = useState([]);

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
  
    // Fetch subscribed topics for the user
    axios.get("http://127.0.0.1:5000/get_subscribed_topics", { params :{
        email: email
      }})
    .then(response => {
        setTopics(response.data['subscribed_topics'])
        // console.log("here: ", topics);
    //   const subscribedTopics = response.data['subscribed_topics'];
  
      // Check if the selected topic is in the list of subscribed topics
      if (topics.includes(selectedTopic)) {
        // Topic is subscribed, send unsubscribe request
        // axios.post("http://127.0.0.1:5000/unsubscribe", {
        //   email: email,
        //   topic: selectedTopic,
        //   timestamp: Date.now()
        // })
        // .then((response) => {
        //   console.log(response);
        //   if (response.status === 200) {
        //     // Unsubscription successful
        //     console.log("Unsubscription successful");
        //     setMessage({
        //       text: `Unsubscribed from ${selectedTopic}.`,
        //       variant: "success"
        //     });
        //     setEmail("");
        //     setSelectedTopic("");
        //   } else {
        //     // Handle error
        //     console.error("Unsubscription failed");
        //     setMessage({
        //       text: `Failed to unsubscribe from topic. Please try again.`,
        //       variant: "danger"
        //     });
        //   }
        // })
        // .catch((error) => {
        //   // Handle error from unsubscribe request
        //   console.error("Error:", error);
        //   setMessage({
        //     text: `${error.response.data.error}, Please try again.`,
        //     variant: "danger"
        //   });
        // });
        console.log("topic in the list");
      } else {
        // Topic is not subscribed, display alert message
        setMessage({
          text: `You are not subscribed to ${selectedTopic}.`,
          variant: "warning"
        });
      }
    })
    .catch(error => {
      // Handle error fetching subscribed topics
      console.error("Error fetching subscribed topics:", error);
      setMessage({
        text: "Failed to fetch subscribed topics. Please try again.",
        variant: "danger"
      });
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
          <Form.Control type="email" placeholder="Enter email" onChange={handleEmailChange} />
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
        <Button variant="danger" type="submit">
          Unsubscribe
        </Button>
      </Form>
    </Container>
  );
};

export default UnsubscribeForm;
