from rest_framework.decorators import api_view


@api_view(['POST'])
def get_sick_employee_by_hospital(request):
    pass


@api_view(['POST'])
def get_sick_employee_by_company(request):
    pass


async def sms_link(request):

    request.META['CONTENT_LENGTH'] = 35

    pass
