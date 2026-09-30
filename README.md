# AI_Assisted_box_selection_system 

A Django REST API that recommends a suitable shipping box for an ecommerce order based on product dimensions, quantity, total weight, box capacity, and cost.

#  Features

1. Product and box management
2. Orders with multiple products and quantities
3. Product rotation support
4. Weight-capacity validation
5. Dedicated box-selection service layer
6. Cheapest suitable box selection
7. REST API with Django REST Framework
8. Automated test support

# Tech Stack

1. Python
2. Django
3. Django REST Framework.
4. SQLite

# Project Structure

box_selection_project/
├── manage.py
├── requirements.txt
├── config/
├── box_selection/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services/
│   │   └── box_selector.py
│   └── tests/
├── README.md
├── AI_USAGE.md
└── CHAT_TRANSCRIPT.md

# Installation
mkdir box_selection_project
cd box_selection_project

# Virual Enviroment

python -m venv venv
venv\Scripts\activate  (For Wndows)

# Install dependencies:

pip install django djangorestframework
pip install -r requirements.txt

# Create Project:

django-admin startproject config .
python manage.py startapp box_selection

# Run migrations:

python manage.py makemigrations
python manage.py migrate

# Run server:

python manage.py runserver

# APIs
POST - /api/products/ (Create product)
GET - /api/products/ (List products)
POST - /api/boxes/ (Create box)
GET - /api/boxes/ (List boxes)
POST - /api/orders/ (Create order0
GET - /api/orders/ (List orders)
GET - /api/orders/<id>/recommended-box/ (Get recommended box)

# Box Selection
1. The selection service:
2. Calculates total order weight.
3. Checks box weight capacity.
4. Checks product dimensions.
5. Supports valid product rotations.
6. Evaluates candidate boxes.
7. Selects the cheapest suitable box.

# Testing

python manage.py test

For detailed output:
python manage.py test -v 2
