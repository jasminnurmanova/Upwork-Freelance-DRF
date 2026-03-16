# Upwork Clone API

## Project Description

This project is a backend REST API for an Upwork-like freelancing platform.
Clients can create projects and freelancers can submit bids for those projects.
Clients can review bids, accept or reject them, and when a bid is accepted a contract is automatically created between the client and freelancer.

The API includes authentication, project management, bidding system, and contract management.

---

## Technologies Used

* Python
* Django
* Django REST Framework (DRF)
* JWT Authentication (SimpleJWT)
* PostgreSQL / SQLite
* Swagger (drf-yasg)
* Postman

---

## API Endpoints

### Authentication

POST /auth/register/
POST /auth/login/

### Projects

POST /projects/create/
PATCH /projects/{id}/update/
DELETE /projects/{id}/delete/
GET /my-projects/
GET /projects/{id}/

### Freelancer

GET /projects/
POST /projects/{id}/bid/
GET /my-bids/
GET /bids/{id}/

### Client

GET /projects/{project_id}/bids/
GET /client/bids/
POST /bids/{bid_id}/accept/
POST /bids/{bid_id}/reject/

### Contracts

GET /contracts/
GET /contracts/{contract_id}/

---

## Swagger Documentation

http://127.0.0.1:8000/swagger/

---

## Postman Documentation

POSTMAN: https://documenter.getpostman.com/view/51287189/2sBXigNEGX

---

## Test Users

### Client

username: client1
password: client123

### Freelancer

username: freelancer1
password: freelancer123

---

## How to Run the Project

1. Clone the repository

```
https://github.com/jasminnurmanova/Upwork-Freelance-DRF.git```

2. Go to project directory

```
cd upwork-api
```

3. Create virtual environment

```
python -m venv venv
```

4. Activate virtual environment

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

5. Install dependencies

```
pip install -r requirements.txt
```

6. Apply migrations

```
python manage.py migrate
```

7. Run the server

```
python manage.py runserver
```

8. Open Swagger documentation

```
http://127.0.0.1:8000/swagger/
```


