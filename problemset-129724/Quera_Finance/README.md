 ## توضیحات

به نظر می‌آید صورت سوال ۸ مشکل دارد.
اگر صورت سوال را در نظر بگیریم، کوئری به این شکل است (با شرط lte):
```
Department.objects
.filter(project__end_time__lte=F('project__estimated_end_time'))
.annotate(num_projects=Count('project__department_id')).order_by('-num_projects', 'name')
.first())
```
در این حالت ردیف‌هایی را به دست می‌آوریم که زمان پایان آن‌ها کوچکتر یا مساوی زمان پیش‌بینی شده است؛ به‌عبارت دیگر زودتر از پیش‌بینی به اتمام رسیده‌اند.

اما با استفاده از این کوئری تست مربوط به سوال ۸ FAIL می‌شود.

اگر صورت سوال را *بخشی که بیشترین تعداد پروژه را زودتر یا برابر موعد پیش‌بینی‌ شده تحویل داده است* در نظر بگیریم، کوئری به این شکل است(با شرط gte):
```
Department.objects
.filter(project__end_time__gte=F('project__estimated_end_time'))
.annotate(num_projects=Count('project__department_id')).order_by('-num_projects', 'name')
.first())
```
در این حالت ردیف‌هایی را به دست‌ می‌آوریم که زمان پایان آن‌ها بزرگ‌تر یا مساوی زمان پیش‌بینی شده است؛ به عبارت دیگر دیرتر از پیش‌بینی به اتمام رسیده‌اند.
حتی اگر از شرط gt هم استفاده کنید، باز هم جواب درست است.
