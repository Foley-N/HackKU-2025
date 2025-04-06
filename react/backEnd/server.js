const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");
const { execFile } = require("child_process");

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
  host: "10.104.61.47",
  user: "project_user",
  password: "yourStrongPassword",
  database: "dbHackKU",
});

db.connect((err) => {
  if (err) throw err;
  console.log("Connected to MySQL");
});

app.get("/data", (req, res) => {
  const query = `
    SELECT * 
    FROM activities
    WHERE activityStartTime LIKE '2025-04-04%' 
       OR activityStartTime LIKE '2025-04-05%' 
       OR activityStartTime LIKE '2025-04-06%';
  `;

  db.query(query, (err, results) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(results);
  });
});

app.get("/wellbeing", (req, res) => {
  const query = `SELECT * FROM DigitalWellbeing`;

  db.query(query, (err, results) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(results);
  });
});

app.get("/run-python-script", (req, res) => {
  const action = req.query.action;

  if (!action) {
    return res.status(400).send("Action is required");
  }
  const scriptArgument =
    action === "1"
      ? "post_run_suggestion"
      : action === "0"
      ? "goal_setting"
      : "";

  if (!scriptArgument) {
    return res.status(400).send("Unknown action");
  }

  execFile(
    "python",
    [
      "C:\\Users\\50vjt\\OneDrive\\문서\\GitHub\\HackKU-2025\\react\\backEnd\\gemini_test.py",
      scriptArgument,
    ],
    (error, stdout, stderr) => {
      if (error) {
        console.error("Python error:", error);
        return res.status(500).send(`Python script failed: ${stderr}`);
      }
      res.send(stdout); // Return the Python script output
    }
  );
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
