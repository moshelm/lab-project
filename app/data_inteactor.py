import mysql.connector

HOST = 'localhost'
USER = 'root'

class Database:
    def __init__(self,database_name:str):
        self.conn = mysql.connector.connect(host=HOST,user=USER)
        self.cursor = self.conn.cursor()
        self.name = database_name

    def create_database(self):
        sql = f"CREATE DATABASE IF NOT EXISTS `{self.name}`;"
        self.cursor.execute(sql)
        return self.name

    def create_table(self, table_name:str, fields:tuple[str]):
        fields = ',\n'.join(fields)
        if not fields:
            raise ValueError
        sql = f"""USE {self.name};
        CREATE TABLE IF NOT EXISTS `{table_name}` (
id INT AUTO_INCREMENT PRIMARY KEY,
{fields});"""

        self.cursor.execute(sql)
