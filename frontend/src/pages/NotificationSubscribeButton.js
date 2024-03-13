import React from "react";
import { Button } from "react-bootstrap";

function NotificationSubscribeButton() {
  const handleSubscribe = () => {
    if ("Notification" in window) {
      Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
          console.log("Notification permission granted.");
        }
      });
    }
  };

  return <Button onClick={handleSubscribe}>Subscribe to Notifications</Button>;
}

export default NotificationSubscribeButton;
