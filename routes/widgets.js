var express = require('express');
var router = express.Router();
var path = require('path');
var request = require('request');

/* GET home page. */
router.get('/', function(req, res, next) {
   request(
       'https://culture.servmedia.ru/embedded/widgets/6', function(error, response, body) {
           console.log(error, response, body)
  res.send(body);
       }
   )


});

module.exports = router;
