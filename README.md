# StripeAPI

The goal of this project is to learn how to use Stripe API and Django together.

This project use Django 4.1.

# Getting Started

1. First clone the repository from Github and switch to the new directory:

```bash
git clone git@github.com:SerHappy/stripeAPI.git
cd stripeAPI
```

2. Activate the virtualenv for your project.

_Installing inside virtualenv is recommended, however you can start your project without virtualenv too._

2.1 Create virtualenv:

```bash
python -m venv env
```

2.2 Activate virtualenv (Windows):

```bash
.\venv\Scripts\activate
```

2.3 Activate virtualenv (Unix):

```bash
source env/bin/activate
```

3. Install project dependencies

```bash
pip install -r requirements.txt
```

4. Then simply apply the migrations:

```bash
python manage.py migrate
```

5. Now you can run the development server:

```bash
python manage.py runserver
```

## API Examples

#### Get HTML with Stripe payment button for Item with id=1

```bash
  curl -X GET http://localhost:8000/item/1/
```

| Parameter | Type  | Description           |
| :-------- | :---- | :-------------------- |
| `id`      | `int` | **Required**. item id |

#### The result:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Item 1 info page</title>
  </head>

  <body>
    <script src="https://js.stripe.com/v3/"></script>
    <script src="http://code.jquery.com/jquery-1.10.2.js"></script>
    <h1>Item name</h1>
    <p>Item 1</p>
    <br />
    <h1>Item description</h1>
    <p>Description of item 1</p>
    <br />
    <h1>Item price</h1>
    <p>100.0 $</p>
    <br />
    <button id="clickMe">Buy</button>
    <input type="hidden" id="url" data-url="/buy/1/" />
    <script defer src="/static/buy.js"></script>
  </body>
</html>
```
