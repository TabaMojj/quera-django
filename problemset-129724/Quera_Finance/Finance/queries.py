from django.db.models import F, Sum, Count, Subquery
from .models import *


def query_0():
    q = Employee.objects.all()
    return q


def query_1():
    queryset = (Payslip.objects
                .filter(payment=None)
                .annotate(total_salary=F('base') + F('tax') + F('insurance') + F('overtime'))
                .aggregate(total_dept=Sum('total_salary')))
    return queryset


def query_2(x):
    queryset = (Salary.objects
                .filter(overtime__gte=x)
                .aggregate(total_overtime=Sum('payslip__overtime'))
                )

    return queryset


def query_3():
    queryset = Payment.objects.aggregate(total=Sum('amount'))
    return queryset


def query_4(x):
    queryset = (EmployeeProjectRelation.objects
                .filter(employee=x)
                .aggregate(total_hours=Sum('hours')))
    return queryset


def query_5(x):
    select_employee_ids_gt_x = (Payslip.objects
                                .exclude(payment=None)
                                .values('salary__employee_id')
                                .annotate(total_salary=Sum('payment__amount'))
                                .filter(total_salary__gte=x)
                                .values_list('salary__employee_id', flat=True))

    select_employees = (Employee.objects
                        .filter(id__in=Subquery(select_employee_ids_gt_x))
                        .all())
    return select_employees


def query_6():
    employee = (Employee.objects
                .annotate(total_hours=Sum('employeeprojectrelation__hours'))
                .order_by('-total_hours', 'account__username')
                .first())
    return employee


def query_7():
    queryset = (Department.objects
                .annotate(total=Sum('employee__salary__payslip__payment'))
                .order_by('-total', 'name')
                .first())
    return queryset


def query_8():
    department = (Department.objects
                  .filter(project__end_time__gt=F('project__estimated_end_time'))
                  .annotate(num_projects=Count('project__department_id')).order_by('-num_projects', 'name')
                  .first())

    return department


def query_9(x):
    queryset = (Employee.objects
                .filter(attendance__in_time__lte=x)
                .annotate(count=Count('id'))
                .order_by('-count', 'account__username')
                .first())

    return queryset


def query_10():
    count = (Employee.objects
             .exclude(employeeprojectrelation__employee_id=F('id'))
             .count())
    return {'total': count}
