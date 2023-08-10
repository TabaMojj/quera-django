from django.db.models import Sum, F, FloatField, Q, Count, Case, When
from django.db.models.functions import Sqrt
from .models import *


def query_0(x):
    queryset = Driver.objects.filter(rating__gt=x)
    return queryset


def query_1(x):
    queryset = (Payment.objects
                .filter(ride__car__owner=x)
                .aggregate(payment_sum=Sum('amount')))
    return queryset


def query_2(x):
    queryset = Ride.objects.filter(request__rider_id=x)
    return queryset


def query_3(t):
    queryset = (Ride.objects
                .annotate(duration=F('dropoff_time') - F('pickup_time'))
                .filter(duration__gt=t)
                .count())
    return queryset


def query_4(x, y, r):
    queryset = (Driver.objects
                .annotate(distance=Sqrt((F('x') - x) ** 2 + (F('y') - y) ** 2, output_field=FloatField()))
                .filter(distance__lte=r, active=True))
    return queryset


def query_5(n, c):
    queryset = (Driver.objects
                .annotate(num_rides=Count('car__ride'))
                .filter(Q(car__car_type='A') | Q(car__color=c), num_rides__gte=n))
    return queryset


def query_6(x, t):
    queryset = (Rider.objects
                .annotate(num_rides=Count('riderequest__ride'))
                .annotate(sum_payment=Sum('riderequest__ride__payment__amount'))
                .filter(num_rides__gte=x, sum_payment__gt=t))
    return queryset


def query_7():
    queryset = (Driver.objects
                .filter(account__first_name=F('car__ride__request__rider__account__first_name'))
                .distinct())
    return queryset


def query_8():
    queryset = (Driver.objects
                .annotate(n=Count('car__ride',
                                  filter=Q(account__last_name=F('car__ride__request__rider__account__last_name')))))
    return queryset


def query_9(n, t):
    queryset = (Driver.objects
                .annotate(duration=F('car__ride__dropoff_time') - F('car__ride__pickup_time'))
                .annotate(n=Count('car__ride', filter=Q(car__model__gte=n, duration__gte=t)))
                .values('id', 'n'))
    return queryset


def query_10():
    queryset = (Car.objects
                .annotate(extra=Case(
                    When(car_type='A', then=Count('ride', output_field=FloatField())),
                    When(car_type='B', then=Sum(F('ride__dropoff_time') - F('ride__pickup_time'), output_field=FloatField())),
                    When(car_type='C', then=Sum('ride__payment__amount', output_field=FloatField())))))
    return queryset
