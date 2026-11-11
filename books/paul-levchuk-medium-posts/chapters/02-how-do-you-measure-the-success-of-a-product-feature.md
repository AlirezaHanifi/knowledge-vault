---
book: paul-levchuk-medium-posts
chapter: 2
title: "How do you measure the success of a product feature?"
translated_title: "موفقیت یک feature محصول را چطور بسنجیم؟"
lang: fa
source_url: https://medium.com/@paul.levchuk/how-do-you-measure-the-success-of-a-product-feature-28240cf20aa3
---

# نوشته‌ی ۲: موفقیت یک feature محصول را چطور بسنجیم؟

[نوشته‌ی ۱: تحول churn در Netflix →](01-churn-rate-evolution-at-netflix.md) · [مجموعه](../README.md) · [نوشته‌ی ۳: این feature بین کاربران فعال هفتگی و روزانه چقدر محبوب است؟ ←](03-how-popular-is-this-feature-among-weekly-daily-active.md)

> **مقاله‌ی اصلی:** [How do you measure the success of a product feature?](https://medium.com/@paul.levchuk/how-do-you-measure-the-success-of-a-product-feature-28240cf20aa3) · Medium، ۲۰۲۲-۰۷-۰۳

## خلاصه

برای سنجش موفقیت یک feature محصول باید متریک‌های محصول را از متریک‌های مدل کسب‌وکار جدا کنیم. چارچوب AARRR از Dave McClure و چارچوب HEART از Google برای سطح feature بیش‌ازحد کلی‌اند. راهنمای Amplitude در ۲۰۱۶ هفت گام پیشنهاد می‌کند و در پایان یادآوری می‌کند هنوز علیت ندارید. نویسنده چارچوب خودش را معرفی می‌کند: هفت پرسش درباره‌ی محبوبیت، عادت، شدت استفاده، اثر روی retention، تفاوت کاربر رایگان و پولی، زمینه‌ی استفاده و نرخ تکمیل، که هر کدام یک نوشته‌ی جدا دارد. این نوشته نقشه‌ی راه بخش اول مجموعه است.

## نکته‌های کلیدی

- **متریک محصول با متریک مدل کسب‌وکار فرق دارد.**
- **چارچوب AARRR** یعنی Acquisition و Activation و Retention و Referral و Revenue؛ برای ارزیابی مدل کسب‌وکار خوب است و برای سطح feature خیلی کلی.
- **چارچوب HEART** از Google یعنی Happiness و Engagement و Adoption و Retention و Task Success؛ برای UX بهتر است ولی باز هم نمی‌گوید دقیقاً چه چیزی را چطور بسنجیم.
- **راهنمای Amplitude** هفت گام دارد، از سنجش استفاده‌ی پایه تا اثر روی engagement، و تأکید می‌کند هنوز علیت ندارید.
- **چارچوب نویسنده هفت پرسش دارد:** محبوبیت، عادت، شدت استفاده، ارزش از نظر retention، درآمدزایی، زمینه و سادگی.

## فهرست بخش‌ها

*این نوشته عنوان بخش ندارد.*

- چارچوب‌های موجود
- گام‌های Amplitude
- چارچوب نویسنده

## یادداشت‌ها

نخستین نکته این است که برای جواب دادن به «موفقیت یک feature را چطور بسنجیم» باید متریک‌های محصول را از متریک‌های مدل کسب‌وکار جدا کرد.

شاید با چارچوب AARRR از Dave McClure آشنا باشید. AARRR مخفف Acquisition و Activation و Retention و Referral و Revenue است. این چارچوب وقتی خوب است که بخواهید مدل کسب‌وکارتان را ارزیابی کنید و شاید نقطه‌های رشد پیدا کنید، ولی برای سطح یک feature بیش‌ازحد کلی است. برای چارچوب مخصوص بهبود UX می‌توانید سراغ HEART از Google بروید، یعنی Happiness و Engagement و Adoption و Retention و Task Success. HEART برای شروع سنجش featureها خیلی بهتر است ولی هنوز کلی است و نمی‌گوید دقیقاً چه چیزی را چطور بسنجید.

اگر عبارت «چطور موفقیت یک feature محصول را بسنجیم» را جست‌وجو کنید میلیون‌ها صفحه می‌آید، ولی به نظر نویسنده مفیدترین‌شان مقاله‌ی تحلیلی Amplitude در ۲۰۱۶ است. توصیه‌ی Amplitude این گام‌هاست:

1. استفاده‌ی پایه از feature جدید را بسنجید.
2. در ویژگی‌های رویداد کند و کاو کنید تا الگو پیدا کنید.
3. بفهمید کاربران درست قبل از استفاده از feature چه می‌کنند.
4. یک cohort رفتاری از کسانی بسازید که از feature استفاده کرده‌اند.
5. اثر feature جدید روی retention را تحلیل کنید.
6. اثر feature را روی قیف‌های تبدیل کلیدی بسنجید.
7. اثر feature را روی engagement بسنجید.

مهم‌تر این‌که Amplitude در پایان راهنمایش به همه یادآوری می‌کند: هنوز علیت ندارید. با این حال نویسنده فکر می‌کند برای جواب دادن به این پرسش مهم هنوز جا برای بهتر شدن هست، و چارچوب خودش را معرفی می‌کند. هر مورد فهرست زیر یک نوشته‌ی جدا دارد که درباره‌ی محاسبه و تفسیر متریک‌ها بینش می‌دهد.

| پرسش | نام | فصل |
|---|---|---|
| feature بین کاربران فعال هفتگی و روزانه چه‌قدر محبوب است؟ | محبوبیت | [۳](03-how-popular-is-this-feature-among-weekly-daily-active.md) |
| کاربران هر هفته چه‌قدر منظم از آن استفاده می‌کنند؟ | عادت | [۴](04-how-regular-are-users-using-this-feature-per-week.md) |
| کاربران در هر روز چند بار از آن استفاده می‌کنند؟ | شدت استفاده | [۵](05-how-often-are-users-using-this-feature-per-day.md) و [۶](06-clustering-users-based-on-weekly-habit-and-daily.md) |
| اثر روی retention چیست؟ | ارزش | [۷](07-what-is-the-impact-on-the-retention-rate.md) تا [۱۱](11-product-feature-retention-deep-dive-mcc-coefficient.md) |
| استفاده بین کاربران رایگان و پولی چه فرقی دارد؟ | درآمدزایی | [۱۲](12-what-is-the-difference-in-product-feature-usage-between.md) |
| کاربران قبل و بعد از استفاده چه می‌کنند؟ | زمینه | [۱۳](13-user-flow.md) |
| نرخ تکمیل استفاده چه‌قدر است؟ | سادگی | [۱۴](14-what-is-the-completion-rate-of-a-product-feature.md) |

نوشته با وعده‌ی نوشته‌ی بعدی تمام می‌شود: اولین پرسش، یعنی محبوبیت feature بین کاربران.

> **In practice:** هفت پرسش نویسنده را می‌شود هفت جدول Gold کرد که همه از یک جدول Silver رویداد feature خوانده می‌شوند، نه هفت query جدا در هفت داشبورد.
>
> **Your turn:** تیم محصول برای هر feature تازه یک داشبورد دستی در Metabase می‌خواهد. چطور این کار را تکراری نکنید؟
>
> *Answer:* یک جدول Gold با ستون feature و یک ستون برای هر پرسش، مثل محبوبیت و عادت و اثر روی retention؛ داشبورد یک filter روی feature می‌گیرد و feature تازه فقط یک مقدار تازه است (بخش «چارچوب نویسنده»).

## پیوندها

- **ادامه در:** [فصل ۳](03-how-popular-is-this-feature-among-weekly-daily-active.md) که اولین پرسش را جواب می‌دهد، و [فصل ۱۵](15-how-a-successful-product-feature-should-look-like.md) که همه‌ی هفت پرسش را کنار هم می‌گذارد تا شکل یک feature موفق را ببیند.
- **چارچوب بزرگ‌تر:** [فصل ۳۵](35-why-does-product-analytics-go-beyond-product-feature.md) می‌گوید چرا تحلیل محصول از تحلیل featureها فراتر می‌رود.

## خودتان را بسنجید

*پرسش‌ها و پاسخ‌ها مال vault است.*

1. **چرا AARRR برای سنجش یک feature مناسب نیست؟**
   - [x] چون برای ارزیابی مدل کسب‌وکار است و برای سطح feature خیلی کلی.
   - [ ] چون فقط درآمد را می‌سنجد.
   - [ ] چون برای UX ساخته شده.

   *Answer:* (بخش «چارچوب‌های موجود»).

2. **ابزار Amplitude در پایان راهنمایش چه یادآوری می‌کند؟**

   *Answer:* این‌که با این گام‌ها هنوز علیت ندارید (بخش «گام‌های Amplitude»).
