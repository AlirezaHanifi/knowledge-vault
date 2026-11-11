# عمل backfill افزایشی bounded در برابر unbounded

یک Incremental Loader با delta column که `ingestion_time >= start` را می‌خواند، در اجراهای معمولی مثل نسخه‌ی bounded رفتار می‌کند، چون چیز تازه‌تری هنوز وجود ندارد. ولی وقتی اجرای قدیمی‌ای را دوباره اجرا کنید، همه چیز را از آن اجرا تا حالا می‌خواند. این آزمایش دو ماه داده‌ی ساعتی می‌سازد و مقایسه می‌کند هر پیاده‌سازی سر backfill یک اجرای تک یا یک هفته‌ی کامل چقدر می‌خواند.

*این آزمایش «الگو: Incremental Loader» از کتاب Data Engineering Design Patterns را نشان می‌دهد، صص. ۱۲–۱۶؛ پنجره‌ی bounded `BETWEEN ingestion_time AND ingestion_time + INTERVAL '1 HOUR'` در ص. ۱۴ است. بار کاری ساختگی است و پیاده‌سازی مال خود vault.*

خروجی انگلیسی می‌ماند، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را بد نشان می‌دهند.

## اجرا

با Python نسخه‌ی ۳٫۱۰ به بالا، فقط کتابخانه‌ی استاندارد، و قطعی با seed ثابت:

```sh
python3 incremental_window.py
```

## خروجی مورد انتظار

```text
Source: 1,444,469 rows over 1440 hourly partitions (60 days)
A normal run reads one hour: about 1,003 rows

Backfilling a single past run
  run replayed         unbounded     bounded
  1 days ago              24,639         804
  7 days ago             170,731         979
  30 days ago            721,537         999
  59 days ago          1,420,335       1,057

Replaying the last 7 days (168 runs, one after another)
  unbounded total rows read: 14,431,698
  bounded total rows read:   170,731
  unbounded / bounded:       84.5x

Bounded runs read disjoint hours, so the 168 replays can also run in parallel.
```

## به چه چیزی نگاه کنید

- اجرای دوباره‌ی اجرایی از ۵۹ روز پیش با loader unbounded تقریباً کل جدول را می‌خواند. این backfill به بار‌گذاری کامل تبدیل شده، همان‌طور که کتاب هشدار می‌دهد.
- نسخه‌ی bounded هر سنی که اجرا داشته باشد یک ساعت می‌خواند، پس محاسبه‌اش پیش‌بینی‌پذیر است.
- اجرای دوباره‌ی یک هفته‌ی پشت‌سرهم بی کران تقریباً ۸۵ برابر گران‌تر است، چون هر اجرای دوباره، ساعت‌های همه‌ی اجراهای دوباره‌ی بعدی را هم می‌خواند.

## پیوندها

- یادداشت فصل: [فصل ۲: الگوهای طراحی ورود داده](../../chapters/02-data-ingestion-design-patterns.md) — «الگو: Incremental Loader»، صص. ۱۲–۱۶
- در مرورگر ببینید: [بار‌گذاری افزایشی و backfill](../../widgets/02-incremental-loader.html)
