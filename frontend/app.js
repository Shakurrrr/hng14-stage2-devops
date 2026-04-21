const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();


// CONFIG (ENV-FIRST)

const API_URL = process.env.API_URL || "http://api:8000";


// MIDDLEWARE

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));


// ROUTES


// Submit job
app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`, req.body, {
      timeout: 5000
    });

    return res.status(200).json(response.data);
  } catch (err) {
    console.error("[FRONTEND ERROR] Submit failed:", err.message);

    return res.status(500).json({
      error: "failed to submit job",
      details: err.message
    });
  }
});

// Check job status
app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(
      `${API_URL}/jobs/${req.params.id}`,
      { timeout: 5000 }
    );

    return res.status(200).json(response.data);
  } catch (err) {
    console.error("[FRONTEND ERROR] Status check failed:", err.message);

    return res.status(500).json({
      error: "failed to fetch job status",
      details: err.message
    });
  }
});

// START SERVER
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
  console.log(`API connected at ${API_URL}`);
});