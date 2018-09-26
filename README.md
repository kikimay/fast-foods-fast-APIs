<<<<<<< HEAD
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

![license](https://img.shields.io/github/license/mashape/apistatus.svg)

# Fast Food Fast

Fast food fast is a fast food delivery application. It allows a user to order food from the restautant and have it delivered to them.

## Getting Started

These instructions will guid you on how to deploy this system locally. For live systems, you will need to consult deployment notes of flask systems for that.

To get started first you need a machine that can run on Python3 and handle postgres database.

### Prerequisites

You will need these installed first before we go any further.

- [Python3.6](https://www.python.org/downloads/release/python-365/)

- [Virtual Environment](https://virtualenv.pypa.io/en/stable/installation/)


For Virtual Environment, you can install like this after Installing Python3:

```
pip install virtualenv
```
```
pip install virtualenvwrapper
```


## Installation and Running


### Installing

Clone the repository below

```
git clone -b development https://github.com/kikimay/fast-foods-fast-APIs.git
```

Create a virtual environment

```
    virtualenv venv --python=python3.6
```

Activate virtual environment

```
    source venv/bin/activate
```

Install required Dependencies

```
    pip install -r requirements.txt
```



### Running

Start the flask server on your command prompt:

    First you need to ``` cd ``` to your project root directory

Then:

```
    python run.py
```

With the server running, paste this in your browser's address bar:

```
    localhost:5000/
```

This is the welcome page.



## Running the tests

This repository contains tests to test the functionality of the API.

To run these tests, run the following command:

### Running all tests.

These tests test the ``` Foods Class, Orders Class, and the Users Class```

In the project's root directory, with the virtual environment running, run this command:

```
pytest
```


### Running specific test scripts

It is possible to run test scripts individually. 

``` cd ``` to your tests directory.

```
pytest test_users.py
```
to test the class Users only.



# Endpoints Available

|    #   | Method | Endpoint                        | Description                           |
|--------| ------ | ------------------------------- | ------------------------------------- |
|    1   | GET    | /                               | Index/Welcome page                    |
|    2   | POST   | /api/v1/register                | Create new user                       |
|    3   | POST   | /api/v1/login                   | Login a registered user               |
|    4   | GET    | /api/v1/logout                  | Logout a logged in user               |
|    5   | POST   | /api/v1/add_food                | Create a new food item                |
|    6   | GET    | /api/v1/foods                   | Retrieve all foods                    |
|    7   | GET    | /api/v1/foods/<int:food_id>     | Retrieve a specific food by food id   |
|    8   | DELETE | /api/v1/foods/<int:food_id>     | Delete a specific food by food id     |
|    9   | PUT    | /api/v1/foods/<int:food_id>     | Update a specific food by food id     |
|    10  | POST   | /api/v1/place_order             | Place an order                        |
|    11  | GET    | /api/v1/orders                  | Retrieve all orders                   |
|    12  | GET    | /api/v1/orders/<int:order_id>   | Retrieve a specific order             |
|    13  | PUT    | /api/v1/orders/<int:order_id>   | Accept an order                       |
|    14  | PUT    | /api/v1/orders/<int:order_id>   | Decline an order                      |
|    15  | PUT    | /api/v1/orders/<int:order_id>   | Complete an order                     |




## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [pip](https://pypi.org/project/pip/) - Dependency Management


## Authors

* **Maryn Mwirigi** -  - [Kikimay](https://github.com/kikimay)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

