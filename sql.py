import mariadb

class SQL:
    def __init__(self,host,port,username,password,database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.cursor = None
        self.db = None

    def connect(self):
        try:
            self.db = mariadb.connect(user=self.username,password=self.password,host=self.host,port=self.port,database=self.database)
            self.cursor = self.db.cursor()
            return True
        except Exception:
            return False

    def query(self,sql,params = []):
        self.cursor.execute(sql,params)
        self.cursor.commit()

    def disconnect(self):
        self.cursor.close()
        self.db.close()

