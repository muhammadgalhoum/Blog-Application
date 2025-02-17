# Building a Blog Application

This repository contains the first project from the "Django 5 by Example" book, along with my enhancements. I've added new features and optimized tasks to ensure the best approach. I will continue to improve it by adding new features and making necessary enhancements.

## Project Setup

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/muhammadgalhoum/Blog-Application.git
```

### 2. Create a Virtual Environment

Create a virtual environment to isolate the dependencies:

```bash
On macOS/Linux:
python3 -m venv venv
On Windows:
python -m venv venv
```

### 3. Activate the Virtual Environment

```bash
On macOS/Linux:
source venv/bin/activate
On Windows:
.\venv\Scripts\activate
```

### 4. Install the Required Dependencies

Install the required dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

Run migrations to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin Access)

Create a superuser to access the Django Admin interface:

```bash
python manage.py createsuperuser
You will be prompted to enter a username, email, and password for the superuser account.
```

### 7. Run the Development Server

Start the development server:

```bash
python manage.py runserver
The server will be available at http://127.0.0.1:8000/
```

### Important Note

Create a .env file in the main directory of the project and add the following variables with their respective values:

```bash
EMAIL_HOST_USER=youremail@example.com
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL="My Blog <youremail@example.com>"
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
```
