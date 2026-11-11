# ابزارهای دست‌ساز داده

توابع `update` و `flatMap` و `countByBoolField` و `unwind` به Python، اجراشده روی داده‌ی این فصل: آن map درآمد، آن دو کتاب با نسخه‌هایشان، و سبد جو. بعد اسکریپت `update` و `unwind` را باز با `set`ی اجرا می‌کند که سر جا mutation می‌دهد، آن‌طور که `_.set` پیش‌فرض Lodash می‌کند.

*تصویری از فصل ۱۴ کتاب Data-Oriented Programming، صص. ۲۹۶–۳۰۹ (listingهای ۱۴.۳ تا ۱۴.۱۹). نویسنده‌ی دوباره در قدم ۱ مثال vault است؛ و سنجش set mutationی کادر vault در درس را تصویر می‌کند.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 custom_data_tools.py
```

## خروجی چشم‌داشته

```text
update (listings 14.2-14.4)
  update(m, 'income', x * 2): {'position': 'manager', 'income': 200000} | m is unchanged: {'position': 'manager', 'income': 100000}
  removeAuthorDuplicates: ['Alan Moore', 'Dave Gibbons']

flatMap (listings 14.5-14.9)
  map:     [["alan-moore", "dave-gibbons"], ["sean-covey", "stephen-covey"]]
  flatMap: ["alan-moore", "dave-gibbons", "sean-covey", "stephen-covey"]

countByBoolField (listings 14.13-14.15)
  test of listing 14.14: {'aTrue': 3, 'aFalse': 1}
  book items: {'lent': 2, 'notLent': 1} -> lendingRatio = 0.6667

unwind (listings 14.17-14.19)
   {"customer-id": "joe", "items": {"item": "phone", "quantity": 1}}
   {"customer-id": "joe", "items": {"item": "pencil", "quantity": 10}}
  cart is unchanged: [{"item": "phone", "quantity": 1}, {"item": "pencil", "quantity": 10}]
  books grouped by library:
    nyc-central-lib: Watchmen (book-item-1), 7 Habits of Highly Effective People (book-item-17)
    hudson-park-lib: 7 Habits of Highly Effective People (book-item-123)

The same with a mutating set (the vault note in the lesson)
   {"customer-id": "joe", "items": {"item": "pencil", "quantity": 10}}
   {"customer-id": "joe", "items": {"item": "pencil", "quantity": 10}}
  both results are the same object: True | the cart itself was changed: {"item": "pencil", "quantity": 10}
  update with a mutating set changes its input: m = {'income': 200000} | same object: True
  books grouped by library: {'nyc-central-lib': ['book-item-1', 'book-item-17', 'book-item-17']}
```

## به چه چیزی نگاه کنید

- تابع `update` mapی تازه برمی‌گرداند و ورودی‌اش را رها می‌کند؛ تابع `countByBoolField` تست listing ۱۴.۱۴ را رد می‌کند، و نسبت قرض آن نمونه ۲ بخش بر ۳ است.
- تابع `unwind` آن سبد را به دو map با یک نسخه برای هر کدام بدل می‌کند، و خود سبد دست‌نخورده می‌ماند.
- گروه کردن کتاب‌های بازشده با `bookItems.libId` کتاب Watchmen و یک نسخه از 7 Habits را در nyc-central-lib می‌گذارد، و آن نسخه‌ی دیگر را در hudson-park-lib.
- با setی جهشی، تابع `unwind` همان یک شیء را دو بار برمی‌گرداند که هر دو نسخه‌ی آخر را نشان می‌دهند، و آن سبد را عوض می‌کند. تابع `update` ورودی‌اش را عوض می‌کند. بعد آن گروه کردن در یک کتابخانه با نسخه‌ای دوباره فرو می‌ریزد.

## مرتبط

- یادداشت فصل: [فصل ۱۴: دست‌کاری پیشرفته‌ی داده](../../chapters/14-advanced-data-manipulation.md) — بخش‌های ۱۴.۱ تا ۱۴.۴، صص. ۲۹۶–۳۰۹
