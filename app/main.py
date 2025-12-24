from fastapi import FastAPI, HTTPException, status
from schemas_api import Contact
import uvicorn
from db_manager import DBContactsManager
import os


# name of database. from env.
DATABASE = os.getenv('DB_NAME','contacts_db')

TABLE_NAME = 'contacts'


app = FastAPI()

db = DBContactsManager(database_name=DATABASE)

@app.get('/contacts')
def get_all_contacts():
    try:
        contacts =  db.database.get_all(TABLE_NAME)
        if not contacts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no contacts")
        return contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


@app.post('/contacts')
def create_contact(contact:Contact):
    try:
        contact_py = contact.model_dump()
        new_id = db.database.create_contact(TABLE_NAME, contact_py)
        return {'message':"Contact created successfully",
                'id':new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not create contact: {str(e)}")

@app.put('/contacts/{id_contact}')
def update_contact(id_contact:int, new_info:Contact):
    contact = new_info.model_dump()
    if db.database.update_record(TABLE_NAME, id_contact, contact):
        return {"status": "update"}
    else:
        return {"status":"error"}    



@app.delete('/contacts/{id_contact}')
def delete_contact(id_contact:int):
    
    if db.database.delete_record(TABLE_NAME, id_contact):
        return {"status": "deleted"}
    else:
        return {"status":"error"}    
    