var express = require('express');
var router = express.Router();

/* GET restaurant list page. */
router.get('/', function(req, res) {
  res.render('restaurant/list', 
  	{
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
});

/* GET retaurant detail page. */
// TODO

module.exports = router;