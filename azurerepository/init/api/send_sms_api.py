from twilio.rest import Client
import sys
import smtplib

def send_sms(message):

    final_message = message
    
    account_sid = "AC360fe6d8105de18b7c969b40f157a80f"
    auth_token  = "002d4c63b65f9dfcac1df9d14d02ea08"
    
    client = Client(account_sid, auth_token)
    
    # message = client.messages.create(
    #     to="+910000000000", 
    #     from_="+10000000000",
    #     body=final_message)
    
    # message = client.messages.create(
    #     to="whatsapp:+910000000000", 
    #     from_="whatsapp:+10000000000",
    #     body=final_message)

    # print(message.sid)

def send_email(message):
    message = "This message is from Group 7 to Barricade: {}".format(message)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("group7barricade@gmail.com", "group7##")
    s.sendmail("group7barricade@gmail.com", "mailid@gmail.com", message)
    s.quit()