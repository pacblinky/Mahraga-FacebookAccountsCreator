import random
import json

class Person:
    users = None
    def __init__(self,fname,lname,gender,day,month,year):
        self.fname = fname
        self.lname = lname
        self.gender = gender
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def getUser():
        data = random.choice(Person.users)
        return Person(data["first_name"],data["last_name"],data["gender"],data["date"].split("/")[0],data["date"].split("/")[1],data["date"].split("/")[2])

    @staticmethod
    def initUsers():
        with open('data.json','r') as f:
            Person.users = json.load(f)
