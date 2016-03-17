from django import forms
from django.forms.models import modelformset_factory
from products.models import Variation


class VariationInventoryForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['title', 'price', 'sale_price', 'inventory', 'active']
        widgets = {
            'sale_price': forms.NumberInput(attrs={'placeholder': 'sale price'}),
            'title': forms.TextInput(attrs={'placeholder': 'title'}),
            'price': forms.NumberInput(attrs={'placeholder': 'price'}),
            'inventory': forms.NumberInput(attrs={'placeholder': 'inventory'}),
        }


VariationInventoryFormSet = modelformset_factory(Variation, form=VariationInventoryForm, extra=1)
