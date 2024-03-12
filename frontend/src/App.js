import React, { useState, useRef } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import SubscribeForm from "./pages/SubscribeForm";
import UnsubscribeForm from "./pages/UnsubscribeForm";
import CreateTopicForm from "./pages/CreateTopicForm";
import PublishForm from "./pages/PublishForm";
import MessageFeed from "./pages/MessageFeed";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<HomePage />} />
        <Route path="/subscribe" element={<SubscribeForm />} />
        <Route path="/unsubscribe" element={<UnsubscribeForm />} />
        <Route path="/create-topic" element={<CreateTopicForm />} />
        <Route path="/publish" element={<PublishForm />} />
        <Route path="/message-feed" element={<MessageFeed />} />
      </Routes>
    </Router>
  );
}

export default App;
