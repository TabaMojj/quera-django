from django import forms
from .models import Product


class CartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.items = kwargs.pop('items', [])
        super().__init__(*args, **kwargs)

        for product in self.items:
            self.fields[f'number_{product.id}'] = forms.IntegerField(label=product.name, initial=1, required=False)
            colors = product.colors_available.all()
            color_choices = [(color.name, color.name) for color in colors]
            self.fields[f'color_{product.id}'] = forms.ChoiceField(label='color', choices=color_choices,required=False)

    def clean(self):
        cleaned_data = super().clean()
        for product in self.items:
            if not cleaned_data.get(f'number_{product.id}'):
                cleaned_data[f'number_{product.id}'] = 1
            if not cleaned_data.get(f'color_{product.id}'):
                color = product.colors_available.order_by('name').first().name
                cleaned_data[f'color_{product.id}'] = color
        return cleaned_data
