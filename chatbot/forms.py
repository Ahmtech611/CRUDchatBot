from django import forms
 
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Enter your email",

        widget=forms.EmailInput(attrs={
            "placeholder": "you@wpbridate.com",
            "autofocus": True,
        })
    )
