# عمل join کردن سرچشمه‌ها با کلید

صافی دوباره‌ی فیلد با `pick` و `keyBy` و تابع عمومی `joinArrays`، اجراشده در برابر Open Libraryی ساختگی، پس هیچ شبکه‌ای لازم نیست. اسکریپت رکوردی را با فیلدهای به‌کار‌آمده‌ی چاپی و تصحیح‌شده صافی می‌کند، داده‌ی تست listing ۱۱.۱۹ را با گزارش ناسازی‌ها join می‌کند، آن join غنی کردن را روی نسخه‌ی ساختگی اجرا، و نشان می‌دهد که آن join یک outer join است.

*تصویری از فصل ۱۱ کتاب Data-Oriented Programming، صص. ۲۲۹–۲۳۹ (listingهای ۱۱.۹ و ۱۱.۱۶ تا ۱۱.۱۹). رکورد 7 Habits در نسخه‌ی ساختگی از فیلدهای listing ۱۱.۶ کار می‌کشد، و رکورد The Power of Habit از فیلدهای listing ۱۱.۱۹. مقدار `isbn_13`ش و ISBNهای افزوده در قدم ۵ مال vault است.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 join_arrays.py
```

## خروجی چشم‌داشته

```text
1. Double field filtering of 7 Habits, requested: ['title', 'publishers', 'number_of_pages', 'revision']
   relevantFields as printed: {"title": "7 Habits of Highly Effective People : Revised and Updated", "number_of_pages": 432, "isbn": "978-1982137274"}
   with "publishers":        {"title": "7 Habits of Highly Effective People : Revised and Updated", "publishers": ["Simon & Schuster, Incorporated"], "number_of_pages": 432, "isbn": "978-1982137274"}
   ('revision' is requested but not relevant, so the server never exposes it)

2. keyBy keeps the last element per key
   {"a": {"isbn": "a", "n": 3}, "b": {"isbn": "b", "n": 2}}

3. The test data of listing 11.19 (each Open Library record carries the other book's title)
   {"available": true, "isbn": "978-1982137274", "subjects": ["Social aspects", "Habit", "Change (Psychology)"], "subtitle": "Why We Do What We Do in Life and Business", "title": "The Power of Habit"}
   {"available": false, "isbn": "978-0812981605", "number_of_pages": 432, "subtitle": "Powerful Lessons in Personal Change", "title": "7 Habits of Highly Effective People"}
   conflicts (Open Library wins silently):
     978-0812981605 title: database 'The Power of Habit' vs Open Library '7 Habits of Highly Effective People'
     978-1982137274 title: database '7 Habits of Highly Effective People' vs Open Library 'The Power of Habit'

4. The enrichment flow with the mock: database rows joined with filtered Open Library records
   {"available": true, "isbn": "978-1982137274", "number_of_pages": 432, "subtitle": "Powerful Lessons in Personal Change", "title": "7 Habits of Highly Effective People : Revised and Updated"}
   {"available": false, "isbn": "978-0812981605", "subtitle": "Why We Do What We Do in Life and Business", "title": "The Power of Habit"}
   conflicts: none (the database contributes only isbn and available)

5. An outer join: a database book with no Open Library record, and vice versa
   {"available": true, "isbn": "978-1982137274", "number_of_pages": 432, "subtitle": "Powerful Lessons in Personal Change", "title": "7 Habits of Highly Effective People : Revised and Updated"}
   {"available": false, "isbn": "978-0812981605", "subtitle": "Why We Do What We Do in Life and Business", "title": "The Power of Habit"}
   {"available": true, "isbn": "978-0000000001"}
   {"isbn": "978-0000000002", "title": "Only in Open Library"}
```

## به چه چیزی نگاه کنید

- مقدار `relevantFields` فیلد `publisher` را فهرست می‌کند، ولی آن API مقدار `publishers` را برمی‌گرداند، پس همان‌طور که چاپ شده ناشران هیچ‌وقت به client نمی‌رسند.
- فیلدی که خواسته شده ولی به‌کار‌آمده نیست، یعنی `revision`، انداخته می‌شود: صافی نخست فهرست سپید سرور است.
- در listing ۱۱.۱۹ هر رکورد Open Library عنوان آن یکی کتاب را می‌برد، و آن درهم‌آمیزی می‌گذارد Open Library خاموش ببرد. همان ناسازی است که درهم‌آمیختن قرار بود از آن بپرهیزد؛ کادر vault در درس را ببینید.
- وقتی پایگاه داده تنها `isbn` و `available` را می‌دهد، مانند جریان غنی کردن، چیزی برای ناساز شدن نیست.
- کتاب‌هایی که تنها در یک سو هستند باز پیدا می‌شوند: کلید زدن هر دو آرایه و درهم آمیختن mapها یک outer join است.

## مرتبط

- یادداشت فصل: [فصل ۱۱: سرویس‌های وب](../../chapters/11-web-services.md) — بخش‌های ۱۱.۴ تا ۱۱.۶، صص. ۲۲۹–۲۳۹
