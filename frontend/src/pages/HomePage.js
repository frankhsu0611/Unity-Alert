import React, { useEffect, useState } from "react";
import { ButtonGroup, Button, Container, Row, Col } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import backgroundImage from "../wallpaper.png";

const HomePage = () => {
  // const [topics, setTopics] = useState([]);
  const navigate = useNavigate();

  return (
    <Container
      fluid
      className="vh-100"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
      }}
    >
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
          <ButtonGroup vertical>
            <Button variant="primary" onClick={() => navigate("/subscribe")}>
              Subscribe
            </Button>
            <Button
              variant="secondary"
              onClick={() => navigate("/unsubscribe")}
            >
              Unsubscribe
            </Button>
            <Button variant="success" onClick={() => navigate("/create-topic")}>
              Create Topic
            </Button>
            <Button variant="warning" onClick={() => navigate("/publish")}>
              Publish Message
            </Button>
            <Button variant="info" onClick={() => navigate("/message-feed")}>
              Message Feed
            </Button>
          </ButtonGroup>
        </Col>
      </Row>
    </Container>
  );
};

export default HomePage;
