# یک LSM-tree کوچک

یک storage engine کامل و کوچک LSM در حدود ۲۰۰ خط: write-ahead log، memtable، SSTableهایی که به شکل فایل مرتب با sparse index نوشته می‌شوند، یعنی یک ورودی برای هر بلوک ۱۶ کلیدی، Bloom filter برای هر SSTable، compaction از نوع size-tiered، tombstone برای حذف، و بازیابی بعد از crash با replay کردن WAL. یک workload نامتوازن هر خواندن را با یک dict مرجع مقایسه می‌کند.

*این آزمایش بخش «ذخیره‌سازی log-structured» از ویراست دوم DDIA را نشان می‌دهد (صص. ۱۱۸–۱۲۵). پیاده‌سازی مال خود vault است.*

## اجرا

با Python 3.10 یا جدیدتر، فقط کتابخانه‌ی استاندارد، و قطعی با seed ثابت:

```sh
python3 lsm.py
```

خروجی برنامه انگلیسی است، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را درست نشان نمی‌دهند.

## خروجی مورد انتظار

```text
Workload: 30,000 writes (5% deletes) over 5,000 keys, memtable limit 500
  SSTables on disk now:         2
  compactions run:              17
  write amplification:          4.09x (bytes written to disk / bytes written by the application)
  SSTable reads per get, without Bloom filters  1.91
  SSTable reads per get, with Bloom filters     0.45
  Bloom false-positive rate:    0.94% (10 bits/key, 7 hashes)

Crash: lost 245 memtable entries; replayed 258 WAL records; all 4901 keys correct after recovery: True
```

## به چه چیزی نگاه کنید

- مقدار write amplification حدود ۴ برابر است: هر نوشتن منطقی یک بار در WAL، یک بار در SSTable هنگام flush و دوباره در هر compactionی که بازنویسی‌اش می‌کند نوشته می‌شود.
- فیلتر Bloom تعداد SSTableهایی را که هر جست‌وجو می‌خواند حدود ۴ برابر کم می‌کند؛ بیشتر این صرفه‌جویی از کلیدهایی می‌آید که وجود ندارند.
- نرخ false positive اندازه‌گیری‌شده، حدود ۱٪، با عدد کتاب برای ۱۰ بیت به ازای هر کلید می‌خواند.
- بعد از یک crash شبیه‌سازی‌شده، memtable از روی WAL دوباره ساخته می‌شود و همه‌ی کلیدها درست خوانده می‌شوند.

## پیوندها

- یادداشت فصل: [فصل ۴: ذخیره‌سازی و بازیابی](../../chapters/04-storage-and-retrieval.md)، بخش «ذخیره‌سازی log-structured»، صص. ۱۱۸–۱۲۵
- در مرورگر: [درون یک LSM-tree](../../widgets/04-lsm-tree.html)
