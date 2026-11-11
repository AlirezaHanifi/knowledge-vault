# تست‌های unit و طرح‌محور

اسکریپت catalogهای تصادفی می‌سازد که با طرح catalog می‌خوانند، بدلی کوچک برای JSON Schema Faker. هر تستی با حرف نخست عنوان کتاب نخست می‌جوید و می‌گذارد اعتبارسنجی مقدار بازگشتی خود تابع رد یا شکست را تصمیم بگیرد. اسکریپت ۱٬۰۰۰ seed را با جست‌وجو همان‌طور که چاپ شده اجرا می‌کند، بعد با چاره‌ی `"Not available"` دیو.

*تصویری از فصل ۱۲ کتاب Data-Oriented Programming، بخش ۱۲.۵، صص. ۲۶۲–۲۶۸ (شکل ۱۲.۳؛ listingهای ۱۲.۱۰ و ۱۲.۲۱ تا ۱۲.۲۸). آن سازنده و فهرست واژه‌هایش و شمار کتاب‌ها و نویسنده‌ها مال vault است، با seed.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 schema_based_tests.py
```

## خروجی چشم‌داشته

```text
First five seeds, as printed (listing 12.1):
  seed 1: false searchBooksByTitle returned an invalid value: data/0/authorNames/0 must be string
  seed 2: false searchBooksByTitle returned an invalid value: data/0/authorNames/0 must be string
  seed 3: false searchBooksByTitle returned an invalid value: data/1/authorNames/0 must be string
  seed 4: false searchBooksByTitle returned an invalid value: data/1/authorNames/0 must be string
  seed 5: false searchBooksByTitle returned an invalid value: data/0/authorNames/0 must be string

Seeds 1-1000, as printed: 134 passed, 866 failed (86.6%)
Seeds 1-1000, with "Not available" (listing 12.28): 1000 passed, 0 failed (0.0%)

Why some unfixed runs pass:
  matching books cite no author at all: 134
  matching books cite only authors that exist: 0
```

## به چه چیزی نگاه کنید

- بیشتر اجراها با `authorNames/… must be string` شکست می‌خورند. شناسه‌های نویسنده‌ی تصادفی در کتاب‌ها و کلیدهای تصادفی در `authorsById` تقریباً هیچ‌وقت رو هم نمی‌افتند، پس آن نام‌ها جاافتاده‌اند. همان اشکالی است که تست کتاب یافت.
- اجراهایی که رد می‌شوند خوش‌بختند: هر کدامشان موردی است که کتاب‌های خورنده هیچ نویسنده‌ای را گواه نمی‌آورند. هیچ‌کدام از آن رد نمی‌شود که نویسنده‌ای تصادفی بر بخت باشد.
- با آن چاره، نویسنده‌ای جاافتاده همان رشته‌ی `"Not available"` است، و هر ۱٬۰۰۰ اجرا رد می‌شود.
- هیچ ادعای صریحی نیست: سنجش حالت dev خود تابع خطا می‌اندازد، و آن تست همان را به `false` بدل می‌کند.

## مرتبط

- یادداشت فصل: [فصل ۱۲: اعتبارسنجی پیشرفته‌ی داده](../../chapters/12-advanced-data-validation.md) — بخش ۱۲.۵، صص. ۲۶۲–۲۶۸
