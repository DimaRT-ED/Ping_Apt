# This is a sample Python script.
#        20_8_2022
#      created by Dima
#   Automation app for rt-ed.co.il , student-portal and crm
#  start with :  pip install -r requirements.txt
# --------------------------------------------------------------------------------------
import requests
import urllib3.exceptions
from data import Data
import os

list_Of_Url = Data.urls.values()
good_request = Data.string["good_response"]

rotations = 0


# ========================================================================================
def send_sms(msg: str, number: str):
    str_sms = create_sms_msg(msg, number)
    print(str_sms)
    url = Data.urls_services["sms"]
    print(requests.post(url, str_sms))


def send_mail(msg: str, addrs: str, subj: str):
    str_mail = create_email_msg(msg, addrs, subj)
    url = Data.urls_services["mail"]
    print(str_mail)
    requests.post(url, str_mail)


def create_sms_msg(msg: str, phone_number: str):
    sms_dict = {"message": msg,
                "phone": phone_number,
                "source": "RT_CRONTAB"}
    return sms_dict


def create_email_msg(msg: str, addressee: str, subj: str):
    email_dict = {"to": addressee,
                  "from": Data.string["omer's_email"],
                  "subject": subj,
                  "html": msg,
                  "source": "RT_CRONTAB"}
    return email_dict


def validate(val_str: str) -> bool:
    if val_str == good_request:
        return True
    else:
        return False


def make_connection(urls) -> str:
    from_url: str = ''
    last_msg: str = ''
    for url in urls:
        try:
            last_msg = str(requests.get(url))
            if validate(last_msg):
                print(f"{url} connection is good :)")
                pass
            else:
                from_url = not_a_response_200(from_url, url)
        except requests.exceptions.ConnectionError:
            from_url = website_not_uploaded(from_url, url)
        except urllib3.exceptions.MaxRetryError:
            from_url = website_not_uploaded(from_url, url)
        except:
            from_url = website_not_uploaded(from_url, url)
    return from_url


def website_not_uploaded(from_url, url):
    print("An error has been raised during the connection")
    last_msg = f'{url} is not available\n'
    from_url += last_msg + ""
    return from_url


def not_a_response_200(from_url, url):
    print("Not a response 200...")
    last_msg = f'{url} is not available\n'
    from_url += last_msg + " "
    return from_url


def file_write(msg: str):
    try:
        f = open("./rotations.txt", "w")
        f.write(msg)
        f.close()
    except:
        print("File Not Found...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        file = open("./rotations.txt", "r")
        rotations = file.read()
        file.close()
    except:
        print("File Not Found...")

    all_req_msg = make_connection(list_Of_Url)
    print(all_req_msg)

    if all_req_msg != '':
        send_sms(all_req_msg, Data.king_pablik["phone_number"])
        send_mail(all_req_msg, Data.king_pablik["email"], "Website is not uploaded")
        send_sms(all_req_msg, Data.uncle_dima["phone_number"])
        send_mail(all_req_msg, Data.uncle_dima["email"], "Website is not uploaded")
        send_mail(all_req_msg, Data.big_daddy_benny["email"], "Website is not uploaded")
        file_write("0")
        exit()

    rotations = int(rotations) + 1

    file_write(str(rotations))

    if rotations == 10:
        send_sms("10 Consecutive Tests Has Ran Successfully! :)", Data.king_pablik["phone_number"])
        send_mail("10 Consecutive Tests Has Ran Successfully! :)", Data.king_pablik["email"], "Tests Ran Successfully")
        send_sms("10 Consecutive Tests Has Ran Successfully! :)", Data.uncle_dima["phone_number"])
        send_mail("10 Consecutive Tests Has Ran Successfully! :)", Data.uncle_dima["email"], "Tests Ran Successfully")
        send_mail("10 Consecutive Tests Has Ran Successfully! :)", Data.big_daddy_benny["email"], "Tests Ran Successfully")
        file_write("0")
