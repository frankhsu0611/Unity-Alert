// NavBar.js
import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const NavBar = () => {
  return (
    <Navbar variant="dark" expand="lg" fixed="top">
      <Navbar.Brand href="/">Unity Alert</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="me-auto">
          <LinkContainer to="/subscribe">
            <Nav.Link>Subscribe</Nav.Link>
          </LinkContainer>
          <LinkContainer to="/create-topic">
            <Nav.Link>Create Topic</Nav.Link>
          </LinkContainer>
          <LinkContainer to="/publish">
            <Nav.Link>Publish Message</Nav.Link>
          </LinkContainer>
          <LinkContainer to="/message-feed">
            <Nav.Link>Message Feed</Nav.Link>
          </LinkContainer>
          <LinkContainer to="/unsubscribe">
            <Nav.Link>Unsubscribe</Nav.Link>
          </LinkContainer>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavBar;
