# برنامه‌ی موازی: هزینه‌ی انتظار برای API

یک launch کوچک، یعنی طراحی API و ساختنش و ساختن frontend و یکپارچه‌سازی و تست و انتشار، دو بار زمان‌بندی می‌شود. در برنامه‌ی اول، frontend منتظر API واقعی می‌ماند. در برنامه‌ی دوم تیم یک روز وقت می‌گذارد تا سر قالب JSON توافق کند، پس frontend همزمان با ساخته شدن API روی objectهای ساختگی کد می‌زند و یکپارچه‌سازی کوتاه‌تر می‌شود. اسکریپت طول محتمل و مسیر بحرانی هر برنامه را چاپ می‌کند و بعد هر دو را با مدت‌های نامطمئن تکرار می‌کند.

*این آزمایش بخش «نقش‌های اصلی یک tech lead» از کتاب The Manager's Path را نشان می‌دهد، ص. ۳۲. پیاده‌سازی مال خود vault است: کارها و مدت‌ها و بلاتکلیفی ساختگی‌اند و مدت‌ها از یک توزیع مثلثی با seed ثابت کشیده می‌شوند.*

خروجی انگلیسی می‌ماند، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را بد نشان می‌دهند.

## اجرا

با Python نسخه‌ی ۳٫۱۰ به بالا، فقط کتابخانه‌ی استاندارد، و قطعی با seed ثابت:

```sh
python3 parallel_plan.py
```

## خروجی مورد انتظار

```text
Most likely durations (working days)

Wait for the API              24 days   critical path: design API -> build API -> build frontend -> integrate -> test and launch
Agree JSON contract first     17 days   critical path: design API -> agree JSON format -> build API -> integrate -> test and launch

10,000 seeded trials with uncertain durations

plan                         median  90th pct
Wait for the API               27.2      30.9
Agree JSON contract first      19.8      22.5
```

## به چه چیزی نگاه کنید

- انتظار کشیدن، frontend را روی مسیر بحرانی می‌نشاند: هفت روزش به هشت روز API اضافه می‌شود.
- با قرارداد توافق‌شده، frontend از مسیر بحرانی بیرون می‌افتد و تنها API سرعت را تعیین می‌کند؛ یک روز توافق حدود یک هفته می‌خرد.
- این فاصله وقتی مدت‌ها نامطمئن‌اند هم می‌ماند، و صدک نودم برنامه به‌اندازه‌ی میانه‌اش بهتر می‌شود. عددها کاملاً به کارهای ساختگی وابسته‌اند؛ شکل استدلال مال کتاب است.

## پیوندها

- یادداشت فصل: [فصل ۳: نقش tech lead](../../chapters/03-tech-lead.md)، بخش «نقش‌های اصلی یک tech lead»، ص. ۳۲
