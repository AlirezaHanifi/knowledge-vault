# داده‌ی منبع و مشتق‌شده با SQL واقعی

سه برنامه‌ی کوچک SQLite روی داده‌ی یک سوپرمارکت فرضی: یک point query با کلید در برابر یک کوئری تحلیلی که فروش یک ماه را جمع می‌زند، یک جدول derived که حذف و از روی منبعش دوباره ساخته می‌شود، و پاک کردن داده‌ی یک مشتری از system of record، از log append-only‌اش، از یک پروفایل derived و از یک snapshot خروجی‌گرفته. کوئری‌ها SQL ساده‌اند و می‌توانید عیناً در کنسول warehouse خودتان اجرایشان کنید.

*این آزمایش بخش‌های «مشخصه‌های پردازش تراکنش و تحلیل» (صص. ۵–۷)، «مفهوم system of record و derived data» (صص. ۱۰–۱۲) و «سیستم‌های داده، قانون و جامعه» (صص. ۲۴–۲۵) از ویراست دوم DDIA را نشان می‌دهد. سؤال‌های سوپرمارکت از مثال‌های کتاب در صفحه‌ی ۵ آمده‌اند؛ داده، جدول‌ها و روش شمردن مال خود vault است.*

## اجرا

با Python 3.10 یا جدیدتر، فقط کتابخانه‌ی استاندارد (`sqlite3` در حافظه) و قطعی: داده با seed ساخته می‌شود و برنامه ردیف می‌شمارد، نه زمان.

```sh
python3 derived.py
```

خروجی برنامه انگلیسی است، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را درست نشان نمی‌دهند.

## خروجی مورد انتظار

```text
1. Point query vs analytical query (pp. 5-6)
   OLTP: fetch sale #4217 by key           -> 1 row returned,       1 row touched
   OLAP: revenue per store in January      -> 3 rows returned, 20,000 rows touched
         centre   46,998
         north    45,320
         south    45,115
   One query asks for one record and reads one; the other asks for three numbers and reads them all.

2. Systems of record and derived data (pp. 10-11)
   Derived table dropped: the system of record still has every sale.
   Rebuilt from the source: 9 rows, identical to before: True
   After one source update: derived total 409,567, source total 409,667 (stale by 100) until something rebuilds it.

3. Erasing one customer (pp. 24-25)
   Before:                                      rows still about #417: sales 10, sales_log 10, customer_profile 1, export_2026_02 10
   Deleted from the system of record:           rows still about #417: sales_log 10, customer_profile 1, export_2026_02 10
   Rebuilt the derived profile from the log:    rows still about #417: sales_log 10, customer_profile 1, export_2026_02 10
   Rewrote the log, rebuilt again:              rows still about #417: export_2026_02 10
   Found and deleted the exported snapshot:     rows still about #417: none
```

## به چه چیزی نگاه کنید

- **بخش ۱:** تابع پایتونی `touch()` در شرط `WHERE` ردیف‌هایی را می‌شمارد که SQLite واقعاً بررسی می‌کند. point query از راه index کلید اصلی فقط ۱ ردیف می‌خواند؛ کوئری تحلیلی برای برگرداندن سه عدد هر ۲۰٬۰۰۰ ردیف را می‌خواند. همین تفاوت الگوی دسترسی موضوع جدول ۱-۱ کتاب است (ص. ۶).
- **بخش ۲:** حذف یک جدول derived چیزی را از بین نمی‌برد، چون از روی system of record دوباره ساخته می‌شود. ولی با یک به‌روزرسانی در منبع، این جدول تا rebuild بعدی کهنه می‌ماند: هر جا داده derived است، چیزی باید به‌روزش کند (ص. ۱۱).
- **بخش ۳:** پاک کردن از system of record کافی نیست. پروفایل از روی log ساخته می‌شود، پس مشتری در هر rebuild برمی‌گردد تا وقتی خود log بازنویسی شود. snapshot خروجی‌گرفته هم اصلاً به هیچ rebuildی ربط ندارد (صص. ۲۴–۲۵).

## قدم بعدی

- یک index روی `month` بسازید (`CREATE INDEX ON sales(month)`) و بخش ۱ را دوباره اجرا کنید. کوئری ژانویه حالا چند ردیف را لمس می‌کند و چرا هنوز خیلی بیشتر از point query است؟
- به جای حذف مشتری ۴۱۷ از `sales_log`، شماره‌ی مشتری را با یک عدد تصادفی عوض کنید. کدام جدول‌ها دیگر چیزی درباره‌ی آن آدم ندارند و پروفایل چه چیزی را از دست می‌دهد؟
