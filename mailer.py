from imap_tools import MailBoxUnencrypted,AND

class FaceMailer:
    def __init__(self,host,port):
        self.mail = MailBoxUnencrypted(host,port)
    
    def login(self,username,password):
        self.mail.login(username,password,initial_folder="INBOX")

    def getCode(self):
        for msg in self.mail.fetch(criteria=AND(from_="registration@facebookmail.com")):
            if "is your Facebook confirmation code" in msg.subject:
                code = msg.subject.split(" ")[0]
                number = code.split("-")[1]
                return number
        return False
        
    def logout(self):
        self.mail.close()
        self.mail.logout()