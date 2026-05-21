# News App — Django Capstone Project

A Django-based news platform with role-based access control (reader, editor,
journalist), article publishing/approval workflows, newsletters, and a REST API.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install Dependencies (virtualenv)](#install-dependencies-virtualenv)
3. [Configure Environment](#configure-environment)
4. [Run Migrations](#run-migrations)
5. [Run with Virtualenv](#run-with-virtualenv)
6. [Run with Docker](#run-with-docker)
7. [Sphinx Documentation](#sphinx-documentation)
8. [Git Branches](#git-branches)

---

## Prerequisites

- Python **3.13** (or any 3.10+ compatible version)
- **pip** or **pip3**
- **Docker** (optional, for containerised deployment)

---

## Install Dependencies (virtualenv)

```bash
# Create a virtual environment (run once)
python -m venv venv

# Activate the virtual environment
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On Windows (Command Prompt):
venv\Scripts\activate.bat
# On macOS / Linux:
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

> **Note:** `requirements.txt` is included in this repository. Install it while
> your virtual environment is activated.

---

## Configure Environment

Before running the application, you **must** add the required secrets to
`news_app/settings.py`. The placeholder values are:

```python
SECRET_KEY = 'django-insecure-...'          # Replace with your own secret key
EMAIL_HOST_USER = 'your-email@gmail.com'     # Replace with your email
EMAIL_HOST_PASSWORD = 'your-password'        # Replace with your email password
```

> **Important:** Never commit real credentials to a public repository. The
> `.gitignore` file excludes `settings.py` if it contains your secrets. Use
> environment variables or a `.env` file in production.

---

## Run Migrations

```bash
python manage.py migrate
```

---

## Run with Virtualenv

```bash
# Make sure the virtual environment is activated first (see above)
python manage.py runserver
```

The development server starts at **http://127.0.0.1:8000/**

---

## Run with Docker

```bash
# Build the Docker image
docker build -t news-app .

# Run the container
docker run -p 8000:8000 news-app
```

The container automatically runs `python manage.py migrate` then starts the
development server on **http://localhost:8000/**

> **Note:** You still need to update `SECRET_KEY`, `EMAIL_HOST_USER`, and
> `EMAIL_HOST_PASSWORD` in `news_app/settings.py` inside the container (or pass
> them as environment variables).

---

## Sphinx Documentation

Auto-generated API documentation is stored in the `docs/` folder.

```bash
cd docs
sphinx-build -b html . _build/html
```

Open `docs/_build/html/index.html` in a browser to view the documentation.

---

## Git Branches

| Branch         | Purpose                                    |
|----------------|--------------------------------------------|
| `master`       | Main application code (merged target)      |
| `docs`         | Sphinx documentation and docstring changes |
| `container`    | Dockerfile and containerisation changes    |
