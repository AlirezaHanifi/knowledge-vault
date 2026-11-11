# یک vector persistent به Python

فهرستی ذخیره‌شده به‌شکل درختی از tuple که node‌هایش دست‌بالا *b* عضو یا فرزند دارند. به‌روز کردن یک عضو تنها مسیر از ریشه تا آن برگ را کپی می‌کند. اسکریپت nodeها و خانه‌های کپی‌شده در هر به‌روزرسانی را برای ضریب شاخه‌های ۲ تا ۶۴ می‌شمارد، کران‌های عمق کتاب را چاپ می‌کند، و حافظه‌ای را که ۱٬۰۰۱ version نگه می‌دارد می‌سنجد، همه در برابر کپی کردن فهرستی ۱۰۰٬۰۰۰عضوی.

*تصویری از فصل ۹ کتاب Data-Oriented Programming، بخش ۹.۲، صص. ۱۷۸–۱۸۳: کپی مسیر، عمق log₂ N در برابر log₃₂ N، و آن کران ده‌میلیاردی. پیاده‌سازی مال vault است: vectorی با اندازه‌ی ثابت بی بهینه‌سازی‌های دُم که کتابخانه‌های production دارند، با seed.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 persistent_vector.py
```

## خروجی چشم‌داشته

```text
Updating one element of a 100,000-element list
        strategy  depth  nodes copied  slots copied
 copy whole list      -             1       100,000
  path copy, b=2     17            17            34
  path copy, b=4      9             9            34
  path copy, b=8      6             6            44
 path copy, b=16      5             5            66
 path copy, b=32      4             4           100
 path copy, b=64      3             3           153

Depth bounds from the book (p. 182): log2 and log32 of the collection size
  N =          1,000   log2 N =  9.97   log32 N = 1.99
  N =        100,000   log2 N = 16.61   log32 N = 3.32
  N =     10,000,000   log2 N = 23.25   log32 N = 4.65
  N = 10,000,000,000   log2 N = 33.22   log32 N = 6.64

Memory kept by 1,001 versions (1,000 random single-element updates), N = 100,000
        strategy     slots kept  vs one version
 copy whole list    100,100,000           1001x
  path copy, b=2        233,953           1.17x
 path copy, b=32        202,539           1.96x
```

## به چه چیزی نگاه کنید

- آن عمق از ۱۷ سطح در *b* = ۲ به ۴ سطح در *b* = ۳۲ می‌افتد. همان log₂ در برابر log₃₂ است که کتاب حساب می‌کند، رو به بالا گرد‌شده.
- خانه‌های کپی‌شده در هر به‌روزرسانی با *b* رشد می‌کنند، یعنی ۳۴ در *b* = ۲ و ۱۰۰ در *b* = ۳۲، در برابر ۱۰۰٬۰۰۰ برای کپی کامل. کتاب ۳۲ را برای CPU برمی‌گزیند: یک آرایه‌ی ۳۲خانه‌ای جفتی دسترسی cache است، ارزان‌تر از دواندن میان ۱۷ node.
- عددهای کتاب: مقدار log₃₂ از ده میلیارد همان ۶٫۶۴ است، که عملاً ثابتش می‌نامد.
- هزار version در *b* = ۳۲ حدود دو برابر خانه‌های یک version را نگه می‌دارند، و با کپی کامل هزار برابر را.

## مرتبط

- یادداشت فصل: [فصل ۹: ساختارهای داده‌ی persistent](../../chapters/09-persistent-data-structures.md) — بخش ۹.۲، صص. ۱۷۸–۱۸۳
