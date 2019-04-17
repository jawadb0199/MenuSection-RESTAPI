# MenuSection-RESTAPI

Menu Section REST API. Implemented using Python, Flask, SQLite, SQLAlchemy, and Marshmallow. The API runs through local-host (127.0.0.1) on port number 5000.

API Functions

1. Add a new menu section (POST)
    - /menusection Request Body: {'name': "menu section"}
2. Get all menu sections (GET) 
    - /menusection
3. Get menu section by id (GET)
    - /menusection/<id:int>
4. Update menu section by id (POST)
    - /menusection/<id:int>
    - Request Body: {'name': "menu section"}
5. Delete menu section by id (Delete)
    - /menusection/<id:int>
