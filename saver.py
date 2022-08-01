from sql import SQL


class Saver:
    def __init__(self,host,port,username,password,database):
        self.db = SQL(host,port,username,password,database)
    
    def open(self):
        if self.db.connect():
            return True
        else:
            return False

    def addAccount(self, email, password, gender, table):
        try:
            self.db.query("""INSERT INTO `closed_accounts`(`email`, `password`, `gender`) VALUES(?, ?, ?)""",[email, password, gender])
            return True
        except Exception:
            return False

    def close(self):
        self.db.disconnect()
