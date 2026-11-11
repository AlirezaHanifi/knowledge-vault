# تست‌های property باگ انبار را پیدا می‌کنند

کلاس `Warehouse` کتاب unit testهای دستی‌نوشته‌اش را قبول می‌شود. این اسکریپت یک تست‌کننده‌ی property‌محور ریز با کتابخانه‌ی استاندارد می‌سازد: سفارش می‌سازد، یعنی قلم از کفش یا کلاه و تعداد یک تا چهار مثل کتاب، بررسی می‌کند که موجودی برداشته‌شده به‌علاوه‌ی موجودی مانده برابر موجودی اصلی است، و هر شکستی را حریصانه به سمت اولین قلم و تعدادهای کمتر کوچک می‌کند. property را روی `in_stock(item)` باگ‌دار و `in_stock(item, quantity)` اصلاح‌شده اجرا می‌کند، و همچنین با تعدادهای تا بیست.

*این آزمایش «یافتن فرض‌های بد» در موضوع ۴۲ از کتاب The Pragmatic Programmer، یعنی تست property‌محور، صص. ۳۷۸–۳۸۳ را نشان می‌دهد: کلاس Warehouse و `order` و property و اصلاح دنبال کتاب می‌روند، یعنی `proptest/stock.py` و `stock1.py`. سازنده و کوچک‌کننده مال vault است؛ کتاب از Hypothesis استفاده می‌کند.*

خروجی انگلیسی می‌ماند، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را بد نشان می‌دهند.

## اجرا

با Python نسخه‌ی ۳٫۱۰ به بالا، فقط کتابخانه‌ی استاندارد، و قطعی با seed ثابت:

```sh
python3 warehouse_properties.py
```

## خروجی مورد انتظار

```text
== buggy in_stock(item)
   hand-written unit tests: pass
   quantity 1-4  seed 1: FAIL after   3 case(s): hats, 4 -> shrunk to hats, 3 in 7 step(s): Exception: Oversold hats
   quantity 1-4  seed 2: FAIL after   6 case(s): hats, 4 -> shrunk to hats, 3 in 7 step(s): Exception: Oversold hats
   quantity 1-4  seed 3: FAIL after   2 case(s): hats, 4 -> shrunk to hats, 3 in 7 step(s): Exception: Oversold hats
   quantity 1-20 seed 1: FAIL after   1 case(s): shoes, 19 -> shrunk to shoes, 11 in 21 step(s): Exception: Oversold shoes
   quantity 1-20 seed 2: FAIL after   2 case(s): shoes, 12 -> shrunk to shoes, 11 in 21 step(s): Exception: Oversold shoes
   quantity 1-20 seed 3: FAIL after   1 case(s): shoes, 19 -> shrunk to shoes, 11 in 21 step(s): Exception: Oversold shoes

== fixed in_stock(item, qty)
   hand-written unit tests: pass
   quantity 1-4  seed 1: pass (100 cases)
   quantity 1-4  seed 2: pass (100 cases)
   quantity 1-4  seed 3: pass (100 cases)
   quantity 1-20 seed 1: pass (100 cases)
   quantity 1-20 seed 2: pass (100 cases)
   quantity 1-20 seed 3: pass (100 cases)
```

## به چه چیزی نگاه کنید

- تست‌های unit برای هر دو نسخه قبول می‌شوند: هیچ‌وقت بیشتر از یک کلاه سفارش نمی‌دهند.
- با راهبرد کتاب، هر seedی ظرف چند حالت شکست می‌خورد و تا `hats, 3` کوچک می‌شود، یعنی نمونه‌ی ناقض کتاب: دو کلاه هست، و `in_stock` فقط دست‌کم یکی را بررسی می‌کرد.
- با تعدادهای تا بیست، کوچک‌کننده به‌جایش روی `shoes, 11` می‌نشیند: شکست کمینه‌ی متفاوتی از همان باگ. راهبرد ورودی تعیین می‌کند کدام نمونه‌ی نقض را می‌بینید.
- نسخه‌ی اصلاح‌شده هر اجرا را قبول می‌شود، پس همان‌طور که کتاب توصیه می‌کند `hats, 3` را به یک unit test معمولی تبدیل کنید تا باگ برنگردد.

## پیوندها

- یادداشت فصل: [فصل ۷: وقتی کد می‌زنید](../../chapters/07-while-you-are-coding.md) — موضوع ۴۲، تست property‌محور، صص. ۳۷۸–۳۸۳
