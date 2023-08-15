from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .SMS import get_phone_number
from .models import *
from .serializer import NameSerializer, NationalIDSerializer


@api_view(['POST'])
def get_sick_employee_by_hospital(request):
    serializer = NameSerializer(data=request.data)
    if serializer.is_valid():
        hospital_name = serializer.validated_data['name']
        sicks = (Sick.objects
                 .filter(hospital__name=hospital_name, illName='Covid19')
                 .annotate(value=Concat(Value('('), F('name'), Value(', '), F('nationalID'), Value(')')))
                 .values_list('value', flat=True)
                 )

        response_data = {}
        for index, sick in enumerate(sicks, start=1):
            response_data[index] = sick

        return Response(response_data, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def get_sick_employee_by_company(request):
    serializer = NameSerializer(data=request.data)
    if serializer.is_valid():
        company_name = serializer.validated_data['name']
        employees_national_id = (Company.objects
                                 .get(name=company_name)
                                 .employees
                                 .values_list('nationalID', flat=True))
        sicks = (Sick.objects
                 .filter(nationalID__in=employees_national_id, illName='Covid19')
                 .annotate(value=Concat(Value('('), F('name'), Value(', '), F('nationalID'), Value(')')))
                 .values_list('value', flat=True))

        response_data = {}
        for index, sick in enumerate(sicks, start=1):
            response_data[index] = sick

        return Response(response_data, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def sms_link(request):
    request.META['CONTENT_LENGTH'] = 35
    serializer = NationalIDSerializer(data=request.data)
    if serializer.is_valid():
        national_ids = serializer.validated_data['national_id']
        for national_id in national_ids:
            phone_number = get_phone_number(national_id)
            DeliveryReport.objects.create(phone_number=phone_number)
        return Response(status=200)
    else:
        return Response(serializer.errors, status=400)
