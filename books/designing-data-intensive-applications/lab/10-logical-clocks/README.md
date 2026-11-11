# ساعت فیزیکی، Lamport clock و hybrid logical clock

سه node که ساعت‌های time-of-day آن‌ها تا ±۴۰ میلی‌ثانیه skew دارند پیام‌های چت رد و بدل می‌کنند، و خیلی از پیام‌ها پاسخ پیام‌های قبلی‌اند. هر پیام به سه روش برچسب می‌خورد و ما پاسخ‌هایی را می‌شماریم که مرتب کردن بر اساس timestamp آن‌ها را پیش از پیامی که جوابش را می‌دهند می‌گذارد.

*این آزمایش بخش «مفهوم logical clock» از ویراست دوم DDIA را نشان می‌دهد (صص. ۴۲۰–۴۲۳). پیاده‌سازی مال خود vault است.*

## اجرا

با Python 3.10 یا جدیدتر، فقط کتابخانه‌ی استاندارد، و قطعی (با seed ثابت):

```sh
python3 clocks.py
```

خروجی برنامه انگلیسی است، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را درست نشان نمی‌دهند.

## خروجی مورد انتظار

```text
300 messages, 192 of them replies; clock skew {'Aaliyah': 40, 'Bryce': -35, 'Caleb': 0}

timestamp scheme     replies ordered before their parent    max |ts - true time|
physical                                              39                   40 ms
lamport                                                0         n/a (a counter)
hlc                                                    0                   40 ms

Example violation with physical clocks:
  message by Caleb    true time 1118  physical 1118  lamport 6  hlc 1118.0
  reply   by Bryce    true time 1151  physical 1116  lamport 7  hlc 1118.1
```

## به چه چیزی نگاه کنید

- مفهوم timestamp فیزیکی حدود ۲۰٪ پاسخ‌ها را پیش از پیام اصلی‌شان می‌گذارد؛ ساعتی که ۳۵ میلی‌ثانیه کند باشد کافی است.
- مفهوم Lamport timestamp هرگز ترتیب علّی را نقض نمی‌کند، اما شمارنده‌ای است که ربطی به ساعت دیواری ندارد.
- مفهوم hybrid logical clock هم هرگز ترتیب علّی را نقض نمی‌کند و فاصله‌اش از زمان واقعی در حد همان clock skew می‌ماند.

## پیوندها

- یادداشت فصل: [فصل ۱۰: مفهوم consistency و consensus](../../chapters/10-consistency-and-consensus.md)، بخش «مفهوم logical clock»، صص. ۴۲۰–۴۲۳
