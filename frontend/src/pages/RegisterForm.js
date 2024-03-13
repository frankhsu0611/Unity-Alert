import React, { useState } from 'react';
import { Form, Button, Container, Card, Alert } from 'react-bootstrap';
import axios from 'axios';

const RegisterForm = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [uuid, setUUID] = useState('');
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

    axios.post('http://127.0.0.1:8000/c_register', { username, email })
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

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: "100vh" }}>
        
      <Card style={{ width: '30rem', padding: '20px', borderRadius: '10px' }}>
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
      </Card>
    </Container>
  );
};

export default RegisterForm;
