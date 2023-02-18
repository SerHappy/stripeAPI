# StripeAPI

The goal of this project is to learn how to use [Stripe API](https://stripe.com/docs) and [Django](https://docs.djangoproject.com/en/4.1/) together.

This project use Django 4.1.

## Features

- Launching using Docker
- Using environment variables
- Viewing Django Models in the Django Admin panel
- Model Order
- Item.currency field

## Before start

1.First clone the repository from Github and switch to the new directory:

```sh
git clone git@github.com:SerHappy/stripeAPI.git
cd stripeAPI
```

2.Rename .env-example to .env and fill it with your data.

*Django test secret key: django-insecure-ar=$!pe)cy9c^\*-t-#$ei$iv&@)bf+4t)!ci2^y_nairmgm9^5*

```text
DJANGO_SECRET_KEY=
DEBUG=
```

3.Activate the virtualenv for your project.

*Installing inside virtualenv is recommended, however you can start your project without virtualenv too.*

3.1 Create virtualenv:

```sh
python -m venv env
```

3.2 Activate virtualenv (Windows):

```sh
.\env\Scripts\activate
```

3.3 Activate virtualenv (Unix):

```sh
source env/bin/activate
```

4.Install project dependencies

```sh
pip install -r requirements.txt
```

5.Then simply apply the migrations:

```sh
python manage.py migrate
```

## Get started

To run this project properly you should add some items and its prices.

1.Create superuser

```sh
python manage.py createsuperuser
```

2.Log in into admin panel (open [admin panel](http://localhost:8000/admin))

3.Go to Currencys.

4.Press add currency.

5.Add USD and EUR currencies.

6.Add items.

7.Add ItemCurrencys for every item (2 ItemCurrencys for each item).

8.Now you can run the development server:

```sh
python manage.py runserver
```

## Docker

*0.Download and install [Docker](https://docs.docker.com/get-docker/)*

1.Build docker image

```sh
docker build -t app .
```

2.Create and start container

```sh
docker run --rm -d --publish 8000:8000 <image_id>
```

3.Open [localhost](http://localhost:8000/) (or 0.0.0.0:8000) in your browser.

## Docker with docker-compose

*0. Download and install [Docker-compose](https://docs.docker.com/compose/install/)*

1. Build docker image, create and start container

```sh
docker-compose up --build
```

2.Open [localhost](http://localhost:8000/) (or 0.0.0.0:8000) in your browser.

## Docker image

1.Or you can just download docker image

```sh
docker pull serhappy/app:firstly
```

2.And run it

```sh
docker run --rm -d --publish 8000:8000 serhappy/app:firstly
```

## Django tests

1.Run tests

```sh
python manage.py test
```

### Possible result

```sh
Found 16 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
................
----------------------------------------------------------------------
Ran 16 tests in 5.178s

OK
Destroying test database for alias 'default'...
```

## API Examples

### Get HTML with Stripe payment button for Item with id=1

```sh
  curl -X GET http://localhost:8000/item/1/
```

| Parameter | Type  |     Description       |
| :-------- | :---- | :-------------------- |
|   `id`    | `int` | **Required**. item id |

### The result

```html
<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Item 1 info page</title>
</head>

<body>
  <script src="https://js.stripe.com/v3/"></script>
  <script src="http://code.jquery.com/jquery-1.10.2.js"></script>
  <h1>Item name</h1>
  <p>Item 1</p>
  <br>
  <h1>Item description</h1>
  <p>Item 1 desc</p>
  <br>
  <h1>Item prices</h1>
  <p>100.0 USD</p>
  <p>94.0 EUR</p>
  <select id="SelectCurrency">
    <option value=USD>USD</option>
    <option value=EUR>EUR</option>
  </select>
  <button id="clickMe">Buy</button>
  <input type="hidden" id="url" data-url="/buy/1/">
  <script defer src="/static/buy.js"></script>
  <form action="/add/1/" method="POST">
    <input type="hidden" name="csrfmiddlewaretoken" value="MvjWy0egC1hDJDYrDL6SwxsejZMvV79hfZYLXzEkOkdLkqiFwEi7GqVmowlmdxce">
    <button type='submit' id="order"> <span class="text">Add to
        cart</span></button>
</body>
</html>
```
