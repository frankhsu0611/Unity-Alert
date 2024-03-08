import React from "react";
import { Form, Container, Button } from "react-bootstrap";

const UnsubscribeForm = () => {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission to backend
  };

  return (
    <Container fluid>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" />
          <Form.Text className="text-muted">
            We'll never share your email with anyone else.
          </Form.Text>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Select aria-label="Default select example">
            <option>Select the topic</option>
            <option value="1">Topic1</option>
            <option value="2">Topic2</option>
            <option value="3">Topic3</option>
          </Form.Select>
        </Form.Group>
        <Button variant="danger" type="submit">
          Unsubscribe
        </Button>
      </Form>
    </Container>
  );
};

export default UnsubscribeForm;
