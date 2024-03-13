import React, { useEffect, useState } from "react";
import { ButtonGroup, Button, Container, Row, Col, Form, Alert, Card } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import backgroundImage from "../wallpaper.png";
import NavBar from "./NavBar";

const HomePage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [uuid, setUUID] = useState('');
  const userUuid = localStorage.getItem('userUuid');

  const handleEmailChange = (e) => {
    setMessage("");
    setEmail(e.target.value);
  };

  const handleUserNameChange = (e) => {
    setMessage("");
    setUsername(e.target.value);
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    axios.post('http://127.0.0.1:8000/c_register', { 'username':username, 'email':email })
    .then((response) => {
      const { user_uuid } = response.data;
      setUUID(user_uuid);

      // Store the UUID in localStorage
      localStorage.setItem('userUuid', user_uuid);

      // Success message or redirect user
      
      setMessage({
        text: `Registration successful!`,
        variant: "success",
      });

    })
    .catch((error) => {
      console.error('Registration failed:', error);
      setMessage({
        text: `Registration failed. Please try again.`,
        variant: "danger",
      });
    });
  };

  // const [topics, setTopics] = useState([]);
  const navigate = useNavigate();

  return (
    <Container
      fluid
      className="vh-100 overflow-hidden"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
      }}
    > 
        <NavBar />
      <Row className="h-100 align-items-center justify-content-center">
        {/* First Column */}
        <Col md={4} className="background-column">
          <div className="background-image">
            <div className="title-tagline text-left">
              <h1 style={{ color: "white" }}>Unity Alert</h1>
            </div>
            <h3 style={{ color: "gray" }}>Stay Connected, Stay Safe!</h3>
          </div>
        </Col>
        <Col
          md={8}
          className="d-flex align-items-center justify-content-center"
        >
            {userUuid ? <ButtonGroup vertical>
            <Button variant="primary" onClick={() => navigate("/subscribe")}>
              Subscribe
            </Button>
            <p style={{ color: "white" }}>Stay informed by subscribing to alerts and updates relevant to your interests and location.</p>
            <Button
              variant="secondary"
              onClick={() => navigate("/unsubscribe")}
            >
              Unsubscribe
            </Button>
            <p style={{ color: "white" }}>Manage your subscriptions and opt-out of alerts that are no longer relevant to you.</p>
            <Button variant="success" onClick={() => navigate("/create-topic")}>
              Create Topic
            </Button>
            <p style={{ color: "white" }}>Empower your community by creating new topics for sharing alerts and critical updates.</p>
            <Button variant="warning" onClick={() => navigate("/publish")}>
              Publish Message
            </Button>
            <p style={{ color: "white" }}>Contribute to community safety by publishing timely information and alerts.</p>
            <Button variant="info" onClick={() => navigate("/message-feed")}>
              Message Feed
            </Button>
            <p style={{ color: "white" }}>Access a consolidated feed of important alerts and updates you might have missed, ensuring you're always informed about the latest community safety news and emergency situations.</p>
          </ButtonGroup> : <Card style={{ width: '30rem', padding: '20px', borderRadius: '10px' }}>
        <Card.Header><p className="mt-3">
            Join Unity Alert today and be a part of a safer, more connected community.
        </p></Card.Header>
        <Card.Body>
        
          <Form onSubmit={handleRegister}>
            <Form.Group className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={handleUserNameChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={handleEmailChange}
                required
              />
            </Form.Group>

            <Button variant="primary" type="submit">
              Register
            </Button>

            {message && <Alert variant={message.variant}>{message.text}</Alert>}
          </Form>
        </Card.Body>
      </Card>}
        </Col>
      </Row>
    </Container>
  );
};

export default HomePage;
