import requests
from bs4 import BeautifulSoup as soup

class Mailu:
    def __init__(self,url):
        self.requestor = requests.session()
        self.url = url

    def login(self,username,password):
        try:
            response = self.requestor.get(self.url+"sso/login")
            if response.status_code == 200:
                response = self.requestor.post(self.url+"sso/login",data={"email": username, "pw": password, "submitAdmin": "Sign in Admin"})
                if response.status_code == 200:
                    return True
                else:
                    return False
        except requests.RequestException:
            return False

    def addUser(self,username,password):
        response = self.requestor.get(self.url+"admin/user/create/mahraga.com")
        if response.status_code == 200:
            try:
                csrf_token = soup(response.text,'html.parser').select_one('input#csrf_token')["value"]
            except Exception:
                return False
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
            response = self.requestor.post(self.url+"admin/user/create/mahraga.com",data=account_data)
            if response.status_code == 302:
                return True
            else:
                return False
        else:
            return False

    def logout(self):
        self.requestor.close()   