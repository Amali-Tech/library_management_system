"""Register user from goolge helper functions"""
import os
import random
from authentications.models import Users


def generate_username(name):
    """When user already exist, it add a new number to the username"""

    username = "".join(name.split(' ')).lower()
    if not Users.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user( email, username):
    """Registers a new social user to the database"""
    filtered_user_by_email = Users.objects.filter(Email_Address=email)
    print(filtered_user_by_email)

    if filtered_user_by_email.exists():
        registered_user = filtered_user_by_email[0]
        return {
            'username': registered_user.username,
            'email': registered_user.Email_Address,
            'tokens': registered_user.token}

    else:
        user = {
            'username': generate_username(username), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        user = Users.objects.create_user(**user)
        user.save()

        return {
            'email': user.Email_Address ,
            'username': user.username,
            'tokens': user.token
        }
