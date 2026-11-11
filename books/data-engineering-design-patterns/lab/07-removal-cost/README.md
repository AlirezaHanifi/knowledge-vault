# هزینه‌ی حذف داده‌ی شخصی

وقتی کاربری می‌خواهد فراموش شود، چقدر باید بازنویسی شود؟ این آزمایش یک مجموعه‌داده‌ی ساختگی بازدید با نود پارتیشن روزانه و چهار فایل در هر پارتیشن می‌سازد، به‌علاوه‌ی یک کاربر سنگین با همان دو هزار بازدید کتاب. دو روش را مقایسه می‌کند. الگوی **In-Place Overwriter** هر فایلی را که یکی از ردیف‌های آن کاربر را دارد بازنویسی می‌کند. با **Vertical Partitioner**، ویژگی‌های شخصی کاربر یک‌بار در جدول جدای user context ذخیره می‌شوند. بعد مقایسه می‌کند که صد درخواست حذف را یکی‌یکی پردازش کنید یا در یک اجرا دسته کنید.

*این آزمایش «الگو: Vertical Partitioner» و «الگو: In-Place Overwriter» از کتاب Data Engineering Design Patterns را نشان می‌دهد، صص. ۱۹۸–۲۰۷. پیامد هزینه، یعنی دو هزار رکورد در برابر یکی و دسته کردن درخواست‌های حذف، در ص. ۲۰۵ است. چیدمان داده ساختگی است و پیاده‌سازی مال خود vault.*

خروجی انگلیسی می‌ماند، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را بد نشان می‌دهند.

## اجرا

با Python نسخه‌ی ۳٫۱۰ به بالا، فقط کتابخانه‌ی استاندارد، و قطعی با seed ثابت:

```sh
python3 removal_cost.py
```

## خروجی مورد انتظار

```text
Visits dataset: 296,580 rows in 360 files (90 days x 4 files)
User context table (Vertical Partitioner): 5,000 rows in 20 files

Removing user 0 (2,000 visits)
                          rows deleted  files rewritten  rows rewritten  MB written
  In-Place Overwriter            2,000              360         296,580       88.97
  Vertical Partitioner               1                1             250        0.03

A median user (25 visits) still makes the In-Place Overwriter rewrite 25 files (21,012 rows)

100 removal requests, In-Place Overwriter
  processed one by one:   3,204,008 rows rewritten
  batched into one run:   296,580 rows rewritten (10.8x less)
```

## به چه چیزی نگاه کنید

- دو هزار بازدید کاربر سنگین روی هر فایلی پخش شده، پس In-Place Overwriter برای حذفشان کل مجموعه‌داده را بازنویسی می‌کند.
- الگوی Vertical Partitioner یک ردیف حذف و یک فایل کوچک بازنویسی می‌کند. جدول بازدیدها فقط `user_id` را نگه می‌دارد، که دیگر به هیچ چیز شخصی وصل نیست.
- حتی کاربری میانه هم به ده‌ها فایل می‌خورد، چون بازدیدها بین روزها پخش‌اند.
- دسته کردن درخواست‌های حذف، همان‌طور که کتاب توصیه می‌کند، هر فایل را یک‌بار بازنویسی می‌کند و نه یک‌بار برای هر درخواست.

## پیوندها

- یادداشت فصل: [فصل ۷: الگوهای طراحی امنیت داده](../../chapters/07-data-security-design-patterns.md) — «حذف داده»، صص. ۱۹۸–۲۰۷
