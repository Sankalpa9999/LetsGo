from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)
    message = forms.CharField(widget=forms.Textarea)

