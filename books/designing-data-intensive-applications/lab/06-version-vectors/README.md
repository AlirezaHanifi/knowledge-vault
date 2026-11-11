# نوشتن‌های concurrent و version vector

بخش اول مثال سبد خرید کتاب را، در شکل‌های ۶-۱۵ و ۶-۱۶، با الگوریتم تک‌replica که کتاب توصیف می‌کند دوباره اجرا می‌کند: سرور برای هر کلید نسخه نگه می‌دارد، هر مقداری را که هنوز بازنویسی نشده به شکل sibling نگه می‌دارد، و clientها پیش از نوشتن siblingها را merge می‌کنند. بخش دوم همین را با version vector به دو replica تعمیم می‌دهد.

*این آزمایش بخش «تشخیص نوشتن‌های concurrent» از ویراست دوم DDIA را نشان می‌دهد (صص. ۲۳۷–۲۴۳). پیاده‌سازی مال خود vault است.*

## اجرا

با Python 3.10 یا جدیدتر، فقط کتابخانه‌ی استاندارد، و قطعی:

```sh
python3 cart.py
```

خروجی برنامه انگلیسی است، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را درست نشان نمی‌دهند.

## خروجی مورد انتظار

```text
Part 1 - one replica, two clients (the book's shopping cart)
  client 1 adds milk   (based on v0) -> server v1: [milk]
  client 2 adds eggs   (based on v0) -> server v2: [milk] | [eggs]
  client 1 adds flour  (based on v1) -> server v3: [eggs] | [flour, milk]
  client 2 adds ham    (based on v2) -> server v4: [flour, milk] | [eggs, ham, milk]
  client 1 adds bacon  (based on v3) -> server v5: [eggs, ham, milk] | [bacon, eggs, flour, milk]
  a reader merging the siblings sees: [bacon, eggs, flour, ham, milk] - no item lost

Part 2 - two replicas, version vectors
  write [milk] at A           -> {'A': 1}; replicate to B: applied
  B writes [eggs, milk]       -> {'A': 1, 'B': 1}
  A writes [flour, milk]      -> {'A': 2}   (neither saw the other: concurrent)
  replicate B's write to A: concurrent sibling kept
  A now holds siblings: [flour, milk] | [eggs, milk]
  a client merges them at A   -> {'A': 3, 'B': 1}: [eggs, flour, milk]
  replicate to B: applied; B holds [eggs, flour, milk]
```

## به چه چیزی نگاه کنید

- هر نوشتن دقیقاً siblingهایی را بازنویسی می‌کند که client آن‌ها را دیده بود و siblingهای هم‌زمان را نگه می‌دارد؛ سرور هیچ‌وقت لازم ندارد مقدارها را بفهمد.
- عمل merge کردن siblingها با اجتماع مجموعه‌ها هیچ آیتمی را گم نمی‌کند؛ برای حذف کردن tombstone لازم است، که در یادداشت فصل آمده.
- مفهوم version vector تشخیص می‌دهد دو نوشتن روی replicaهای مختلف concurrent هستند، هر دو را نگه می‌دارد، و اجازه می‌دهد یک نوشتن merge‌شده‌ی بعدی جای هر دو را بگیرد.

## پیوندها

- یادداشت فصل: [فصل ۶: مفهوم replication](../../chapters/06-replication.md)، بخش «تشخیص نوشتن‌های concurrent»، صص. ۲۳۷–۲۴۳
- در مرورگر: [نوشتن‌های concurrent](../../widgets/06-concurrent-writes.html) و [مفهوم replication lag و quorum](../../widgets/06-replication.html)
