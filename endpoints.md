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

----

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
| tags | `/menus?tags=chicken` | list all menus with `chicken` tag associated | |
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
| restaurant_id | ✔ | ID of restaurant that this menu belongs to | |
| name | ✔ | name of menu (can be in non-English) | |
| price | ✔ | price of menu (up to 2 decimal places) | |
| currency | ✔ | three-character currency (price-related) | 'JPY' |
| images | ✔ | list of image links related to this menu | |
| tags | ✔ | list of tags to associate with this menu | |

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
| name | ✔| name of menu (can be in non-English) | |
| price | ✔ | price of menu (up to 2 decimal places) | |
| currency | ✔ | three-character currency (price-related) | 'JPY' |
| images | ✔ | list of image links related to this menu | |
| tags | ✔ | list of tags to associate with this menu | |

Take note that you are not allowed to change the menu's associated restaurant ID. To do so, we recommend you delete the menu and recreate.

> Delete a menu

```
DELETE /menus/:menu_id
```

This deletes the above menu, returning a `200 OK` status code if successful.

----

#### Restaurants

[TODO]

----

#### Ratings (Menu)

You can search for ratings of the menus from the user perspective (i.e., which menus have the user rated).
More interestingly, you can also list ratings as from the ranking perspective (i.e., which menus are ranked top for `chicken` tag).

> List a user's menu ratings

```
GET /user/:user_id/ratings/menus
```


> List the menu ratings (ranked top-down)

```
GET /ratings/menus
```

You need to further query/filter the list of menu ratings with **at least one** of following parameters:

| parameter | example | description | default |
| ---- | ---- | ---- | ---- |
| tags | `/ratings/menus?tags=chicken` | list all menu ratings for menus having the `chicken` tag | |
| price | `/ratings/menus?price=100,500` | list all menu ratings for menus priced between 100￥ to 500￥ (inclusive) | |
