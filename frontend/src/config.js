const ip = process.env.REACT_APP_SUBSCRIBER_IP || "127.0.0.1";
const port = process.env.REACT_APP_SUBSCRIBER_PORT || "8000";
const baseURL = `http://${ip}:${port}`;

export { baseURL };
