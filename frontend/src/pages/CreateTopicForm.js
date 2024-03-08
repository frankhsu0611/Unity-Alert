import React from "react";
import { Form, Container, Button } from "react-bootstrap";

const CreateTopicForm = () => {
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
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Control
            type="text"
            placeholder="Topic name"
            aria-label="Topic name example"
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
