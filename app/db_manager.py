from data_inteactor import Database


class DBContactsManager:
    def __init__(self,database_name:str):
        self.database = Database(database_name)
        self.database.create_database()

    def create_table(self,table_name:str):
        fields = ('first_name VARCHAR(50) NOT NULL','last_name VARCHAR(50) NOT NULL','phone_number VARCHAR(20) NOT NULL UNIQUE')
        self.database.create_table(table_name,fields)

