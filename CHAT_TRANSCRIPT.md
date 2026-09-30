# AI-Assisted Box Selection System — Chat Transcript

### User

I’m working on a Python/Django hiring assignment called **AI-Assisted Box Selection System**. The system needs to manage Products, Boxes, Orders, and OrderItems. I also need a separate service for selecting the right box, support for rotating products while checking fit, quantity and weight handling, REST APIs, automated tests, documentation, and a code review.

### Assistant

We divided the assignment into smaller parts, including understanding the requirements, making assumptions, designing the database models, implementing the box-fitting logic, handling packing limitations, setting up the Django project structure, building the APIs, writing tests, and verifying the overall implementation.

### User

When I open the Django root URL, I’m getting a 404 error.

### Assistant

The issue was that the `/` URL had not been configured. The project already had routes such as `/admin/` and `/api/`, but there was no endpoint for the root URL. I suggested either adding a simple root endpoint or using the available API URLs directly.

### User

When I try to use the Product API, I get this error:

`Field name 'created_at' is not valid for model 'Product'.`

### Assistant

This happens when the serializer contains a field that doesn’t exist in the corresponding Django model. I recommended checking the `ProductSerializer` and removing `created_at` if that field isn’t defined in the `Product` model.

### User

When I create a product, the API rejects the weight value `1.500`.

### Assistant

The problem is related to the number of decimal places allowed by the `DecimalField`. The current field configuration supports two decimal places, so the value should be entered as `1.50` instead of `1.500`.

### User

The Orders API gives me this error:

`Lists are not currently supported in HTML input.`

### Assistant

This is a limitation of Django REST Framework’s browsable API when working with nested list data such as order items. I recommended using Postman or another API client and sending the request as JSON.

For example:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    }
  ]
}
```

### User

Postman is showing this error:

`Error: Invalid protocol: post http:`

### Assistant

The problem was that `POST` had been entered as part of the URL instead of being selected as the HTTP method.

The correct Postman configuration is:

* **Method:** `POST`
* **URL:** `http://127.0.0.1:8000/api/orders/`

### Development Principle

Throughout the development process, the suggestions were checked against the actual Django errors, API responses, and behavior of the project. The goal was to keep the transcript based on real development issues and solutions rather than claiming test results, learning experiences, or official exported transcripts that did not actually happen.
