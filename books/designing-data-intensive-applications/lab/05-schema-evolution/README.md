# فرمت‌های encoding باینری و تکامل schema

دو encoder کوچک: یکی برای wire format در Protocol Buffers، یعنی field tag و wire type و varint، و یکی برای قالب باینری Avro، که tag ندارد، zigzag varint دارد و writer's schema را با reader's schema تطبیق می‌دهد. رکورد نمونه‌ی کتاب در مثال ۵-۲ را encode می‌کند و اندازه‌هایی را که کتاب گزارش می‌دهد بازتولید می‌کند، یعنی ۸۱ بایت JSON، ۳۳ بایت Protocol Buffers و ۳۲ بایت Avro، و بعد forward و backward compatibility را نشان می‌دهد.

*این آزمایش بخش‌های «قالب Protocol Buffers» و «قالب Avro» از ویراست دوم DDIA را نشان می‌دهد (صص. ۱۶۹–۱۷۷). پیاده‌سازی مال خود vault است.*

## اجرا

با Python 3.10 یا جدیدتر، فقط کتابخانه‌ی استاندارد، و قطعی:

```sh
python3 encoding.py
```

خروجی برنامه انگلیسی است، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را درست نشان نمی‌دهند.

## خروجی مورد انتظار

```text
Encoded size of the book's example record (Example 5-2):
  JSON (no whitespace)        81 bytes
  Protocol Buffers style      33 bytes   0a 06 4d 61 72 74 69 6e 10 b9 0a 1a 0b 64 61 79 64 72 65 61 6d 69 6e 67 1a 07 68 61 63 6b 69 6e 67
  Avro style                  32 bytes   0c 4d 61 72 74 69 6e 02 f2 14 04 16 64 61 79 64 72 65 61 6d 69 6e 67 0e 68 61 63 6b 69 6e 67 00

Protocol Buffers: compatibility through tag numbers
  forward  (v1 reader, v2 data): skipped unknown tag(s) [4]; read {'userName': 'Martin', 'favoriteNumber': 1337, 'interests': ['daydreaming', 'hacking']}
  backward (v2 reader, v1 data): email absent -> '<default>'

Avro: compatibility through writer/reader schema resolution
  backward (v2 reader, v1 data): {'userName': 'Martin', 'favoriteNumber': 1337, 'interests': ['daydreaming', 'hacking'], 'email': None}
  forward  (v1 reader, v2 data): {'userName': 'Martin', 'favoriteNumber': 1337, 'interests': ['daydreaming', 'hacking']}
  adding a field WITHOUT a default breaks backward compatibility: reader requires field 'email' with no default
```

## به چه چیزی نگاه کنید

- بایت به بایت: دنباله‌ی `0a 06 4d 61 72 74 69 6e` یعنی tag شماره‌ی ۱، wire type شماره‌ی ۲، طول ۶ و «Martin».
- قالب Protocol Buffers به forward compatibility می‌رسد چون خواننده‌ی قدیم می‌تواند از tag ناشناخته بگذرد؛ wire type می‌گوید چند بایت را باید رد کند.
- قالب Avro اصلاً tag ندارد؛ سازگاری از تطبیق writer's schema با reader's schema بر اساس اسم فیلد می‌آید، و برای همین فیلد تازه default لازم دارد.

## پیوندها

- یادداشت فصل: [فصل ۵: قالب‌های encoding و تکامل](../../chapters/05-encoding-and-evolution.md)، بخش‌های «قالب Protocol Buffers» و «قالب Avro»، صص. ۱۶۹–۱۷۷
- در مرورگر: [یک رکورد، چهار encoding](../../widgets/05-encodings.html) و [writer's schema و reader's schema](../../widgets/05-schema-evolution.html)
