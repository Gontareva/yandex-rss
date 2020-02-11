var express = require('express');
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.contentType('application/rss+xml');

  res.sendFile(path.join(__dirname, '../views', 'rssPublications.html'), { title: 'Express' });
});

module.exports = router;
