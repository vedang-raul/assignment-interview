# FastAPI RBAC Task Manager

A scalable, full-stack REST API built with **FastAPI** and **MongoDB**, featuring secure JWT Authentication, Role-Based Access Control (RBAC), and a lightweight Vanilla JS frontend.

Designed as a modular, containerized application ready for horizontal scaling.

## 🚀 Features

* **Authentication:** Secure User Registration & Login with Password Hashing (`bcrypt`) and JWT generation.
* **Role-Based Access Control (RBAC):**
    * **Admins:** Can Create, Read, Update, and Delete any task.
    * **Users:** Can only View tasks and mark them as "Completed".
* **Database:** Asynchronous MongoDB integration using `Motor`.
* **Frontend:** A lightweight, single-page interface built with Vanilla JS (No heavy framework overhead).
* **Documentation:** Auto-generated Interactive API Docs (Swagger UI).
* **Deployment:** Fully containerized with Docker.

## 🛠️ Tech Stack

* **Backend:** Python 3.11, FastAPI, Uvicorn
* **Database:** MongoDB (Atlas or Local)
* **Validation:** Pydantic
* **Security:** Python-Jose (JWT), Passlib (Hashing)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript

---

## ⚙️ Installation & Running


### Option 1: Render (Recomended)

**https://assignment-interview.onrender.com**


### Option 2: Docker 
The easiest way to run the application is via Docker, ensuring a consistent environment.

1.  **Build the Image:**
    ```bash
    docker build -t assignment-app .
    ```

2.  **Run the Container:**
    ```bash
    docker run -p 8000:8000 assignment-app
    ```

### Option 3: Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <folder-name>
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration:**
    Create a `.env` file in the root directory:
    ```env
    MONGO_URL=mongodb+srv://<your_connection_string>
    DB_NAME=assignment
    SECRET_KEY=winter_is_coming
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ADMIN_CODE=YouKnowNothingJonSnow
    ```

5.  **Run the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```

---

## 📖 API Documentation

Once the server is running, access the full interactive API documentation (Swagger UI) at:

👉 **http://localhost:8000/docs**

This interface allows you to test all endpoints (`POST /register`, `POST /login`, `GET /tasks`, etc.) directly from the browser.

---

## 🧪 Usage Guide

### Admin Access
To test Admin privileges (Create/Delete tasks), use the following code during registration in the "Admin Code" field:
> **Code:** `YouKnowNothingJonSnow`

### Standard Flow
1.  Navigate to `http://localhost:8000/`.
2.  Register a new user.
3.  Login to access the Dashboard.
4.  The UI will automatically adapt based on your Role (Admin/User).

---

## 📈 Scalability Note
*Required Deliverable #5*

This architecture was designed with the "Microservices First" mindset to ensure scalability under high load:

1.  **Stateless Authentication:** The application uses **JWT (JSON Web Tokens)** for authentication. This is stateless, meaning the server does not need to store session data. This allows the application to be easily load-balanced across multiple server instances without "sticky sessions."
2.  **Containerization:** The application is fully **Dockerized**. This makes it orchestration-ready (e.g., Kubernetes), allowing for automated horizontal scaling (spinning up more containers) based on traffic spikes.
3.  **Asynchronous I/O:** By utilizing **FastAPI** and **Motor (Async MongoDB driver)**, the application handles I/O-bound operations non-blocking. This allows a single worker to handle significantly more concurrent requests compared to traditional synchronous frameworks (like Flask/Django).
4.  **Modular Structure:** The codebase is strictly separated into `routes`, `models`, `core`, and `db`. In a production scenario, the "Auth" module could be easily decoupled into its own microservice independent of the "Tasks" module.

---
