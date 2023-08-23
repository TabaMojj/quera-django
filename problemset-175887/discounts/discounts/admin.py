from django.contrib import admin

from .models import CountryDiscount, AuthorDiscount, CategoryDiscount, BookDiscount

# Register your models here.
admin.site.register(CountryDiscount)
admin.site.register(AuthorDiscount)
admin.site.register(CategoryDiscount)
admin.site.register(BookDiscount)
