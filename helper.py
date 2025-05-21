
from faker import Faker

fake = Faker()
fakeRU = Faker(locale='ru_RU')


def create_random_email():
    email = fake.free_email()
    return email


def create_random_password():
    password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return password


def create_random_username():
    username = fakeRU.first_name()
    return username
def get_headers(token=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers