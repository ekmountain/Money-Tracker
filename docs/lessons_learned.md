## Django MVT Pattern

| Layer | File | Responsibility |
|---|---|---|
| Model | `models.py` | Defines the data structure and database logic |
| View | `views.py` | Handles the business logic — what happens when a URL is visited |
| Template | `.html files` | What the user actually sees in the browser |


{% csrf_token %} is a Django security requirement for all forms — it prevents cross-site request forgery attacks

{% block title %} and {% block content %} are placeholders that child templates fill in