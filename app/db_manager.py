from data_inteactor import Database


class DBContactsManager:
    def __init__(self,database_name:str=None, file_name :str = None):
        if database_name is None and file_name is None:
            raise ValueError("we need or name for database or file name")
        if database_name:
            self.database = Database(database_name=database_name)
            self._create_table('contacts')
        else:
            self.database = Database(file_name=file_name)


    def _create_table(self,table_name:str):
        fields = ('first_name VARCHAR(50) NOT NULL','last_name VARCHAR(50) NOT NULL','phone_number VARCHAR(20) NOT NULL UNIQUE')
        self.database.create_table(table_name,fields)

