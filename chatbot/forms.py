from django import forms
 
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Enter your email",

        widget=forms.EmailInput(attrs={
            "placeholder": "enter email",
            "autofocus": True,
        })
    )
