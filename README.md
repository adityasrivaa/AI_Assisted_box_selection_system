# AI-Assisted Box Selection System

A Django REST API for selecting a suitable shipping box for ecommerce orders. The system considers product dimensions, quantities, total weight, box capacity, and cost when recommending a box.

## Features

* Manage products and shipping boxes
* Create and manage orders and order items
* Calculate order weight based on product quantities
* Check whether products fit inside a box with rotation support
* Validate the maximum weight capacity of boxes
* Keep box-selection logic in a separate service
* Select the lowest-cost suitable box
* REST APIs using Django REST Framework
* Automated tests for the main functionality

## Tech Stack

* **Python**
* **Django**
* **Django REST Framework**
* **SQLite**
* **Decimal** for accurate weight and cost calculations

## Project Structure

```text
config/
└── Project configuration

box_selection/
├── models.py
├── serializers.py
├── views.py
├── urls.py
├── services/
│   └── box_selector.py
└── tests/
```

The main box-selection logic is kept inside the service layer rather than putting business logic directly into the API views. This makes the logic easier to test, maintain, and modify later.

## API Endpoints

| Method     | Endpoint                            | Description                          |
| ---------- | ----------------------------------- | ------------------------------------ |
| GET / POST | `/api/products/`                    | Create and view products             |
| GET / POST | `/api/boxes/`                       | Create and view boxes                |
| GET / POST | `/api/orders/`                      | Create and view orders               |
| GET        | `/api/orders/<id>/recommended-box/` | Get the recommended box for an order |

## Dependencies

```bash
pip install django djangorestframework
```
## Project Creation

```bash
django-admin startproject config .
python manage.py startapp box_selection
```

## Installation

```bash

cd box_selection_project
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API can then be accessed at:

```text
http://127.0.0.1:8000/api/
```

## Running Tests

To run the automated tests:

```bash
python manage.py test
```

## How Box Selection Works

When an order is submitted, the box-selection service performs the following steps:

1. Calculates the total weight of the order.
2. Takes the quantity of each product into account.
3. Checks whether the total weight is within the box's maximum capacity.
4. Checks whether the products can fit inside the box, including possible product rotations.
5. Uses the project's packing approach when an order contains multiple products.
6. Compares the valid boxes and selects the cheapest suitable option.

### Packing Limitation

The current implementation uses a practical heuristic for packing multiple products. It checks the required dimensions and other constraints, but it does not attempt to solve the complete mathematical 3D bin-packing problem.

Because of this, a valid result from the service does not necessarily mean that the products are packed in the mathematically most space-efficient arrangement.

## Assumptions

The implementation is based on the following assumptions:

* Product and box dimensions use the same units.
* Product and box weights use consistent units.
* Box costs are handled using decimal precision.
* Only active boxes are considered during selection.
* When multiple boxes are suitable, the documented cheapest-box rule is used to choose the recommendation.

## Possible Future Improvements

Some areas that could be improved in a production version include:

* Implementing a more advanced 3D bin-packing algorithm
* Adding authentication and permission management
* Moving from SQLite to PostgreSQL
* Adding OpenAPI/Swagger API documentation
* Containerizing the application with Docker
* Improving performance for orders containing a large number of products

## AI Usage

ChatGPT was used as a coding assistant during development. It helped with requirement analysis, implementation ideas, debugging, test-case suggestions, and documentation.

More details about how AI was used during development are available in `AI_USAGE.md`.
