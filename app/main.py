from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import uvicorn
from db_manager import DBContactsManager

DATABASE = 'contacts_db'

class Contact(BaseModel):
    first_name:str
    last_name:str
    phone_number:str

app = FastAPI()

db = DBContactsManager(DATABASE)
table_name = 'contacts'
db.create_table(table_name)

@app.get('/contacts')
def get_all_contacts():
    return db.database.get_all(table_name)


@app.post('/contacts')
def create_contact(contact:Contact):
    d_contact = contact.model_dump()
    new_id = db.database.create_contact(table_name,d_contact)
    return {'message':"Contact created successfully",
            'id':new_id}


@app.put('/contacts/{id_contact}')
def update_contact(id_contact:int, new_info:Contact):
    contact = new_info.model_dump()
    db.database.update_record(table_name,id_contact,contact)

@app.delete('/contact/{id_contact}')
def delete_contact(id_contact:int):
    db.database.delete_record(table_name,id_contact)

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)
