# مدل‌های relational، document و گراف با SQL واقعی

پنج برنامه‌ی کوچک SQLite که ادعاهای فصل را با عدد نشان می‌دهند: حلقه‌ای به سبک ORM در برابر یک join، یک join چندبه‌چند که جمع کل را بزرگ می‌کند، کوئری گراف آمریکا به اروپای کتاب به شکل یک CTE بازگشتی، یک چرخه که `UNION ALL` را بی‌پایان می‌کند، و خواندن هم‌زمان رکوردهای قالب قدیم و جدید. هر کوئری را می‌توانید در کنسول warehouse خودتان روی جدول‌های واقعی امتحان کنید.

*این آزمایش بخش‌های «مدل relational در برابر مدل document» و «مدل‌های داده‌ی گراف‌مانند» از ویراست دوم DDIA را نشان می‌دهد (صص. ۶۷–۹۲). پیاده‌سازی و داده‌ی نمونه مال خود vault است؛ گراف همان شکل ۳-۶ و کوئری همان مثال ۳-۶ کتاب است که برای `json_extract` در SQLite تطبیق داده شده.*

## اجرا

با Python 3.10 یا جدیدتر، فقط کتابخانه‌ی استاندارد (`sqlite3` در حافظه) و قطعی:

```sh
python3 models.py
```

خروجی برنامه انگلیسی است، چون بیشتر ترمینال‌ها متن راست‌به‌چپ را درست نشان نمی‌دهند.

## خروجی مورد انتظار

```text
Chapter 3 in SQLite 3.x

1. N+1 queries versus one join (p. 69)
--------------------------------------
  ORM-style loop:  51 queries for 50 comments with their authors
  one join:         1 query  for 50 comments with their authors
  same result:    True

2. Many-to-many join fan-out (pp. 75-77)
----------------------------------------
  6 transactions become 12 rows after joining account_holders
  per account (no join)        total =    1250   ok
  per customer, all holders    total =    3030   WRONG
  per customer, primary only   total =    1250   ok
  per customer, split evenly   total =    1250   ok

3. Variable-length traversal with WITH RECURSIVE (pp. 90-92)
------------------------------------------------------------
  within United States:   2 locations, deepest 1 edge down (Idaho)
  within Europe:          8 locations, deepest 4 edges down (Saint-Lo)
  Example 3-6 (30 lines of SQL here, comments removed): ['Lucy']
  The Cypher version (Example 3-5) is 4 lines.

4. A cycle in the graph: UNION versus UNION ALL (p. 92)
-------------------------------------------------------
  UNION, no limit:        stops by itself; 8 rows = accounts ABCDEFGH
  UNION ALL, hop limit -> rows (one per path): 1:3  2:5  3:7  4:11  5:17  6:23  7:27  8:35
  UNION ALL, no hop limit: still going at 10,000 rows; only the safety LIMIT stopped it

5. Schema-on-read: old and new records side by side (p. 81)
-----------------------------------------------------------
  user 1: first_name = Ada    (old format, split at read time)
  user 2: first_name = Alan   (old format, split at read time)
  user 3: first_name = Grace  (new format, read as is)
```

## به چه چیزی نگاه کنید

- **مسئله‌ی N+1:** برای همان ۵۰ ردیف، ۵۱ کوئری در برابر ۱ کوئری (ص. ۶۹). در warehouse که هر کوئری هزینه‌ی ثابت شروع دارد، این فاصله بیشتر هم می‌شود.
- **پدیده‌ی fan-out:** شش تراکنش بعد از join به ۱۲ ردیف تبدیل می‌شوند و جمع کل از ۱٬۲۵۰ به ۳٬۰۳۰ می‌رسد. هر قاعده‌ای که هر تراکنش را فقط یک بار حساب کند (grain حساب، صاحب اصلی حساب، یا تقسیم مساوی) دوباره همان جمع درست را می‌دهد.
- **بازگشت:** آیداهو ۱ یال `within` پایین‌تر از ایالات متحده است و سن‌لو ۴ یال پایین‌تر از اروپا، پس هیچ تعداد ثابتی join جواب نمی‌دهد؛ CTE بازگشتی Lucy را پیدا می‌کند (صص. ۹۰–۹۲). ۳۰ خط آن را با ۴ خط Cypher مقایسه کنید.
- **چرخه‌ها:** با `UNION` ردیف‌های تکراری حذف می‌شوند و کوئری بعد از ۸ حساب تمام می‌شود. با `UNION ALL` به ازای هر مسیر یک ردیف می‌آید و چرخه‌ی A → B → D → E → A مدام ردیف اضافه می‌کند تا چیزی جلویش را بگیرد (کتاب در ص. ۹۲ چرخه‌ها را جزو جزئیات اضافه می‌شمارد).
- **الگوی schema-on-read:** رکوردهای قدیمی با `name` و رکوردهای جدید با `first_name` کنار هم زندگی می‌کنند و کوئری خواندن همان شرط `if (user.name && !user.first_name)` کتاب را اجرا می‌کند (ص. ۸۱).

## پیوندها

- یادداشت فصل: [فصل ۳: مدل‌های داده و زبان‌های کوئری](../../chapters/03-data-models-and-query-languages.md)، صص. ۶۷–۹۲
- همین را در مرورگر امتحان کنید: [یال‌ها را دنبال کنید](../../widgets/03-graph-traversal.html)، [چرا جمع کل بزرگ‌تر می‌شود؟](../../widgets/03-join-fanout.html)
