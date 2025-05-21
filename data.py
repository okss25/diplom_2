from helper import *


class UsersData:
    email = 'Barsik_kolbas_44@ya.ru'
    password = 'Kitsi_44'
    username = 'Barsik'

    credentials_with_empty_field = [
        {'email': '',
         'password': create_random_password(),
         'name': create_random_username()
         },
        {'email': create_random_email(),
         'password': '',
         'name': create_random_username()
         },
        {'email': create_random_email(),
         'password': create_random_password(),
         'name': ''
         }
    ]


class IngredientData:
    burger_1 = ['61c0c5a71d1f82001bdaaa74', '61c0c5a71d1f82001bdaaa6c',
                '61c0c5a71d1f82001bdaaa6f', '61c0c5a71d1f82001bdaaa79']

    burger_2 = ['61c0c5a71d1f82001bdaaa73', '61c0c5a71d1f82001bdaaa6d',
                '61c0c5a71d1f82001bdaaa7a', '61c0c5a71d1f82001bdaaa76']

    invalid_hash_ingredient = '61c0c5a71d1f088005553535'