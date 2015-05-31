# Snakebite

## API Overview

Snakebite is the backend API server for Gobbl, responding to HTTP requests with JSON responses.
Design-wise, Snakebite tries to adheres to RESTful design principles in terms of routing syntax.

### API Endpoints

Currently, the resources that end users or clients can get access to are the following:

- Menu `/menus`
- Restaurant `/restaurants`
- Rating `/ratings`


Additionally, we opened up a `/batch` endpoint to handle all batch-related operations so that batch requests can be performed with fewer HTTP requests.

We will go through the allowable methods on each of the resources.

#### Menu

> List menus

```
GET /menus
```

You can further query/filter the list of menus with the following parameters:

| parameter | example | description | default |
| ---- | ---- | ---- | ---- |
| name | `/menus?name=curry` | list all menus with `curry` in their name | |
| price | `/menus?price=100,500` | list all menus between 100￥ to 500￥ (inclusive) | |
| rating | `/menus?rating=3,5` | list all menus with rating between 3 to 5 (inclusive) | |
| geolocation | `/menus?geolocation=1,2` | list all menus within distance (1km default) from geolocation of longitude 1, latitude 2 | |
| maxDist | `/menus?geolocation=1,2&maxDist=200` | list all menus within 200m from geolocation of longitude 1, latitude 2 | 1000 |

> Get single menu

```
GET /menus/:menu_id
```

This gets the individual menu (ID: menu_id)

> Create a menu

```
POST /menus
```

You can create a new menu via the above method and the following items are required in the payload:

| parameter | required | description | default |
| ---- | ---- | ---- | ---- |
| restaurant_id | YES | ID of restaurant that this menu belongs to | |
| name | YES | name of menu (can be in non-English) | |
| price | YES | price of menu (up to 2 decimal places) | |
| currency | YES | three-character currency (price-related) | 'JPY' |
| images | YES | list of image links related to this menu | |
| tags | YES | list of tags to associate with this menu | |

```
# Example post using CURL

$ curl -X POST http://snakebite.herokuapp.com/menus -H 'Content-Type: application/json'
  -d '{"name": "test menu", "restaurant_id": "sahriwerfhvn21", "price": 800, "currency": "JPY", "images": ["http://example.com/curry.jpg"], "tags": ["chicken", "curry"]}'

```

> Update a menu

```
PUT /menus/:menu_id
```

You can update an existing menu via the above method and the following items can be sent in the payload:

| parameter | required | description | default |
| ---- | ---- | ---- | ---- |
| name | YES | name of menu (can be in non-English) | |
| price | YES | price of menu (up to 2 decimal places) | |
| currency | YES | three-character currency (price-related) | 'JPY' |
| images | YES | list of image links related to this menu | |
| tags | YES | list of tags to associate with this menu | |

Take note that you are not allowed to change the menu's associated restaurant ID. To do so, we recommend you delete the menu and recreate.

> Delete a menu

```
DELETE /menus/:menu_id
```

This deletes the above menu, returning a `200 OK` status code if successful.
