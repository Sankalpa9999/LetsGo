from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from Home.models import Vendor, Product, ProductImages, DocumentImage, TermsAndConditions
from django.contrib.auth.forms import PasswordChangeForm

from django.forms import inlineformset_factory



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'image', 'description', 'price', 'old_price',
            'specifications', 'department', 'category',
            'featured'
        ]
        # widgets = {
        #     'tags': forms.TextInput(attrs={'placeholder': 'Enter comma-separated tags'}),
        # }

ProductImageFormSet = inlineformset_factory(
    Product, ProductImages,
    fields=('image',),
    extra=3,
    can_delete=True
)

DocumentImageFormSet = inlineformset_factory(
    Product, DocumentImage,
    fields=('document',),
    extra=2,
    can_delete=True
)

TermsAndConditionsFormSet = inlineformset_factory(
    Product, TermsAndConditions,
    fields=('term_image', 'description'),
    extra=1,
    can_delete=True
)
