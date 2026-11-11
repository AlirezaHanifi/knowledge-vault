# مفهوم write skew در snapshot isolation و SSI

یک موتور MVCC کوچک با خواندن از snapshot، قاعده‌ی first-committer-wins برای تعارض نوشتن‌ها، و نسخه‌ی ساده‌شده‌ای از بررسی serializable snapshot isolation. اول مثال پزشک‌های on-call کتاب را دوباره اجرا می‌کند و بعد ۱٬۰۰۰ ترتیب تصادفی از همان دو تراکنش را.

*این آزمایش بخش‌های «مفهوم write skew و phantom» و «مفهوم serializable snapshot isolation» از ویراست دوم DDIA را نشان می‌دهد (صص. ۳۰۳–۳۲۳). پیاده‌سازی مال خود vault است.*

## اجرا

با Python 3.10 یا جدیدتر، فقط کتابخانه‌ی استاندارد، و قطعی (با seed ثابت):

```sh
python3 mvcc.py
```

خروجی برنامه انگلیسی است، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را درست نشان نمی‌دهند.

## خروجی مورد انتظار

```text
Snapshot isolation, the book's interleaving:
    T1 (aaliyah) counts 2 doctors on call
    T2 (bryce) counts 2 doctors on call
    T1 (aaliyah) sets aaliyah off call
    T2 (bryce) sets bryce off call
    T1 (aaliyah) commits
    T2 (bryce) commits
  -> doctors still on call: 0  (aborted transactions: 0)

Serializable (SSI), the book's interleaving:
    T1 (aaliyah) counts 2 doctors on call
    T2 (bryce) counts 2 doctors on call
    T1 (aaliyah) sets aaliyah off call
    T2 (bryce) sets bryce off call
    T1 (aaliyah) commits
    T2 (bryce) ABORTED: read aaliyah which changed after the snapshot
  -> doctors still on call: 1  (aborted transactions: 1)

1,000 random interleavings of the same two transactions (38 happen to be serial):
  Snapshot isolation   nobody on call in  843 runs;    0 aborts (retry needed)
  Serializable (SSI)   nobody on call in    0 runs;  843 aborts (retry needed)
```

## به چه چیزی نگاه کنید

- در snapshot isolation دو تراکنش ردیف‌های متفاوتی می‌نویسند، پس تعارضی پیش نمی‌آید و هر دو commit می‌شوند؛ نتیجه این است که هیچ پزشکی on-call نمی‌ماند.
- بررسی SSI دقیقاً همان ترتیب‌هایی را abort می‌کند که قاعده را می‌شکستند (۸۴۳ از ۸۴۳) و هیچ‌کدام از ترتیب‌های امن را نه.
- هر abort یعنی یک retry که خود برنامه باید انجامش دهد؛ این هزینه‌ی کنترل concurrency خوش‌بینانه است.

## پیوندها

- یادداشت فصل: [فصل ۸: تراکنش‌ها](../../chapters/08-transactions.md)، بخش‌های «مفهوم write skew و phantom» و «مفهوم serializable snapshot isolation»، صص. ۳۰۳–۳۲۳
- در مرورگر: [گام‌به‌گام سطح‌های isolation](../../widgets/08-isolation.html)
