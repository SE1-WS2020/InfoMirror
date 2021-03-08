import requests
import json
import shutil


API_URL = "http://127.0.0.1:8000/api/"
LOGIN_URL = API_URL + "login/"
USER_CONFIG_URL = API_URL + "user-config/"
ALL_EMAILS_URL = API_URL + "all_users/"
USER_IMAGE_URL = API_URL + "download_image/"


# check if return value != None (=> token was successfully received)
def get_token(username, password):
    if type(username) == str and type(password) == str:
        login_dict = {
            "username": username,
            "password": password
        }
        response = requests.post(url=LOGIN_URL, json=login_dict)
        if response.ok:
            return response.json()["token"]
        else:
            print("request failed: " + str(response.status_code))
    else:
        print("password and username need to be strings.")


def get_user_config(username, token):
    if type(username) == str and type(token) == str:
        response = requests.get(USER_CONFIG_URL + username, headers={"Authorization": "Token " + token})
        if response.ok:
            #print(response.text)
            # TODO
            return response.json()
            # return response.text
        else:
            if "Invalid token" in response.text:
                print("Token did not match user.")
    else:
        print("password and token need to be strings.")


def get_all_user_images(token):
    if type(token) == str:
        all_user_emails = get_all_user_emails_with_images(token)
        if all_user_emails != None:
            for email in all_user_emails:
                get_user_image(token, email)
    else:
        print("token must be a string")


def get_all_user_emails_with_images(token):
    if type(token) == str:
        response = requests.get(ALL_EMAILS_URL, headers={"Authorization": "Token " + token})

        if response.ok:
            # print([email_dict["user_account"] for email_dict in json.loads(response.text)])
            return [email_dict["user_account"] for email_dict in json.loads(response.text)]
        else:
            print("user emails could not be received " + str(response.status_code))
    else:
        print("token must be a string")


def get_user_image(token, user_email):
    if type(token) == str and type(user_email) == str:
        response = requests.get(USER_IMAGE_URL, data={"user_account": user_email}, headers={"Authorization": "Token " + token})
        file_name = "user_images/" + user_email.replace(".", "_") + ".png"
        #print(user_email)

        with open(file_name, "wb") as file:
            file.write(response.content)

    else:
        print("token and user email must be strings")


#get_user_config("another1@email.com", '87afe80878b563e915db28911b8a2cd018e6e0e5')
# get_all_user_emails(get_token("mirror@admin.com", "123456"))
# get_user_image(get_token("mirror@admin.com", "123456"), "another1@email.com")
# get_all_user_images(get_token("mirror@admin.com", "123456"))
#print(get_token('admin@admin.admin','admin'))
