from django import forms
from .models import Administrators


class Administrators_Form(forms.ModelForm):
    class Meta:
        model = Administrators
        fields = [
       "password",
       "last_login",
       "is_superuser",
        "username",
       "first_name",
       "last_name",
       "email",
       "is_staff",
       "is_active",
       "date_joined",
       "fingerprint_data",
       "last_fingerprint_update",
        "failed_login_attempts",
       "account_locked_until",
        ]
        