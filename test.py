from email import parser
import requests
from bs4 import BeautifulSoup as soup


requestor = requests.session()
login_data = {
    "email": "admin@mahraga.com",
    "pw": "Mail012243543",
    "submitAdmin": "Sign in Admin"
}
requestor.get("http://mail.mahraga.com/sso/login")
requestor.post("http://mail.mahraga.com/sso/login",data=login_data)
response = requestor.get("http://mail.mahraga.com/admin/user/create/mahraga.com")
csrf_token = soup(response.text,'html.parser').select_one('input#csrf_token')["value"]
account_data = {
    "localpart": "test14256",
    "pw": "abo zabaal",
    "pw2": "abo zabaal",
    "displayed_name": "",
    "comment": "",
    "enabled": "y",
    "quota_bytes": 1000000000,
    "enable_imap": "y",
    "enable_pop": "y",
    "submit": "Save",
    "csrf_token": str(csrf_token)
}
p = requestor.post("http://mail.mahraga.com/admin/user/create/mahraga.com",data=account_data)   
print(p.status_code)