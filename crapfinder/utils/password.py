import getpass
import os
from os.path import join
from dotenv import load_dotenv

from crapfinder.utils.utils import get_project_root

def user_credential_input() -> tuple[str, str]:
    user = input('Username: ')
    password = getpass.getpass()

    return user, password

def get_app_password():
    dotenv_path = join(get_project_root(), '.env')
    load_dotenv(dotenv_path)

    return os.getenv('USER_EMAIL'), os.getenv('PASSWORD')

if __name__ == '__main__':
    user, password = get_app_password()

    print('User =', user)
    print('Password =', password)