# الگوی three-way merge به Python

درگاهی از فاز commit این فصل: تابع `diff` ساختاری و `informationPaths` و `havePathInCommon` و آن درهم‌آمیزی و `reconcile`. کتابخانه‌ی ناچیز listingهای ۵.۶ و ۵.۷ را replay می‌کند: mutationی سال نشر Watchmen را عوض می‌کند و آن یکی عنوانش و نام نویسنده‌ای را. بعد دو دام کد چاپی را نشان می‌دهد. و در پایان می‌سنجد که دو mutation concurrent چند بار abort می‌شوند وقتی روی فیلدهای کم‌تری جمع می‌شوند.

*تصویری از فصل ۵ کتاب Data-Oriented Programming، بخش‌های ۵.۲ تا ۵.۵، صص. ۹۴–۱۰۸ (listingهای ۵.۴ تا ۵.۱۶). آزمون abort، با یک فیلد تصادفی برای هر جهشی، مال vault است، با seed.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 three_way_merge.py
```

## خروجی چشم‌داشته

```text
diff(previous, next):    {"catalog": {"booksByIsbn": {"978-1779501127": {"publicationYear": 1986}}}}
diff(previous, current): {"catalog": {"booksByIsbn": {"978-1779501127": {"title": "The Watchmen"}}, "authorsById": {"dave-gibbons": {"name": "David Chester Gibbons"}}}}
paths of next's diff:    [['catalog', 'booksByIsbn', '978-1779501127', 'publicationYear']]
paths of current's diff: [['catalog', 'booksByIsbn', '978-1779501127', 'title'], ['catalog', 'authorsById', 'dave-gibbons', 'name']]
table 5.4, array addition: diff([1], [1, 2]) = [null, 2]

reconcile(current, previous, next), condition fixed:
{
 "catalog": {
  "booksByIsbn": {
   "978-1779501127": {
    "isbn": "978-1779501127",
    "title": "The Watchmen",
    "publicationYear": 1986,
    "authorIds": [
     "alan-moore",
     "dave-gibbons"
    ]
   }
  },
  "authorsById": {
   "alan-moore": {
    "name": "Alan Moore",
    "bookIsbns": [
     "978-1779501127"
    ]
   },
   "dave-gibbons": {
    "name": "David Chester Gibbons",
    "bookIsbns": [
     "978-1779501127"
    ]
   }
  }
 }
}

Fast-forward when nothing else committed: True
Listing 5.16 as printed, on these NON-conflicting mutations: Conflicting concurrent mutations.
Both set publicationYear, paths compared by value: Conflicting concurrent mutations.
Both set publicationYear, paths compared by identity: merged silently, year = 1986 (1988 lost)

Two concurrent mutations, each setting one random field out of F (1,000 trials each)
   F  aborted  abort rate
   1     1000     100.0%
   2      484      48.4%
   4      263      26.3%
   8      119      11.9%
  16       63       6.3%
  64       17       1.7%
```

## به چه چیزی نگاه کنید

- با کد همان‌طور که فهرست شده، آن عوض شدن نام زیر `catalog` می‌نشیند، پس خروجی درهم‌آمیخته یک `catalog` تنها با هر سه تغییر دارد. آن از خروجی چاپی listing ۵.۱۴ فرق دارد؛ کادر vault در درس را ببینید.
- عبارت `diff([1], [1, 2])` مقدار `[null, 2]` می‌دهد، مانند جدول ۵.۴: عضوهای برابر null می‌شوند.
- کد listing ۵.۱۶ همان‌طور که چاپ شده روی همان مثال بی‌ناسازی خود کتاب خطای *Conflicting concurrent mutations* می‌اندازد، چون شرطش برگشته است.
- سنجیدن مسیرها با همانندی، آن‌طور که `_.intersection` از Lodash برای آرایه‌ها می‌کند، هیچ‌وقت مسیری مشترک نمی‌یابد. بعد دو mutation روی همان یک سال خاموش درهم می‌آمیزند، و یکی‌شان گم می‌شود.
- با یک فیلد تصادفی برای هر کدام، نرخ abort حدود ۱ بخش بر F است. concurrency خوش‌بینانه وقتی جواب می‌دهد که mutationها کم به همان فیلدها دست بزنند.

## مرتبط

- یادداشت فصل: [فصل ۵: کنترل پایه‌ی concurrency](../../chapters/05-basic-concurrency-control.md) — بخش‌های ۵.۲ تا ۵.۵، صص. ۹۴–۱۰۸
