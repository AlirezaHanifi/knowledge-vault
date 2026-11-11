# ردیف‌ها به‌شکل map با SQLite

جدول‌های ۱۰.۱ تا ۱۰.۳ را در پایگاه داده‌ای SQLite در حافظه بار می‌کند، با row factoryی که هر ردیفی را به‌شکل dictionary برمی‌گرداند: همان قدم راننده در شکل ۱۰.۲. بعد جست‌وجوی این فصل را همان‌طور که چاپ شده و تصحیح‌شده اجرا می‌کند، و ردیف‌ها را با آن طرح اعتبارسنجی. در پایان، کلیدها را با یک تابع عمومی برای کتاب‌ها و کاربران نام‌عوض می‌کند، و آن join سه‌ردیفی را در دو کتاب گرد.

*تصویری از فصل ۱۰ کتاب Data-Oriented Programming، صص. ۱۹۸–۲۱۸ (listingهای ۱۰.۴ تا ۱۰.۲۶). پایگاه SQLite جای PostgreSQL کتاب می‌نشیند؛ و جایگزین `?` است به‌جای `$1`.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 rows_as_maps.py
```

## خروجی چشم‌داشته

```text
1. The query of listing 10.6, as printed: '%$1%' inside the quotes
    ProgrammingError: Incorrect number of bindings supplied. The current statement uses 0, and there are 1 supplied.
   (inside a quoted literal the placeholder is just text)

2. Corrected: LIKE '%' || ? || '%', still selecting only title and isbn
   rows: [{"title": "The Power of Habit", "isbn": "978-0812981605"}, {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274"}]
   validation: ["data/0 must have required property 'publication_year'", "data/1 must have required property 'publication_year'"]

3. Selecting publication_year too, as the schema requires
   rows: [{"title": "The Power of Habit", "isbn": "978-0812981605", "publication_year": 2012}, {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274", "publication_year": 1989}]
   validation: valid
   JSON (late binding: the year is written without quotes): {"title": "The Power of Habit", "isbn": "978-0812981605", "publication_year": 2012}
   with a case-sensitive LIKE, as in PostgreSQL: 0 rows

4. renameResultKeys, the same function for books and users (listings 10.13-10.16)
   [{"isbn": "978-0812981605", "bookTitle": "The Power of Habit", "publicationYear": 2012}, {"isbn": "978-1982137274", "bookTitle": "7 Habits of Highly Effective People", "publicationYear": 1989}]
   [{"encryptedPassword": "secret-pass", "userEmail": "jennie@gmail.com"}, {"encryptedPassword": "my-secret", "userEmail": "franck@hotmail.com"}]

5. The join of listing 10.17, then aggregateFields (figure 10.3)
   3 rows:
     {"title": "The Power of Habit", "isbn": "978-0812981605", "author_name": "Charles Duhigg"}
     {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274", "author_name": "Sean Covey"}
     {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274", "author_name": "Stephen Covey"}
   2 books:
     {"title": "The Power of Habit", "isbn": "978-0812981605", "authorNames": ["Charles Duhigg"]}
     {"title": "7 Habits of Highly Effective People", "isbn": "978-1982137274", "authorNames": ["Sean Covey", "Stephen Covey"]}
```

## به چه چیزی نگاه کنید

- جایگزینی درون مقداری گیومه‌دار تنها متن است: پایگاه SQLite آن bindingی افزوده را نمی‌پذیرد. در PostgreSQL، عبارت `'%$1%'` خاموش نویسه‌های `$1` را می‌جست.
- برداشتن تنها `title` و `isbn`، آن‌طور که listing ۱۰.۶ می‌کند، در `dbSearchResultSchema` شکست می‌خورد، که `publication_year` را اجبار می‌کند؛ کادر vault در درس را ببینید.
- عملگر `LIKE` در SQLite بزرگی و کوچکی ASCII را نشنیده می‌گیرد، پس `habit` هر دو عنوان را می‌یابد. با `LIKE`ی حساس، مانند PostgreSQL، هیچ نمی‌یابد، و آن‌جا به `ILIKE` نیاز داشتید. این مشاهده‌ی vault است: کتاب از بزرگی و کوچکی حرف نمی‌گوید.
- همان یک `renameResultKeys` ردیف‌های کتاب و کاربر را از نو شکل می‌دهد.
- تابع `aggregateFields` سه ردیف آن join را به دو کتاب بدل می‌کند، با نام کاوی‌ها گردشده در یک فهرست `authorNames`.

## مرتبط

- یادداشت فصل: [فصل ۱۰: عملیات پایگاه داده](../../chapters/10-database-operations.md) — بخش‌های ۱۰.۱ تا ۱۰.۴، صص. ۱۹۸–۲۱۸
