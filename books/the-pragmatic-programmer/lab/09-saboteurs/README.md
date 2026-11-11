# خرابکارها: تست‌ها باگ‌های کاشته‌شده را می‌گیرند؟

برای تست کردن تست‌ها، باگ بکارید و ببینید تست‌ها می‌فهمند یا نه. اسکریپت هشت mutant از تابع کوچک `clamp(x, lo, hi)` می‌سازد. آن‌هایی را که دقیقاً مثل اصل رفتار می‌کنند، یعنی mutantهای هم‌ارز، تشخیص می‌دهد، و بقیه را روی یک مجموعه‌ی ضعیف، یعنی یک تست روی مسیر خوش، و یک مجموعه‌ی قوی، یعنی هفت تست از جمله همان بیرون هر دو مرز، اجرا می‌کند. بعد از فضای حالت `a / (a + b)` کتاب با تا یک میلیون تست تصادفی نمونه می‌گیرد.

*این آزمایش «تست کردن تست‌ها» و «تست کردن جامع» در موضوع ۵۱ از کتاب The Pragmatic Programmer، یعنی جعبه‌ی شروع pragmatic، صص. ۴۵۷–۴۵۸ با tipهای ۹۲ و ۹۳ را نشان می‌دهد. تابع clamp و mutantها و تست‌ها مال vault است؛ تابع a / (a + b) با a و b از صفر تا ۹۹۹ مال کتاب. اولین تست شکست‌خورده از توزیع هندسی کشیده می‌شود و نه با کشیدن یکی‌یکی یک میلیون زوج.*

خروجی انگلیسی می‌ماند، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را بد نشان می‌دهند.

## اجرا

با Python نسخه‌ی ۳٫۱۰ به بالا، فقط کتابخانه‌ی استاندارد، و قطعی با seed ثابت:

```sh
python3 saboteurs.py
```

## خروجی مورد انتظار

```text
Mutants of clamp(x, lo, hi), run against a weak suite (1 test) and a strong suite (7 tests)

mutant                                weak    strong
< becomes <=                    (equivalent: same behaviour)
> becomes >=                    (equivalent: same behaviour)
return lo becomes return hi       SURVIVES    caught
return hi becomes return lo       SURVIVES    caught
x < lo becomes x < hi               caught    caught
x > hi becomes x > hi + 1         SURVIVES    caught
x < lo becomes x < lo - 1         SURVIVES    caught
return x becomes return x + 1       caught    caught

mutation score: weak 2/6, strong 6/6

State coverage: test(a, b) = a / (a + b) for a, b in 0..999 (1,000,000 states, one fails)

random tests  line coverage    runs (of 100) that hit a = b = 0
         100           100%                                   0
      10,000           100%                                   3
   1,000,000           100%                                  63

The chance of finding the state with k random tests is 1 - (1 - 1e-6)^k: about 63% at a million.
```

## به چه چیزی نگاه کنید

- دو تا از هشت mutant هم‌ارزند، چون تبدیل < به <= سر مرز clamp هیچ چیزی را عوض نمی‌کند: هیچ تستی هیچ‌وقت نمی‌توانست بگیردشان.
- مجموعه‌ی یک‌تستی می‌گذارد چهار از شش باگ واقعی جان سالم ببرند، گرچه قبول می‌شود و مسیر اصلی را اجرا.
- مجموعه‌ی قوی هر شش‌تا را می‌گیرد؛ و mutantهای یکی‌کم‌و‌زیاد که مرزی را جابه‌جا می‌کنند فقط با تست‌هایی گرفته می‌شوند که همان بیرونش‌اند، یعنی ۱۱ و ۱−.
- صد تست تصادفی روی `a / (a + b)` صد درصد پوشش خط می‌دهند و تقریباً هیچ‌وقت آن یک حالت شکست‌خورده را پیدا نمی‌کنند. حتی یک میلیون تست هم فقط حدود ۶۳٪ وقت‌ها پیدایش می‌کند: پوشش حالت را تست کنید و نه پوشش کد.

## پیوندها

- یادداشت فصل: [فصل ۹: پروژه‌های pragmatic](../../chapters/09-pragmatic-projects.md) — «تست کردن تست‌ها» و «تست کردن جامع»، صص. ۴۵۷–۴۵۸
