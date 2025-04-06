const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
  host: '10.104.61.47',
  user: 'project_user',
  password: 'yourStrongPassword',
  database: 'dbHackKU'
});

db.connect(err => {
  if (err) throw err;
  console.log('Connected to MySQL');
});

app.get('/data', (req, res) => {
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

app.get('/wellbeing', (req, res) => {
  const query = `SELECT * FROM DigitalWellbeing`;

  db.query(query, (err, results) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(results);
  });
});


app.get('/run-python', (req, res) => {
  execFile('python3', ['my_script.py'], (error, stdout, stderr) => {
    if (error) {
      console.error('Python error:', error);
      return res.status(500).send('Python script failed');
    }
    res.send(`Python output: ${stdout}`);
  });
});



app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
