import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Card, Accordion } from "react-bootstrap";
import SubscribeForm from "./SubscribeForm";
import UnsubscribeForm from "./UnsubscribeForm";
import CreateTopicForm from "./CreateTopicForm";

import backgroundImage from "../wallpaper.png";
// import backgroundImage from "../wallpaper3.jpg";
// import "./HomePage.css"; // Import CSS for styling

const HomePage = () => {
  // State to track which accordion item is active
  const [activeAccordion, setActiveAccordion] = useState("1");
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    // Fetch topics list from backend API
    axios.get("http://127.0.0.1:5000/get_topics")
      .then(response => {
        setTopics(response.data['topics']);
        // console.log(topics);
      })
      .catch(error => {
        console.error("Error fetching topics:", error);
      });
  }, []);

  const handleNewTopic = (newTopic) => {
    setTopics([...topics, newTopic]);
  };
  // Function to handle accordion item clicks
  const handleAccordionClick = (index) => {
    setActiveAccordion(index === activeAccordion ? null : index);
  };

  return (
    // <div>
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
        {/* Second Column */}
        <Col
          md={8}
          className="d-flex align-items-center justify-content-center"
        >
          <Card className="card" style={{ width: "80%" }}>
            <Card.Body>
              {/* Accordion */}
              <Accordion
                activeKey={activeAccordion}
                onSelect={handleAccordionClick}
              >
                <Row className="w-100">
                  <Col>
                    {/* Subscribe Column */}
                    <Accordion.Item eventKey="1">
                      <Accordion.Header>Subscribe</Accordion.Header>
                      <Accordion.Body>
                        <SubscribeForm topics={topics}/>
                      </Accordion.Body>
                    </Accordion.Item>
                  </Col>
                  <Col>
                    {/* Unsubscribe Column */}
                    <Accordion.Item eventKey="2">
                      <Accordion.Header>Unsubscribe</Accordion.Header>
                      <Accordion.Body>
                        <UnsubscribeForm />
                      </Accordion.Body>
                    </Accordion.Item>
                  </Col>
                  <Col>
                    {/* Create New Topic Column */}
                    <Accordion.Item eventKey="3">
                      <Accordion.Header>Create New Topic</Accordion.Header>
                      <Accordion.Body>
                        <CreateTopicForm onNewTopic={handleNewTopic}/>
                      </Accordion.Body>
                    </Accordion.Item>
                  </Col>
                </Row>
              </Accordion>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
    // </div>
  );
};

export default HomePage;
