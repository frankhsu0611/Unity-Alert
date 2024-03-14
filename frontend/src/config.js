const ip = process.env.SUBSCRIBER_IP || '127.0.0.1'; // Default IP if not provided via environment variables
const port = process.env.SUBSCRIBER_PORT || '8000'; // Default port if not provided via environment variables
const baseURL = `http://${ip}:${port}`;

export { baseURL };