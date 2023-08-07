## لینک‌های مفید مرتبط با مسئله
1. [لینک](https://stackoverflow.com/questions/35999186/how-can-one-change-the-type-of-a-django-model-field-from-charfield-to-foreignkey "لینک")
2. [لینک](https://stackoverflow.com/questions/31914222/django-new-foreignkey-field-based-on-existing-field "لینک")

## توضیحات

برای اینکه به‌هنگام migration داده‌های موجود را متناسب با مدل جدید تغییر دهیم، در فایلی که بعد از اجرای دستور makemigrations ایجاد می‌شود، تابع‌هایی برای ایجاد تغییرات می‌نویسیم. سپس این تابع‌ها را در operations می‌گذاریم تا اجرا شوند. بعد از ساخت مدل Category، عنوان‌های دسته‌بندی را از داده‌های موجود در Article می‌گیریم تا آبجکت‌های متناظر را در Category ایجاد کنیم. سپس فیلد Article.category را با مقدار category.id به‌روزرسانی می‌کنیم.

دقت کنید که در تمام تابع‌ها از متد save استفاده نمی‌کنیم تا در داده‌های موجود، Article.updated=Article.created باقی بماند.
