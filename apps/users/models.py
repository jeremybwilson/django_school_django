from __future__ import unicode_literals

from django.db import models
import re, bcrypt

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_and_create_user(self, form_data):
        errors = []

        name = form_data['name']
        email = form_data['email']
        password = form_data['password']
        confirm_password = form_data['confirm_password']

        if len(name) < 1:
            errors.append('Name cannot be blank.')
        if len(name) < 2:
            errors.append('Name must be longer than 2 characters.')
        if len(email) < 1:
            errors.append('Email cannot be blank.')
        elif not EMAIL_REGEX.match(email):
            errors.append('You must enter a valid email address!')
        if len(password) < 1:
            errors.append('Password cannot be blank.')
        if len(password) < 3:
            errors.append('Password must be at least 3 characters long.')
        if len(confirm_password) < 1:
            errors.append('Confirm password cannot be blank.')
        if password != confirm_password:
            errors.append('Passwords do not match!')

        if errors:
            return (False, errors)
        # check for existence of a user
        try:
            existing_user = User.objects.get(email=email)
            errors.append('Email already exists.')
            return (False, errors)
        except:
            # REMEMBER TO HASH THE PASSWORD
            # pw_hash = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())   # shortened variable names before passing them here
            # user = self.create(name=form_data['name'], email=form_data['email'], pw_hash=pw_hash, permission_level="STUDENT")
            user = self.create(name=name, email=email, pw_hash=pw_hash, permission_level='STUDENT')   # shortened variable names before passing them here

        return (True, user.id)

    def login_user(self, form_data):
        errors = []
        email = form_data['email']
        password = form_data['password']

        try:
            user = self.get(email=email)
            # check to see if passwords match
            if not bcrypt.checkpw(password.encode(), user.pw_hash.encode()):
                errors.append('Username or password is invalid')
                return (False, errors)
            return (True, user.id)
        except:
            errors.append('Username or password is invalid')
            return (False, errors)

    def validate_and_update_user(self, user_id, form_data):
        errors = []
        # not converting form data into straight variables
        if len(form_data['name']) < 2:  # len of name field must be at least 2 chars
            errors.append('Name must be at least 2 characters')
        if not EMAIL_REGEX.match(form_data['email']):  # email field must meet complexity/regex reqs
            errors.append('Must use a valid email address')

        if errors:
            return (False, errors)

        try:
            user = self.get(id=user_id)
            user.name = form_data['name']
            user.email = form_data['email']
            user.save()
            return (True, user)
        except:
            errors.append("User doesn't exist")
            return (False, errors)

    def delete_user_by_id(self, user_id):
        try:
            user = self.get(id=user_id)
            user.delete()
            return True
        except:
            return False


class User(models.Model):
    # def __init__(self):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=500)
    permission_level = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        output = "<User object: {} {} {}>".format(self.name, self.email, self.permission_level)
        return output
