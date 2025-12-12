from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

from utils import load_data, save_data

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', examples= ['P001', 'P002'])]
    name: Annotated[str, Field(..., description= 'Name of the patient')]
    city: Annotated[str, Field(..., description= 'City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description= 'Age of the patient in years')]
    gender: Annotated[str, Literal['male', 'female' 'others'], Field(..., description= 'Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in KGs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal Weight'
        elif self.bmi <30:
            return 'Overweight'
        else:
            return "Obesity"

class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[str], Literal['male', 'female' 'others'], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'Fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient in the DB", example='P002')):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., descrption = 'Sort on the basis of age, weight, height, or bmi'), order: str =Query('asc', description = 'sort in ascending or descending order')):
    valid_feilds =['wight', 'height', 'bmi', 'age']

    if sort_by not in valid_feilds:
        raise HTTPException(status_code = 400, detail=f'Invalid sort field. Choose from {valid_feilds}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code= 400, detail ='Invalid order. Choose "asc" or "desc"')
    
    data= load_data()

    sort_order= True if order =='desc' else False

    sorted_data = sorted(data.values(), key = lambda x:x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    data=load_data()

    # check if patient with same ID already exists
    if patient.id in data:
        raise HTTPException(status_code = 400, detail= 'Patient with this ID already exists')
    
    # add new patient to database
    data[patient.id]= patient.model_dump(exclude=['id'])

    # save into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient record created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update: PatientUpdate):
    
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key]= value

    # existing_patient_info -> pydantic object -> updated bmi + verdict    
    existing_patient_info['id']= patient_id
    patient_pydantic_object= Patient(**existing_patient_info)

    # -> pydantic object -> dict excluding id
    existing_patient_info = patient_pydantic_object.model_dump(exclude=['id'])

    # add this dict to data
    data[patient_id]= existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient record updated successfully'})


@app.delete('/delete/{pateint_id}')
def delete_patient(patient_id: str):
    #load data
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient record deleted successfully'})
