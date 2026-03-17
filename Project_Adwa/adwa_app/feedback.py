import smtplib
import dotenv
import os

dotenv.load_dotenv()
email_psd = os.getenv("EMAIL_PSD")

class EmailHandler:
    def __init__(self,feed,name,email="No Email"):
        self.status = "Failed"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login("abelalex530@gmail.com",email_psd )
            connection.sendmail(from_addr="abelalex530@gmail.com", to_addrs="abelalex122129@gmail.com",
                                msg=f"Subject:From: {name}\nEmail{email} \n\n\n{feed}")
            connection.close()
            self.status = "Success"

    def status_email(self):
        return {"status":self.status}