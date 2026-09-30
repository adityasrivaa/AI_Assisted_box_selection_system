# AI Usage

## AI Tool Used

I used **ChatGPT** as an AI coding assistant during the development of this project.

## How AI Was Used

ChatGPT was mainly used to support the development process in the following areas:

* Understanding the assignment requirements and identifying the necessary assumptions.
* Planning the Django project structure, including models, serializers, APIs, and the service layer.
* Designing the box-selection logic, including product rotation and checking whether products fit inside a box.
* Debugging issues encountered while working with Django and Postman.
* Identifying useful test cases and reviewing the implementation for possible issues.
* Preparing and improving the project documentation.

## Examples of Actual Debugging

Some of the issues where AI assistance was used during development include:

* Fixing the missing `/` route that caused a 404 error on the Django root URL.
* Resolving a mismatch between the `Product` model and serializer involving the `created_at` field.
* Correcting the product weight input from `1.500` to `1.50` based on the validation error returned by the API.
* Fixing an incorrect Postman URL configuration that caused the `Invalid protocol: post http:` error.

## Verification

The suggestions provided by ChatGPT were not accepted blindly. They were checked against the actual Django application, API responses, and observed project behavior. Changes were tested and adjusted whenever necessary.

## Important Note

This document describes the actual ways AI assistance was used during the development of the project. It does not include fabricated test results, personal learning claims, or a made-up ChatGPT transcript.

The **“What did you learn?”** section will be written separately by the project author based on their own experience while building the project.
