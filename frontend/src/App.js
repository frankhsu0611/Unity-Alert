import React, { useState, useRef } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  redirect,
  Navigate,
} from "react-router-dom";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<HomePage />} />
      </Routes>
    </Router>
  );
}

export default App;
