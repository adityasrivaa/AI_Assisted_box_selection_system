# AI_USAGE.md

# AI-Assisted Box Selection System — AI Usage

## 1. Purpose

This project was developed with the assistance of ChatGPT as an AI coding and development assistant.

AI assistance was used for:

- Understanding and breaking down the assignment requirements
- Designing the Django application architecture
- Discussing the box-selection algorithm
- Writing and reviewing Django code
- Troubleshooting errors encountered during development
- Explaining API testing and debugging steps
- Identifying edge cases and potential implementation weaknesses
- Preparing development documentation

The generated code was reviewed incrementally during development rather than being accepted without verification.

---

## 2. AI Tool Used

### ChatGPT

ChatGPT was used as an AI coding assistant during development.

The AI was used for:

- Requirement analysis
- Architecture discussion
- Django implementation guidance
- REST API implementation
- Debugging
- Code review
- Test planning
- Documentation assistance

---

## 3. Actual Prompts Used

The main development prompt provided to ChatGPT described the assignment:

> I am working on a Python/Django hiring assignment titled “AI-Assisted Box Selection System.”

The prompt provided the assignment requirements, including:

- Product, Box, Order, and OrderItem models
- Product quantities
- Box-selection service layer
- Product rotation
- Weight-capacity validation
- Multi-product packing limitations
- Django REST Framework API
- Automated testing
- Project structure
- README requirements
- AI usage documentation requirements
- Code-review and verification requirements

The prompt also explicitly requested a step-by-step development process rather than immediately generating the entire project.

During implementation, additional prompts were used to troubleshoot the running project and continue development based on actual errors shown in screenshots.

Examples included:

- Asking what to do after the Django server was running.
- Providing screenshots of Django errors and asking how to fix them.
- Showing the Product API serializer error involving `created_at`.
- Showing a validation error caused by the `weight` field allowing only two decimal places.
- Showing the Orders API and asking how to create an order.
- Showing a Postman request error and asking how to correct it.

---

## 4. Development Assistance Received

### Requirement Analysis

The assignment requirements were broken into separate areas:

1. Requirements and ambiguities
2. Assumptions and business rules
3. Database models
4. Box-selection algorithm
5. Packing strategy
6. Project structure
7. Django models
8. Box-selection service
9. Serializers and API endpoints
10. Automated tests
11. Code review
12. Installation and execution commands

### Box Selection

The proposed design separates the box-selection business logic from views and serializers.

The service is responsible for:

- Calculating total order weight
- Considering product quantities
- Checking box weight capacity
- Checking product dimensions
- Considering rotations
- Evaluating candidate boxes
- Selecting a suitable box according to the defined business rule
- Handling cases where no box can accommodate the order

A major limitation was also identified: checking every product independently against a box does not prove that multiple products can physically be packed together.

A small-assignment-friendly heuristic was therefore discussed instead of silently claiming to implement a complete 3D bin-packing algorithm.

---

## 5. Actual Errors Found During Development

The following issues were actually encountered during development.

### 5.1 Root URL Returned 404

Initially, opening:

```text
http://127.0.0.1:8000/
```

returned a Django 404 page.

Django showed that the configured routes were:

```text
admin/
api/
```

The issue was that no route had been defined for the empty path `/`.

A simple API home endpoint was suggested:

```python
def home(request):
    return JsonResponse({
        "message": "AI-Assisted Box Selection System API",
        "api": "/api/",
        "admin": "/admin/",
    })
```

This was a routing issue rather than a server startup issue.

---

### 5.2 Invalid `created_at` Serializer Field

When accessing:

```text
/api/products/
```

Django returned:

```text
ImproperlyConfigured

Field name 'created_at' is not valid for model 'Product'
```

The problem was a mismatch between the actual `Product` model and `ProductSerializer`.

The serializer referenced:

```text
created_at
```

even though the actual model did not contain that field.

The serializer was corrected by removing `created_at` from its fields and `read_only_fields`.

This demonstrated the importance of keeping serializers synchronized with the actual Django models.

---

### 5.3 Weight Decimal Validation Error

When creating a product, the following value was initially entered:

```text
1.500
```

The API returned:

```text
Ensure that there are no more than 2 decimal places.
```

The existing model configuration allowed two decimal places.

The value was therefore changed to:

```text
1.50
```

This matched the existing model validation.

No unnecessary database migration was introduced for this issue.

---

### 5.4 DRF HTML Form Limitation for Nested Order Items

The Orders API displayed:

```text
Lists are not currently supported in HTML input.
```

The Order API uses a nested `items` list, so the Django REST Framework browsable API cannot conveniently create this particular request using its normal HTML form.

The order was therefore prepared as JSON using an API client such as Postman.

Example request:

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

---

### 5.5 Postman Invalid Protocol Error

While creating an order in Postman, the request initially failed with:

```text
Error: Invalid protocol: post http:
```

The issue was that `POST` had accidentally been included in the URL field.

The correct Postman configuration was:

```text
Method:
POST
```

and:

```text
URL:
http://127.0.0.1:8000/api/orders/
```

rather than:

```text
POST http://127.0.0.1:8000/api/orders/
```

The JSON request body itself was correctly structured.

---

## 6. Changes Made During Development

The following changes were made based on the actual development issues encountered:

- Added/adjusted handling for the root `/` URL.
- Corrected the Product serializer so it matched the actual Product model.
- Removed the unsupported `created_at` field from the Product serializer.
- Used two decimal places for product weight because that matched the existing model validation.
- Used JSON/API-client requests for creating orders containing nested order items.
- Corrected the Postman method/URL configuration.

---

## 7. Outputs Rejected or Corrected

AI-generated code and suggestions were not automatically treated as correct.

One concrete example was the initial assumption that the Product model contained a `created_at` field.

The running application demonstrated that this assumption was incorrect:

```text
Field name 'created_at' is not valid for model 'Product'
```

The serializer was then corrected to match the actual model.

Another example was the initial use of:

```text
1.500
```

for product weight. The actual API validation showed that the existing model allowed only two decimal places, so:

```text
1.50
```

was used instead.

The Postman URL configuration was also corrected after the actual request produced an invalid protocol error.

---

## 8. Verification Performed

Verification was performed incrementally through the running Django development server.

### Django Server

The Django development server was successfully running at:

```text
http://127.0.0.1:8000/
```

### Product API

The Product API successfully loaded after correcting the serializer/model mismatch:

```text
GET /api/products/
```

The API also performed validation on the product weight field.

### Orders API

The Orders API successfully loaded:

```text
GET /api/orders/
```

and initially returned:

```json
[]
```

indicating that no orders had yet been created.

### API Client

Postman was used to prepare an order creation request.

The request body was:

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

The first Postman attempt failed because of an incorrectly configured URL. This was identified from the actual Postman error.

---

## 9. Testing Status

The development screenshots and conversation so far verify portions of the API manually.

This document does **not** claim that the complete automated test suite has been executed.

The following command should be run when the implementation is ready:

```bash
python manage.py test -v 2
```

If the test suite is executed later, the actual output should be recorded in `TEST_OUTPUT.md`.

Do not add a claim such as "all tests passed" unless the command has actually been executed and verified.

---

## 10. Important AI-Assisted Development Principle

AI-generated code was treated as development assistance rather than unquestioned final code.

The implementation was checked against:

- The actual Django project
- Django error messages
- API responses
- Validation behavior
- Postman request behavior
- Assignment requirements

When an AI-generated assumption did not match the actual project, the implementation was corrected based on the observed behavior.

---

## 11. Personal Learning Section

This section should be written by the project author and should **not be generated by AI**.

The following questions can be used to write it:

1. What did I learn about separating business logic from Django views?
2. What did I learn about Django models and relationships?
3. What did I learn about Django REST Framework serializers?
4. What did I learn about handling nested Order and OrderItem data?
5. How did I implement product rotation?
6. Why is multi-product 3D packing more complicated than comparing individual dimensions?
7. What bugs did I encounter during development?
8. How did I debug those bugs?
9. What did I learn from using Postman?
10. What would I improve if I had more time?

The final answers should describe my actual experience rather than AI-generated experiences.

---

## 12. Summary

ChatGPT was used throughout development as a coding assistant for requirement analysis, architecture discussion, implementation guidance, debugging, API testing guidance, and code review.

The development process remained iterative. Actual application behavior was used to identify and correct mismatches between generated suggestions and the project's implementation.

No fabricated AI usage history, test results, personal learning statements, or exported ChatGPT transcript is included in this document.
