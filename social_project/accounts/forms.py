from django.contrib.auth import get_user_model
# returns the user model that is active in this project
# we used models.User for our User model
# https://docs.djangoproject.com/en/3.1/topics/auth/default/
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    # there is django form called usercreationform

# class UserCreationForm

#     A ModelForm for creating a new user.

#     It has three fields: username (from the user model), password1, and password2. It verifies that password1 and password2 match, validates the password using validate_password(), and sets the user’s password using set_password().
# we added one more with email

    # we use keyword dic here ie**kwargs to change the username label to something else
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'IGN (In Game Name)'
        self.fields['email'].label = 'Email Address'
