import requests
from bs4 import BeautifulSoup as soup

class Mailu:
    def __init__(self,url):
        self.requestor = requests.session()
        self.url = url

    def login(self,username,password):
        self.requestor.get(self.url+"/sso/login",data={"email": username, "pw": password, "submitAdmin": "Sign in Admin"})

    def addUser(self,username,password):
        response = self.requestor.get(self.url+"/admin/user/create/mahraga.com")
        csrf_token = soup(response.text,'html.parser').select_one('input#csrf_token')["value"]
        account_data = {
            "localpart": username,
            "pw": password,
            "pw2": password,
            "displayed_name": "",
            "comment": "",
            "enabled": "y",
            "quota_bytes": 1000000000,
            "enable_imap": "y",
            "enable_pop": "y",
            "submit": "Save",
            "csrf_token": str(csrf_token)
        }
        self.requestor.post(self.url+"/admin/user/create/mahraga.com",data=account_data)   

    def logout(self):
        self.requestor.close()   