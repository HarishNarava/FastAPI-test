# FastAPI Patient Management

Simple patient management system API built with FastAPI

## what it does
- patient management system with basic CRUD operations
- loads patient data from JSON file
- automatic API documentation

## run these in terminal
```bash
pip install -r requirements.txt

# and then

uvicorn main:app --reload
```

then go to http://127.0.0.1:8000 to see it work

## endpoints
- `/` - main API info
- `/about` - about the patient management system
- `/view` - view all patient records
- `/docs` - automatic API documentation

the patient data is stored in patients.json for now