from imaplib import IMAP4
from email import message_from_bytes

class FaceMailer:
    def __init__(self,host,port):
        self.mail = IMAP4(host,port)
    
    def login(self,username,password):
        self.mail.login(username,password)

    def getCode(self):
        self.mail.select(mailbox="INBOX",readonly=True)
        data = self.mail.search(None,'(FROM "registration@facebookmail.com")')
        mail_ids = data[0].decode('utf-8')
        id_list = mail_ids.split()
        for i in id_list:
            typ, msg_data = self.mail.fetch(str(i), '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = message_from_bytes(response_part[1])
                    subs = msg['subject'].split("\n")
                    for sub in subs:
                        if "is your Facebook confirmation code" in sub:
                            code = sub.split(" is")
                            number = code[0].split("-")[1]
                            return str(number)
        return False
        
    def logout(self):
        self.mail.close()
        self.mail.logout()