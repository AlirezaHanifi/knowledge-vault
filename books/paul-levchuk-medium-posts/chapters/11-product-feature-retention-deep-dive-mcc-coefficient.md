---
book: paul-levchuk-medium-posts
chapter: 11
title: "Product feature retention deep dive — MCC coefficient"
translated_title: "غواصی در retention فیچر: ضریب MCC"
lang: fa
source_url: https://medium.com/@paul.levchuk/product-feature-retention-deep-dive-mcc-coefficient-3e04150e56f7
---

# نوشته‌ی ۱۱: غواصی در retention فیچر: ضریب MCC

[نوشته‌ی ۱۰: تحلیل retention فیچر با Information gain →](10-retention-deep-dive.md) · [مجموعه](../README.md) · [نوشته‌ی ۱۲: استفاده از feature بین کاربران رایگان و پولی چه فرقی دارد؟ ←](12-what-is-the-difference-in-product-feature-usage-between.md)

> **مقاله‌ی اصلی:** [Product feature retention deep dive — MCC coefficient](https://medium.com/@paul.levchuk/product-feature-retention-deep-dive-mcc-coefficient-3e04150e56f7) · Medium، ۲۰۲۲-۱۱-۲۳

## خلاصه

ضعف اصلی Information Gain این است که جهت اثر را، مثبت یا منفی، تشخیص نمی‌دهد، چون همیشه عددی مثبت است. feature18 سومین Information Gain بالا را دارد ولی کاربرانی که از آن استفاده کرده‌اند retention برابر ۷٫۹٪ دارند و کسانی که استفاده نکرده‌اند ۲۰٫۷٪. یعنی استفاده از آن اثر منفی قوی دارد. برای یادگیری ماشین این مهم نیست ولی در تحلیل محصول باید جهت را بدانیم. نویسنده ضریب MCC را پیشنهاد می‌کند، ضریب همبستگی بین دو متغیر دودویی. یافته‌ی مهم: تقریباً همه‌ی featureهای محبوب اثر منفی روی retention دارند.

## نکته‌های کلیدی

- **ارزیابی قابل‌اعتماد سه چیز می‌خواهد:** محبوبیت feature، عملکرد retention آن، و تعدیل با عملکرد استفاده نکردن.
- **شاخص Information Gain جهت را نمی‌گوید.** همیشه مثبت است؛ feature18 سومین مقدار بالا را دارد ‏(۰٫۰۱۴۰) ولی retention استفاده‌کننده‌ها ۷٫۹٪ و استفاده‌نکننده‌ها ۲۰٫۷٪ است.
- **ضریب MCC** همبستگی دو متغیر دودویی است، یعنی استفاده از feature و بازگشت، و علامتش جهت اثر را می‌گوید.
- **تقریباً همه‌ی featureهای محبوب اثر منفی دارند.** معمولاً محبوب‌ترین‌ها set-up‌اند و در بالای قیف دیده می‌شوند، جایی که قصد کاربر کم است و retention هم کم است.
- **نکته‌ی جانبی:** ضریب MCC منفی است وقتی درصد برگشته‌های محصول از میانگین وزنی کمتر باشد.
- **مقایسه‌ی MCC و Information Gain در یک نمودار** بهترین کاری است که می‌شود کرد.

## فهرست بخش‌ها

*این نوشته عنوان بخش ندارد.*

- ضعف Information Gain
- ضریب MCC
- مقایسه‌ی MCC با Information Gain
- نقش featureهای محبوب و اثر منفی

## یادداشت‌ها

برای ارزیابی قابل‌اعتماد اثر featureهای محصول روی retention باید سه چیز را در نظر گرفت: محبوبیت feature، عملکرد retention آن، و تعدیل با عملکرد استفاده نکردن. یکی از راه‌حل‌های ممکن Information Gain است. ضعف اصلی آن این است که جهت اثر را، مثبت یا منفی، تشخیص نمی‌دهد؛ چون Information Gain همیشه عددی مثبت است.

مثال feature18: سومین Information Gain بالا را دارد، ۰٫۰۱۴۰. ولی اگر دقیق نگاه کنیم، کاربرانی که از feature18 استفاده کرده‌اند retention برابر ۷٫۹٪ دارند و کاربرانی که استفاده نکرده‌اند ۲۰٫۷٪. داده می‌گوید استفاده از این feature اثر منفی قوی روی retention دارد. از دید یادگیری ماشین این کاملاً درست است، ولی از دید تحلیل محصول نه؛ باید جهت را بدانیم.

برای رفع این مشکل نویسنده ضریب MCC را توصیه می‌کند. محاسبه‌ی MCC یک ضریب همبستگی برای دو متغیر دودویی است. چند روش محاسبه هست و نویسنده روشی را ترجیح می‌دهد که از جدول چهارخانه‌ی استفاده و بازگشت می‌آید. ضریب MCC را برای فهرست featureها حساب و مصور می‌کند. شاید بهترین کار مقایسه‌ی ضریب MCC با Information Gain در یک نمودار باشد.

بینش مهم این‌جاست: **تقریباً همه‌ی featureهای محبوب اثر منفی روی retention دارند.** معمولاً محبوب‌ترین featureها از نوع set-up هستند. این featureها در بالای قیف ظاهر می‌شوند، جایی که قصد کاربر کم است، و به همین دلیل retention کاربران هم پایین است.

یک نکته‌ی جانبی: اگر دقیق نگاه کنیم می‌بینیم ضریب MCC وقتی منفی است که متریک درصد کاربران برگشته‌ی محصول پایین‌تر از میانگین وزنی باشد.

> **Try it:** [جهت اثر: Information Gain یا MCC](../widgets/11-information-gain-vs-mcc.html): retention کاربران و غیرکاربران feature را عوض کنید و ببینید فقط MCC علامتش برمی‌گردد.

> **In practice:** ضریب MCC را می‌شود مستقیم در SQL ClickHouse از چهار خانه‌ی ماتریس درهم‌ریختگی ساخت و در Gold کنار هر feature نگه داشت.
>
> **Your turn:** گزارش Information Gain یک feature را بالای فهرست گذاشته و تیم می‌خواهد آن را تبلیغ کند. چه چیزی را چک می‌کنید؟
>
> *Answer:* علامت اثر را با MCC؛ Information Gain همیشه مثبت است و feature‌ای که retention را پایین می‌آورد هم ممکن است بالای فهرست باشد (بخش «ضعف Information Gain»).

## پیوندها

- **بر پایه‌ی:** [فصل ۱۰](10-retention-deep-dive.md) که Information Gain را می‌سازد.
- **ادامه در:** [فصل ۲۰](20-the-mcc-coefficient-or-cohort-analysis.md) که MCC را با تحلیل cohort مقایسه می‌کند و [فصل ۲۱](21-mastering-the-mcc-coefficient.md) که MCC را عمیق‌تر می‌شکافد، و [فصل ۱۵](15-how-a-successful-product-feature-should-look-like.md) که از آن شکل feature موفق را می‌سازد.

## خودتان را بسنجید

*پرسش‌ها و پاسخ‌ها مال vault است.*

1. **چرا برای تحلیل محصول Information Gain کافی نیست؟**
   - [x] چون جهت اثر را نمی‌گوید و همیشه مثبت است.
   - [ ] چون محاسبه‌اش سخت است.
   - [ ] چون محبوبیت را نادیده می‌گیرد.

   *Answer:* feature18 با Information Gain بالا در واقع اثر منفی داشت (بخش «ضعف Information Gain»).

2. **چرا featureهای محبوب اغلب MCC منفی دارند؟**

   *Answer:* چون معمولاً set-up‌اند و در بالای قیف می‌آیند که قصد کاربر کم و retention پایین است (بخش «نقش featureهای محبوب و اثر منفی»).
