#  TO RUN BACKEND AND FRONTEND ( Chapter Generator ) 

### About : AI Powered Chapter Generator From Given Sets Of Contents and Guidelines

```
For Backend and Frontend : git clone https://github.com/nebulaanish/chapter_generator.git
```
```
( For Backend )

cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

```

Set Your Own Credentials For Backend

POSTGRES_DB_NAME = 
POSTGRES_USER = 
POSTGRES_PASSWORD = 
POSTGRES_PORT = 5432 
POSTGRES_HOST = 127.0.0.1
GEMINI_API_KEY = 
SECRET_KEY=


```

```
( For Frontend )

cd frontend
npm install
npm run dev

```
