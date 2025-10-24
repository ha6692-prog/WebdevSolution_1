# DataX2 Django Project

## Setup

1. Create a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Development Server

1. Apply migrations:
   ```powershell
   python manage.py migrate
   ```

2. Start the server:
   ```powershell
   python manage.py runserver
   ```

Access the server at `http://127.0.0.1:8000/`.