from django.db import models
from django.contrib.auth import models
# Create your models here.
# https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django-contrib-auth
# more about django's built in registration


class User(models.User, models.PermissionsMixin):

    # using string formating to make it look like twitter usernamer
    # @jack
    def __str__(self):
        return "@{}".format(self.get_username)
    # we dont need to register this models to admin.py, cause its pre-registered.
    # why ? cause we are using built in User models they are pre registered
