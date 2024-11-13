const express = require('express');
const ejs = require('ejs');
const haikus = require('./haikus.json');
const app = express();
const port = process.env.PORT || 3000;

// Static files and view engine setup
app.use(express.static('public'));
app.set('view engine', 'ejs');

// Routes
app.get('/', (req, res) => {
  res.render('index', {haikus: haikus});
});

// Start server
app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});