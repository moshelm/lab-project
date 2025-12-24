from fastapi import FastAPI, HTTPException, status
from schemas_api import Contact
import uvicorn
from db_manager import DBContactsManager
from pathlib import Path


current_file = Path(__file__).resolve()
sql_path = current_file.parent.parent / "sql" / "init.sql"

DATABASE = 'contacts_db'
TABLE_NAME = 'contacts'

INITIALIZE_SQL = sql_path



app = FastAPI()

db = DBContactsManager(file_name=INITIALIZE_SQL)

@app.get('/contacts')
def get_all_contacts():
    
    contacts =  db.database.get_all(TABLE_NAME)
    
    
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no contacts"
        )
    else:
        return contacts

@app.post('/contacts')
def create_contact(contact:Contact):
    d_contact = contact.model_dump()
    new_id = db.database.create_contact(TABLE_NAME, d_contact)
    return {'message':"Contact created successfully",
            'id':new_id}


@app.put('/contacts/{id_contact}')
def update_contact(id_contact:int, new_info:Contact):
    contact = new_info.model_dump()
    db.database.update_record(TABLE_NAME, id_contact, contact)
    return {"status": "update"}


@app.delete('/contacts/{id_contact}')
def delete_contact(id_contact:int):
    db.database.delete_record(TABLE_NAME, id_contact)
    return {"status": "deleted"}


if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)
