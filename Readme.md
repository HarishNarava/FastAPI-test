# FastAPI Patient Management

Simple patient management system API built with FastAPI and Pydantic

## what it does
- full CRUD operations for patient records
- loads patient data from JSON file
- view individual patient records by ID
- sort patients by various criteria
- create new patient records with validation
- update existing patient records (partial updates supported)
- delete patient records
- automatic BMI calculation and health verdict
- data validation using Pydantic models

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
- `/patient/{patient_id}` - get specific patient by ID (e.g., `/patient/P002`)
- `/sort` - sort patients by age, weight, height, or bmi with asc/desc order
- `/create` - create new patient record (POST request)
- `/edit/{patient_id}` - update patient record (PUT request, partial updates allowed)
- `/delete/{patient_id}` - delete patient record (DELETE request)
- `/docs` - automatic API documentation

## example usage
- View patient P002: `/patient/P002`
- Sort by age descending: `/sort?sort_by=age&order=desc`
- Create patient: POST to `/create` with patient data
- Update patient: PUT to `/edit/P002` with fields to update
- Delete patient: DELETE to `/delete/P002`

## patient data includes
- automatic BMI calculation
- health verdict (underweight, normal, overweight, obesity)
- input validation for age, height, weight, gender
- partial updates (only update specific fields)

the patient data is stored in patients.json and uses utils.py for data operations

the sample patient data is stored in patients.json for now