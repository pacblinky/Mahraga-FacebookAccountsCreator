from imap_tools import MailBoxUnencrypted,AND
from re import findall

class Mailer:
    def __init__(self,host,port):
        self.mail = MailBoxUnencrypted(host,port)
    
    def login(self,username,password):
        try:
            self.mail.login(username,password,initial_folder="INBOX")
            return True
        except Exception:
            return False

    def getCode(self):
        for msg in self.mail.fetch(criteria=AND(from_="registration@facebookmail.com")):
            if "is your Facebook confirmation code" in msg.subject:
                return findall(r"\b\d{5}\b", msg.subject)[0]
        return False
        
    def logout(self):
        self.mail.logout()