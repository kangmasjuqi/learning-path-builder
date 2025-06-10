# Interactive Learning Path Builder

## Project Overview

Welcome to the **Interactive Learning Path Builder**, a full-stack EdTech platform designed to empower educators to create dynamic and engaging learning experiences. This project aims to provide a robust backend for managing courses, lessons, quizzes, and student progress, laying the groundwork for a rich, interactive frontend.

The core idea is to build a platform where educators can craft personalized learning paths comprising various content types (articles, videos, quizzes). Students can then navigate these paths, track their completion, and receive immediate feedback on their progress and quiz performance.

This project directly addresses several key requirements, including a **tutoring platform**, a comprehensive **learning experience**, a foundation for a **responsive and interactive UI**, a **Python backend** (using FastAPI), and a strong **RDBMS** (PostgreSQL) with **API integration**.

### Key Features (Backend Implemented)

* **User Authentication & Authorization:** Secure JWT-based registration and login system with distinct **Student** and **Educator** roles.
* **Course Management:** Educators can create, read, update, and delete courses.
* **Lesson Management:** Educators can add, organize, and manage lessons within courses, supporting various content types (text, video, quiz, external links).
* **Quiz & Question System:** Educators can build multiple-choice quizzes, adding questions and defining correct answers.
* **Student Progress Tracking:** Students can mark lessons as complete, and the system records their progress.
* **Quiz Answer Submission & Grading:** Students can submit answers to quiz questions, with automatic grading for multiple-choice questions.
* **Database Management:** Robust PostgreSQL database schema managed via **SQLAlchemy** and **Alembic migrations** for smooth schema evolution.
* **RESTful API:** A well-structured API built with **FastAPI**, featuring automatic interactive documentation (Swagger UI).

---

## Technologies Used

### Backend

* **Python 3.12.2:** The primary programming language.
* **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
* **PostgreSQL:** A powerful, open-source relational database system chosen for its robustness and data integrity.
* **SQLAlchemy 2.0:** Python SQL Toolkit and Object Relational Mapper (ORM) for efficient database interaction.
* **Alembic:** Database migration tool for SQLAlchemy, ensuring seamless schema updates.
* **JWT (JSON Web Tokens):** For secure, stateless authentication.
* **Bcrypt:** For strong password hashing.
* **Pydantic:** Data validation and settings management using Python type hints.

### Frontend (Planned)

* **Next.js (React):** For building the interactive user interface, leveraging SSR/SSG for performance.
* **Redux Toolkit:** For robust client-side state management.
* **Tailwind CSS:** For efficient and highly customizable styling.

---

## Getting Started

Follow these steps to set up and run the backend of the Interactive Learning Path Builder on your local machine.

### Prerequisites

* **Python 3.12.2**
* **Node.js (v18.x.x recommended)** & **npm (v9.x.x recommended)** (needed for frontend setup later)
* **PostgreSQL:** A running PostgreSQL instance.
    * Make sure you have a database created (e.g., `learning_path_db`) and a user with access to it.

### Backend Setup

1.  **Clone the repository:**

    ```bash
    git clone git@github.com:kangmasjuqi/learning-path-builder.git
    cd learning-path-builder
    ```

2.  **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

3.  **Create and activate a Python virtual environment:**

    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

4.  **Install backend dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables:**

    Create a `.env` file in the `backend/` directory with your PostgreSQL connection string and a secret key.

    ```ini
    # backend/.env
    DATABASE_URL="postgresql://user:password@localhost:5432/learning_path_db"
    SECRET_KEY="YOUR_SUPER_SECURE_RANDOM_KEY_HERE" # <<< IMPORTANT: CHANGE THIS!
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_DAYS=7
    ```

    * **Replace `user`, `password`, and `learning_path_db`** with your actual PostgreSQL credentials.
    * **Generate a strong `SECRET_KEY`**. You can do this in Python: `python -c "import os; print(os.urandom(32).hex())"`

6.  **Run Database Migrations:**

    This will create all the necessary tables in your PostgreSQL database.

    ```bash
    alembic init alembic # If not already done in the project root
    # IMPORTANT: Ensure backend/alembic/env.py is configured to use your .env.
    # (Refer to the specific setup steps for env.py if you encountered issues during implementation)
    alembic revision --autogenerate -m "Create initial tables"
    alembic upgrade head
    ```

7.  **Run the FastAPI application:**

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

    The backend API will now be running at `http://localhost:8000`.

---

## API Documentation

Once the backend is running, you can access the interactive API documentation (Swagger UI) at:
[http://localhost:8000/docs](http://localhost:8000/docs)

This interface allows you to explore all available endpoints, test requests, and understand the expected request/response formats.

---

## Future Enhancements (Frontend Coming Soon!)

The next phase of this project will focus on developing a dynamic and user-friendly frontend using Next.js. Key features to be implemented include:

* User registration and login forms.
* Student and Educator dashboards.
* Interactive course listings and detailed course pages.
* Lesson content display (text, video).
* Interactive quiz components and submission flow.
* Student progress tracking and visualization.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---