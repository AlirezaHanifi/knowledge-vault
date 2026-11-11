# گرفتن و replay

زمینه‌ی تابعی، یعنی آرگومان‌هایش، را در فایلی JSON می‌ریزد که با زمینه و UUID نام گرفته، بعد synchronous بازش می‌خواند و آن صدا زدن را replay. آن هشت پرسش تست را روی سه version جست‌وجو، روی catalog گرفته‌شده، اجرا می‌کند. در پایان نشان می‌دهد ریختنی asynchronous چه ثبت می‌کند وقتی صداکننده پیش می‌رود و داده را عوض.

*تصویری از فصل ۱۵ کتاب Data-Oriented Programming، صص. ۳۱۴–۳۲۸ (listingهای ۱۵.۵ تا ۱۵.۲۶). فایل‌ها در پوشه‌ای transient نوشته و برداشته می‌شوند. UUIDها با seedاند و آن مسابقه با رویدادها ترتیب خورده، پس خروجی قطعی است. برداشتن Watchmen صحنه‌ی vault است.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 capture_replay.py
```

## خروجی چشم‌داشته

```text
1. Capture: console.log versus JSON.stringify (listings 15.5-15.6)
   console.log:    I like the word "reproducibility"
   JSON.stringify: "I like the word \"reproducibility\""
   pasting the console.log output back: fails (Expecting value)
   pasting the JSON output back: OK

2. Dump the context of searchBooksByTitle(catalog, 'Watch'), then replay it
   wrote test-data/searchBooksByTitle-85750621-02fb-4d4f-b57f-bc5af71a1bfc.json (990 bytes)
   original: [{"title": "Watchmen", "isbn": "978-1779501127", "authorNames": ["Alan Moore", "Dave Gibbons"]}]
   replayed: [{"title": "Watchmen", "isbn": "978-1779501127", "authorNames": ["Alan Moore", "Dave Gibbons"]}] | identical: True

3. The eight queries of listings 15.25-15.26 on the captured catalog
   query       expected 15.8 lowercase startsWith   15.12 word startsWith       15.24 lowercase \b regex
   "Habit"     book     FAIL none                   ok   found                  ok   found
   "habit"     book     FAIL none                   FAIL none                   ok   found
   "7 Habit"   book     ok   found                  FAIL none                   ok   found
   "habits of" book     FAIL none                   FAIL none                   ok   found
   "abit"      nothing  ok   none                   ok   none                   ok   none
   "bit"       nothing  ok   none                   ok   none                   ok   none
   "7 abit"    nothing  ok   none                   ok   none                   ok   none
   "habit of"  nothing  ok   none                   ok   none                   ok   none
   passing:            5 / 8                       5 / 8                       8 / 8

4. An asynchronous dump while the caller goes on and withdraws Watchmen
   mutable   data: the function saw 1 book(s); the replay finds 0 -> NOT reproduced
   immutable data: the function saw 1 book(s); the replay finds 1 -> reproduced
```

## به چه چیزی نگاه کنید

- خروجی `console.log` گیومه‌ها و ممیزهای معکوس را گم می‌کند، پس بازچسباندنی نیست. قالب JSON می‌تواند.
- نام آن فایل همان UUID را دارد؛ و همان‌طور که چاپ شده، listing ۱۵.۱۵ هیچ‌وقت به‌هم‌چسبانی‌اش نمی‌کند؛ کادر vault در درس را ببینید. خروجی replay‌شده با اصل برابر است.
- تابع حرف‌کوچک `startsWith` از listing ۱۵.۸ و پیشوند واژه‌ی listing ۱۵.۱۲ هر کدام ۵ پرسش از ۸ را رد می‌کنند و در پرسش‌های مختلفی شکست می‌خورند. عبارت باقاعده‌ی حرف‌کوچک `\b` از listing ۱۵.۲۴ هر ۸ را رد می‌کند.
- با داده‌ی تغییرپذیر، آن ریختن asynchronous catalogی را می‌نویسد که تابع هیچ‌وقت ندید، و آن replay هیچ نمی‌یابد. با داده‌ی تغییرناپذیر، صداکننده versionی تازه می‌سازد، و آن ریختن دقیقاً همان را ثبت می‌کند که تابع گرفت (ص. ۳۲۶).

## مرتبط

- یادداشت فصل: [فصل ۱۵: اشکال‌زدایی](../../chapters/15-debugging.md) — بخش‌های ۱۵.۲ تا ۱۵.۴، صص. ۳۱۴–۳۲۸
