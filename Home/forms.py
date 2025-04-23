from django import forms
from Home.models import ProductReview, RentalRequest

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write your review here...'}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        



class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ['rent_date', 'return_date', 'address']  # Include 'address' field
        widgets = {
            'rent_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter rental address here...'}),  # Address field
        }
