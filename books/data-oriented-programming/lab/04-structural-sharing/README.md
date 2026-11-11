# شریک شدن ساختاری در عدد

هر به‌روزرسانی immutability واقعاً چقدر کپی می‌کند؟ درگاهی Python از `setImmutable` سال نشر یک کتاب را در کتابخانه‌هایی از ۱۰ تا ۱۰٬۰۰۰ کتاب می‌گذارد. اسکریپت mapهایی را که می‌سازد، خانه‌هایی را که کپی می‌کند، و mapهایی را که با version پیشین شریک می‌شود در برابر کپی عمیق می‌شمارد. بعد ۱٬۰۰۰ version از کتابخانه‌ای ۱٬۰۰۰کتابی را نگه می‌دارد و mapهایی را که با هم دارند می‌شمارد.

*تصویری از فصل ۴ کتاب Data-Oriented Programming، بخش‌های ۴.۲ و ۴.۳، صص. ۷۵–۸۱: شریک شدن ساختاری، و تابع `setImmutable` دیو (listing ۴.۴، ص. ۸۱). شکل آن کتابخانه از شکل ۴.۲ پی می‌گیرد؛ و اندازه‌اش و نویسنده‌ها و به‌روزرسانی‌های تصادفی مال vault است، با seed.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 structural_sharing.py
```

## خروجی چشم‌داشته

```text
One update: set a book's publication year
  books  maps in library  new maps  slots copied  shared maps  deep copy
     10              343         4            21          339        343
    100              658         4           111          654        658
   1000            3,808         4         1,011        3,804      3,808
  10000           35,308         4        10,011       35,304     35,308

The previous version is untouched:
  previous title: Book 1
  next title:     Watchmen
  userManagement shared by reference: True
  sibling book shared by reference:   True

Keeping 1,000 versions of a 1,000-book library (one random update each)
  maps in one version:               3,808
  maps kept by 1,001 shared versions: 7,808  (2.05x one version)
  maps kept by 1,001 deep copies:     3,811,808  (1001x)
```

## به چه چیزی نگاه کنید

- پس از یک به‌روزرسانی دقیقاً ۴ map تازه‌اند، یکی برای هر سطح آن مسیر، یعنی کتابخانه و catalog و `booksByIsbn` و خود کتاب، هر اندازه‌ای هم آن کتابخانه داشته باشد. باقی شریک است، مقدار `userManagement` و کتاب‌های هم‌نیا هم.
- *خانه‌های کپی‌شده* با آن مجموعه رشد می‌کند: کلون سطحی `booksByIsbn` هر کلیدی را کپی می‌کند. همان کندی‌ای است که فصل ۹ با ساختارهای داده‌ی persistent به درست کردنش می‌رود.
- کپی عمیق به‌اندازه‌ی mapهایی که آن کتابخانه دارد map می‌سازد. آن برای ۱۰٬۰۰۰ کتاب ۳۵٬۳۰۸ است، در برابر ۴.
- هزار version شریک تنها حدود دو برابر mapهای یک version را نگه می‌دارند. هزار کپی عمیق هزار برابر را نگه می‌داشتند.

## مرتبط

- یادداشت فصل: [فصل ۴: مدیریت state](../../chapters/04-state-management.md) — بخش‌های ۴.۲ و ۴.۳، صص. ۷۵–۸۱
