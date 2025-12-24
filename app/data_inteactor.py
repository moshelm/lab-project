import mysql.connector

HOST = 'localhost'
USER = 'root'


class Database:
    def __init__(self,database_name:str = None, file_name :str = None):
        if database_name is None and file_name is None:
            raise ValueError("we need or name for database or file name")

        self.conn = mysql.connector.connect(host=HOST,user=USER)
        self.cursor = self.conn.cursor()

        if database_name:
            self.name = database_name
            self._create_database()
        else:
            self._initialize_schema(file_name)

    def _initialize_schema(self,file_name:str):
        with open(file_name, 'r') as file:
            commends_sql = file.read().split(';')
            for commend in commends_sql:
                if commend.strip():
                    self.cursor.execute(commend)
                    self.conn.commit()
            self.cursor.execute("SELECT DATABASE();")
            name = self.cursor.fetchone()[0]
            self.name = name
            self.conn.database = self.name

    def _create_database(self):
        sql = f"CREATE DATABASE IF NOT EXISTS `{self.name}`;"
        self.cursor.execute(sql)
        self.conn.database = self.name


    def create_table(self, table_name:str, fields:tuple[str]):
        fields = ','.join(fields)
        if not fields:
            raise ValueError
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
id INT AUTO_INCREMENT PRIMARY KEY,
{fields});"""

        self.cursor.execute(sql)

    def create_contact(self,table_name:str, info:dict):
        fields = ','.join(list(info.keys()))
        values = tuple(info.values())
        flags = ','.join(['%s' for _ in range(len(list(info.keys())))])
        print(f"field : {fields}")
        print("-------------------------------")
        print(f"values : {values}")
        print("-------------------------------")
        print(f"flags : {flags}")
        sql = (f"""
               INSERT INTO `{table_name}` ({fields})
               VALUES ({flags});""")
        print("-------------------------------")
        print(f"sql : {sql}")
        self.cursor.execute(sql,values)
        new_id = self.cursor.lastrowid
        self.conn.commit()
        return new_id

    def get_all(self,table_name:str):
        sql = f"SELECT * FROM `{table_name}`;"
        self.cursor.execute(sql)
        result = [row for row in self.cursor]
        if result:
            return result
        else:
            return None

    def update_record(self,table_name:str,record_id:int, update_info:dict):
        updates = []
        for field in list(update_info.keys()):
            updates.append(f"{field} = %s")

        sql = f"""UPDATE  `{table_name}` SET {','.join(updates)} WHERE id = %s;"""
        l_update_info = list(update_info.values())
        l_update_info.append(record_id)
        values = tuple(l_update_info)

        self.cursor.execute(sql,values)
        self.conn.commit()

    def delete_record(self,table_name:str, record_id:int):
        sql = f"DELETE FROM {table_name} WHERE id = %s"
        value = (record_id,)

        self.cursor.execute(sql,value)
        self.conn.commit()
        return self.cursor.rowcount




