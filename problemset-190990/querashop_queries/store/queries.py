from datetime import timedelta
from datetime import datetime
from .models import Employee, Product, Order, Company
from django.db.models import Avg, Sum, Count, Q


def young_employees(job: str):
    queryset = (Employee.objects
                .filter(job__exact=job, age__lt=30)
                .all())
    return queryset


def cheap_products():
    price_average = (Product.objects
                     .aggregate(Avg('price'))
                     .get('price__avg'))
    queryset = (Product.objects
                .filter(price__lte=price_average)
                .order_by('price')
                .values_list('name', flat=True))
    return list(queryset)


def products_sold_by_companies():
    queryset = (Product.objects
                .values('company__name')
                .annotate(sold=Sum('sold'))
                .values_list('company__name', 'sold'))
    return queryset


def sum_of_income(start_date: str, end_date: str):
    price_sum = (Order.objects
                 .filter(time__gte=start_date, time__lte=end_date)
                 .aggregate(Sum('price'))
                 .get('price__sum'))
    return price_sum


def good_customers():
    now = datetime.now()
    last_month = now - timedelta(days=30)
    queryset = (Order.objects
                .filter(time__lt=now, time__gt=last_month)
                .values('customer__name')
                .annotate(count=Count('customer__name'))
                .filter(count__gt=10)
                .values_list('customer__name', 'customer__phone'))
    return queryset


def nonprofitable_companies():
    queryset = (Company.objects
                .annotate(num_products_sold_less_than_100=Count('product', filter=Q(product__sold__lt=100)))
                .filter(num_products_sold_less_than_100__gte=4)
                .values_list('name', flat=True))
    return list(queryset)
