Admin Chatbot :

A natural-language admin chatbot that allows logged-in admins to add, remove, and update system users through chat commands.

Built as a technical assignment for WP Brigade (Sialkot) for the Data Scientist / ML role.

Overview :

Admins can manage users without traditional forms by simply typing commands such as:

can you add the user "john.smith@xyz.com" with phone number "+92332"
can you remove the user "john.smith@xyz.com"
can you update samanthas city to Cordoba

The chatbot classifies the user's intent, extracts the required information, performs the database operation, and returns a clear response.

Tools and Technologies :

- Python - Core development and ML logic
- Django 4.2 - Backend and web application
- scikit-learn - Intent classification
- TF-IDF - Text vectorization
- Multinomial Naive Bayes - Intent prediction
- Regex (re) - Entity extraction
- SQLite - Database
- Django Templates - Frontend structure
- HTML & CSS - User interface
- JavaScript Fetch API - Chat communication
- Joblib - Model and vectorizer persistence
- Django Admin - Database/user management

How its works :

User command -> JavaScript Fetch API  ->  Django view  ->  Intent classification  ->  Entity extraction   ->  CRUD operation  ->  JSON response ->  Chat response

The model supports four intents:

- add_user
- remove_user
- update_user
- unknown

The intent classifier uses TF-IDF with unigrams and bigrams and Multinomial Naive Bayes. The model is evaluated on an 80/20 split and then retrained on the complete dataset before being saved with Joblib.

Regex-based extraction handles emails, phone numbers, names, fields, and update values.

CRUD handlers perform the corresponding SystemUser database operations and handle duplicate or missing users without crashing.

SQL Lite usage :

- SQLite: Used to keep the assignment simple and easy to run without additional database configuration.

- Regex: Used for structured entity extraction because emails, phone numbers, and update patterns are predictable.
- Name-based updates: Supported because the assignment's update example does not provide an email.
- Confidence threshold: Low-confidence predictions fall back to a clarification response instead of performing an uncertain operation.
- No chat history: Messages are currently displayed for the active session but are not stored in the database.
