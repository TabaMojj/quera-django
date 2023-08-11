from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price > 1000:
            raise ValidationError('Product is too expensive')
        return price

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) <= 20:
            raise ValidationError('Product must have a good description')
        return description
