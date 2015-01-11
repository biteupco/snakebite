var express = require('express');
var router = express.Router();
var request = require('request');
var querystring = require('querystring');

var SERVER_URL;

/* GET restaurant list page. */
router.get('/', function(req, res) {
  
  SERVER_URL = req.app.get('config')['api']['url'];
  
  var qry = querystring.stringify(req.query);
  var url = SERVER_URL + '/restaurants';
  url = qry? (url + '?' + qry) : url;
  request({url: url, headers: {'Content-Type': 'application/json'}, method: 'get', json: true}, function(err, resp, body){

    if(err) throw err;

    switch(resp.statusCode){
      case 200: {
        render(body.items);
        break;
      }
      default: {
        render();
        break;
      }
    };
  });

  function render(restaurants){
      res.render('restaurant/list', 
          {
            restaurants: restaurants || [],
            title: "Restaurants",
            action_map: {
              "Action": "#", 
              "Another Action": "#"
            },
            filter_options: [
              {name: "name", label: "Name", type: "text", value: ""},
              {name: "tags", label: "Tags", type: "text", value: ""},
              {name: "address", label: "Address", type: "text", value: ""},
              {name: "ctime", label: "Created After", type: "date", value: ""},
            ] 
          }
       );
  };
});

/* GET retaurant detail page. */
router.get('/:id', function(req, res) {

  SERVER_URL = req.app.get('config')['api']['url'];
  
  var url = SERVER_URL + '/restaurants/' + req.params.id;
  request({url: url, headers: {'Content-Type': 'application/json'}, method: 'get', json: true}, function(err, resp, body){

    if(err) throw err;

    switch(resp.statusCode){
      case 200: {
        render(body);
        break;
      }
      default: {
        render();
        break;
      }
    };
  });
  
  function render(restaurant){
    res.render('restaurant/detail', 
      {
        title: "Restaurant @" + req.params.id,
        restaurant: restaurant,
        action_map: {
          "Action": "#", 
          "Another Action": "#"
        }
      }
   );
  }
});

module.exports = router;