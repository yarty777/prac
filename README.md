# EduSystem

EduSystem is a backend application for managing educational tests.
The system allows users to register, authenticate, take tests, and store their results.

---

## Authors

* **Dmytruk Ivan** (EzX_Anub1s) — Backend developer
* **Onyshchuk Oleksandra** — Backend developer

---

## Technologies Used

* Python
* FastAPI
* MongoDB
* Swagger (OpenAPI)

---

## Functional Features

* User registration
* Authentication and authorization (JWT)
* Creating tests
* Taking tests
* Updating and deleting tests
* Viewing test results
* Saving test results

---

## Team Contribution

### Dmytruk Ivan (EzX_Anub1s)

* FastAPI project base setup
* User model implementation
* Result model implementation
* CRUD operations for results
* Authentication endpoints (`/register`, `/login`)
* Pagination for tests
* Endpoint for retrieving questions by test
* Integration testing:

  * Full system integration tests
  * Integration tests with fake database

### Onyshchuk Oleksandra

* Quiz model implementation
* Question model implementation
* CRUD endpoints for quizzes:

  * `GET /quizzes`
  * `GET /quizzes/{id}`
  * `POST /quizzes`
  * `PUT /quizzes/{id}`
  * `DELETE /quizzes/{id}`

---

## Requirements

```txt
fastapi
uvicorn
pymongo
python-dotenv
python-jose
passlib[bcrypt]

pytest
pytest-asyncio
httpx
```

---

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
```

2. Create and activate virtual environment:

```bash
python -m venv venv
.\venv\Scripts\Activate   # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

---

## API Documentation

Swagger UI (OpenAPI) is available at:

```
http://127.0.0.1:8000/docs
```

---

## Testing

Integration tests are located in the `tests/integration` folder.

Run full system integration tests:

```bash
python -m pytest tests/integration/test_full_system.py -v
```

Run integration tests with fake database:

```bash
python -m pytest tests/integration/integration_database.py -v
```
