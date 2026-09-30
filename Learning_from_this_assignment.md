# Learnings from This Assignment

In this assignment, I gained experience in creating a Django REST API for a real-life problem and not only in tinkering around small features.

I have learned how to organize a Django project through models, serializers, views, URLs, and a separate service layer. I understand why business logic such as box selection needs to be separated from the views to make the code more manageable and testable.

Furthermore, I learned how to deal with related models like Order and OrderItem, calculate the quantity of products, and the total weight of the order. The box selection feature showed me that dimension verification becomes complicated if the products can be rotated.

Another important lesson I have learned is that there is a limit to multi-product packing. Checking each individual product against the box does not ensure that all of the products will fit together physically; therefore, a concrete packing algorithm is required.

During the coding process, I learned how to debug Django-related issues through looking into the actual error messages. I have fixed several errors such as serializer/model mismatch and incorrect decimal validation. Moreover, I learned how to utilize Postman to make JSON requests to API endpoints.
