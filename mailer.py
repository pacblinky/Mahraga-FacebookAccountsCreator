import imaplib
import email

class FaceMailer:
    def __init__(self,host,port):
        self.mail = imaplib.IMAP4(host,port)
    
    def login(self,username,password):
        self.mail.login(username,password)

    def getCode(self):
        self.mail.select(mailbox="INBOX",readonly=True)
        messages = self.mail.fetch(criteria=AND(from_="registration@facebookmail.com"),mark_seen=TRUE,bulk=True)
        for msg in messages:
            print(msg.subject)
    
    def logout(self):
        self.mail.close()
        self.mail.logout()


mailer = FaceMailer("mail.mahraga.com",143)
mailer.login("admin@mahraga.com","Mail012243543")
mailer.getCode()     
