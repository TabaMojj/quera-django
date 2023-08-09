from django.db.models import Sum, Count, Case, When, F
from .models import *


def query_0():
    q = Driver.objects.all()
    return q


def query_1():
    queryset = Payment.objects.aggregate(income=Sum('amount'))
    return queryset


def query_2(x):
    queryset = (Payment.objects
                .filter(ride__request__rider_id=x)
                .aggregate(payment_sum=Sum('amount')))
    return queryset


def query_3():
    queryset = (Driver.objects
                .filter(car__car_type='A')
                .annotate(num_cars=Count('car'))
                .filter(num_cars__gte=1)
                .count())

    return queryset


def query_4():
    queryset = RideRequest.objects.filter(ride__isnull=True).all()
    return queryset


def query_5(t):
    queryset = (Rider.objects
                .annotate(total_payments=Sum('riderequest__ride__payment__amount'))
                .filter(total_payments__gte=t))
    return queryset


def query_6():
    queryset = (Account.objects
                .annotate(num_cars=Count('drivers__car'))
                .order_by('-num_cars', 'last_name')
                .first())
    return queryset


def query_7():
    queryset = (Rider.objects
                .filter(riderequest__ride__car__car_type='A')
                .annotate(n=Count('id')))
    return queryset


def query_8(x):
    queryset = (Driver.objects
                .annotate(car_model_fixed=Case(When(car__model__lte=99, then=1300 + F('car__model')), default=F('car__model')))
                .filter(car__model__gte=x)
                .annotate(num=Count('car'))
                .filter(num__gte=1)
                .values('account__email'))

    return queryset


def query_9():
    queryset = (Driver.objects
                .annotate(n=Count('car__ride')))
    return queryset


def query_10():
    queryset = (Driver.objects
                .values('account__first_name')
                .annotate(n=Count('car__ride')))
    return queryset


def query_11(n, c):
    queryset = (Driver.objects
                .filter(car__color=c, car__model__gte=n)
                .distinct())
    return queryset


def query_12(n, c):
    queryset = (Driver.objects
                .filter(car__color=c)
                .filter(car__model__gte=n)
                .distinct())
    return queryset


def query_13(n, m):
    queryset = (Ride.objects
                .filter(request__rider__account__first_name=m, car__owner__account__first_name=n)
                .annotate(duration=F('dropoff_time') - F('pickup_time'))
                .aggregate(sum_duration=Sum('duration')))

    return queryset
