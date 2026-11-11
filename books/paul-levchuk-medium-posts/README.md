---
title: "Paul Levchuk on Medium"
short_title: "Levchuk"
kind: articles
edition: "Blog series"
authors: ["Paul Levchuk"]
publisher: "Medium (self-published)"
year: 2026
published: "2020-05-17"
toc_source: "Medium GraphQL listing of the author's profile (medium.com/@paul.levchuk), all 71 posts"
toc_verified: "2026-11-09"
source_file: "raw/ (kept locally, gitignored; the listing, each post's text extracted through a reader mirror, and images). Posts have no page numbers, so references are to the post's own section headings"
lang: fa
---

# Paul Levchuk on Medium

**نسخه‌ی تعاملی را با باز کردن [`index.html`](index.html) در مرورگر ببینید**: برای هر نوشته یک درس، با شبیه‌سازی و خودسنجی. همین متن روی GitHub هم خوب خوانده می‌شود.

## درباره‌ی این مجموعه

نویسنده‌ی Paul Levchuk در Medium درباره‌ی تحلیل محصول و رشد می‌نویسد. این مجموعه **همه‌ی ۷۱ نوشته‌ی** او را از ۲۰۲۰ تا ۲۰۲۶-۰۹-۲۷ در بر می‌گیرد: از تحول churn در Netflix و سنجش featureهای محصول، تا cohort و stickiness، LTV و CAC payback، ماتریس RF و وضعیت مشتری، و آخرین نوشته‌ها درباره‌ی انتساب و جذب کاربر در بازی‌های موبایل. فهرست کامل نوشته‌ها از راه GraphQL خود Medium گرفته شده است، چون feed RSS و صفحه‌ی پروفایل فقط حدود ده نوشته‌ی آخر را نشان می‌دهند.

هر نوشته این‌جا یک «فصل» است. نوشته‌ها به ترتیب تاریخ انتشار آمده‌اند، چون بسیاری صریحاً دنباله‌ی هم‌اند.

## محتوای این پوشه

| مسیر | چیست |
|---|---|
| `chapters/NN-*.md` | برای هر نوشته یک یادداشت، که منبع اصلی است؛ کنار هر کدام یک درس `.html` ساخته می‌شود |
| `framework.md` | چارچوب تحلیلی: سنتز vault که همه‌ی نوشته‌ها را در زنجیره‌ی ارزش، هشت اصل، جعبه‌ابزار و راهنمای تصمیم به هم وصل می‌کند |
| `widgets/` | شبیه‌سازی‌های دست‌ساز که در درس‌ها جاسازی شده‌اند |
| `raw/` | خود نوشته‌ها همان‌طور که منتشر شده‌اند، که **فقط روی دیسک محلی‌اند و در gitignore** تا متن و نمودار نویسنده بازنشر نشوند؛ یادداشت‌ها آن‌ها را به زبان vault بازگو می‌کنند |
| `index.html` | صفحه‌ی این مجموعه که از همین README و نوشته‌ها ساخته می‌شود |

## این مجموعه چطور به هم وصل است

شش رشته به ترتیب زمان: **سنجش feature و retention** (۱ تا ۱۵)، **monetization و رشد محصول‌محور** (۱۶ تا ۲۳)، **stickiness، engagement و cohort** (۲۴ تا ۴۰)، **LTV و CAC payback** (۴۱ تا ۴۸)، **RF و وضعیت مشتری** (۴۹ تا ۵۶) و **اقتصاد جذب کاربر و انتساب** (۵۷ تا ۷۱).

```mermaid
flowchart LR
    A["سنجش feature و retention"] --> B["monetization و PLG"] --> C["stickiness و cohort"] --> D["LTV و CAC payback"] --> E["RF و وضعیت مشتری"] --> F["اقتصاد جذب کاربر و انتساب"]
    C -.-> E
    D -.-> F
```

*ترتیب پیکان‌ها ترتیب انتشار است؛ خط‌چین‌ها خوانش vault از ایده‌های مشترک.*

برای نقشه‌ی کامل، از زنجیره‌ی ارزش و هشت اصل تا راهنمای «از پرسش به مسیر» و جایگاه هر نوشته، [چارچوب تحلیلی](framework.md) را بخوانید؛ آن صفحه سنتز خود vault است و از کل به جزء پیش می‌رود: سه جمله‌ی خلاصه، زنجیره، هشت اصل با یک شکل و یک شبیه‌سازی برای هر کدام، و در پایان جایگاه تک‌تک نوشته‌ها. [کاوشگر چارچوب](widgets/00-framework-explorer.html) همین زوم را تعاملی می‌کند.

رشته‌هایی که تکرار می‌شوند:

- **از نتیجه به فرایند.** قیف دو عدد می‌دهد؛ وضعیت‌ها و گذارها مسیر را نشان می‌دهند (۴۹ تا ۵۶).
- **ترکیب جمعیت در برابر رفتار.** متریک یا به این دلیل تکان می‌خورد که جمعیت عوض شده یا آدم‌ها جور دیگری رفتار کرده‌اند (۳۷، ۶۷، ۷۱).
- **چیزی را بشمارید که قابل‌اجرا است.** سیگنال دقیق بی‌حجم از هیچ‌کاری‌نکردن می‌بازد (۶۳) و LTV بدون churn واقعی گمراه می‌کند (۵۷).
- **نیت و ظرفیت دو چیزند.** رفتار نیت را می‌سنجد، نه ظرفیت پرداخت (۵۸، ۵۹).

## نوشته‌ها

| # | نوشته | انتشار |
|---:|---|---|
| ۱ | [تحول churn در Netflix](chapters/01-churn-rate-evolution-at-netflix.md) | ۲۰۲۰-۰۵-۱۷ |
| ۲ | [موفقیت یک feature محصول را چطور بسنجیم؟](chapters/02-how-do-you-measure-the-success-of-a-product-feature.md) | ۲۰۲۲-۰۷-۰۳ |
| ۳ | [این feature بین کاربران فعال هفتگی و روزانه چقدر محبوب است؟](chapters/03-how-popular-is-this-feature-among-weekly-daily-active.md) | ۲۰۲۲-۰۷-۱۹ |
| ۴ | [کاربران هر هفته چقدر منظم از این feature استفاده می‌کنند؟](chapters/04-how-regular-are-users-using-this-feature-per-week.md) | ۲۰۲۲-۰۸-۰۲ |
| ۵ | [کاربران در هر روز چند بار از این feature استفاده می‌کنند؟](chapters/05-how-often-are-users-using-this-feature-per-day.md) | ۲۰۲۲-۰۸-۲۱ |
| ۶ | [خوشه‌بندی کاربران بر پایه‌ی الگوی عادت هفتگی و شدت استفاده‌ی روزانه](chapters/06-clustering-users-based-on-weekly-habit-and-daily.md) | ۲۰۲۲-۰۹-۰۴ |
| ۷ | [featureهای محصول چه اثری روی retention دارند؟](chapters/07-what-is-the-impact-on-the-retention-rate.md) | ۲۰۲۲-۰۹-۲۶ |
| ۸ | [نسخه‌ی بهبودیافته‌ی تحلیل اثر featureها روی retention](chapters/08-an-enhanced-version-of-the-analysis-of-how-product.md) | ۲۰۲۲-۱۰-۰۳ |
| ۹ | [دو نوع retention برای feature](chapters/09-two-types-of-feature-retention.md) | ۲۰۲۲-۱۰-۱۷ |
| ۱۰ | [تحلیل retention فیچر با Information gain](chapters/10-retention-deep-dive.md) | ۲۰۲۲-۱۱-۰۸ |
| ۱۱ | [غواصی در retention فیچر: ضریب MCC](chapters/11-product-feature-retention-deep-dive-mcc-coefficient.md) | ۲۰۲۲-۱۱-۲۳ |
| ۱۲ | [استفاده از feature بین کاربران رایگان و پولی چه فرقی دارد؟](chapters/12-what-is-the-difference-in-product-feature-usage-between.md) | ۲۰۲۲-۱۲-۰۵ |
| ۱۳ | [جریان کاربر](chapters/13-user-flow.md) | ۲۰۲۳-۰۱-۰۴ |
| ۱۴ | [نرخ تکمیل یک feature محصول چقدر است؟](chapters/14-what-is-the-completion-rate-of-a-product-feature.md) | ۲۰۲۳-۰۱-۲۴ |
| ۱۵ | [یک feature موفق چه شکلی دارد؟](chapters/15-how-a-successful-product-feature-should-look-like.md) | ۲۰۲۳-۰۲-۱۰ |
| ۱۶ | [آیا تمرکز روی retention به درآمدزایی کمک می‌کند؟](chapters/16-is-focusing-on-retention-could-help-us-improve.md) | ۲۰۲۳-۰۲-۱۸ |
| ۱۷ | [استراتژی PLG و تحلیل محصول](chapters/17-plg-strategy-and-product-analytics.md) | ۲۰۲۳-۰۳-۰۷ |
| ۱۸ | [رشد PLG: جذب کاربر جدید](chapters/18-plg-growth-attracting-users.md) | ۲۰۲۳-۰۴-۱۱ |
| ۱۹ | [رشد PLG: فعال‌سازی کاربر جدید](chapters/19-plg-growth-activating-new-users.md) | ۲۰۲۳-۰۵-۰۸ |
| ۲۰ | [ضریب MCC یا تحلیل cohort؟](chapters/20-the-mcc-coefficient-or-cohort-analysis.md) | ۲۰۲۳-۰۵-۱۴ |
| ۲۱ | [تسلط بر ضریب MCC](chapters/21-mastering-the-mcc-coefficient.md) | ۲۰۲۳-۰۵-۲۳ |
| ۲۲ | [رشد PLG: نگه داشتن و پولی کردن کاربران](chapters/22-plg-growth-retaining-monetizing-users.md) | ۲۰۲۳-۰۶-۲۱ |
| ۲۳ | [رشد PLG: نگه داشتن کاربران](chapters/23-plg-growth-retaining-users.md) | ۲۰۲۳-۰۶-۲۷ |
| ۲۴ | [بینش‌های stickiness](chapters/24-in-the-last-post-i-discussed-how-stickiness-relates-to.md) | ۲۰۲۳-۰۷-۰۱ |
| ۲۵ | [بینش‌های stickiness، بخش دوم](chapters/25-stickiness-insights-part-2.md) | ۲۰۲۳-۰۷-۲۰ |
| ۲۶ | [تحلیل رشد Threads](chapters/26-threads-growth-analysis.md) | ۲۰۲۳-۰۷-۲۳ |
| ۲۷ | [بینش‌های stickiness، بخش سوم](chapters/27-stickiness-insights-part3.md) | ۲۰۲۳-۰۸-۰۱ |
| ۲۸ | [مدل‌های رشد](chapters/28-growth-models.md) | ۲۰۲۳-۰۸-۲۳ |
| ۲۹ | [درگیری کاربر: مقدمه](chapters/29-user-engagement-introduction.md) | ۲۰۲۳-۱۰-۱۹ |
| ۳۰ | [درگیری کاربر: بازه‌ی تحلیل](chapters/30-user-engagement-period-of-analysis.md) | ۲۰۲۳-۱۰-۲۹ |
| ۳۱ | [درگیری کاربر: تجربه‌ی اولیه‌ی کاربر](chapters/31-user-engagement-first-time-user-experience.md) | ۲۰۲۳-۱۱-۰۶ |
| ۳۲ | [درگیری کاربر: retention روز اول](chapters/32-user-engagement-d1-retention.md) | ۲۰۲۳-۱۱-۲۱ |
| ۳۳ | [retention روز اول: متریکی که پیش‌بینی‌اش حیله‌گر است](chapters/33-d1-retention-a-tricky-metric-to-predict.md) | ۲۰۲۳-۱۲-۰۶ |
| ۳۴ | [درگیری کاربر: رویدادهای کلیدی](chapters/34-user-engagement-key-events.md) | ۲۰۲۴-۰۱-۱۱ |
| ۳۵ | [چرا تحلیل محصول از تحلیل featureهای محصول فراتر می‌رود؟](chapters/35-why-does-product-analytics-go-beyond-product-feature.md) | ۲۰۲۴-۰۲-۱۹ |
| ۳۶ | [retention cohort کاربران](chapters/36-user-cohort-retention.md) | ۲۰۲۴-۰۳-۰۵ |
| ۳۷ | [retention مخلوط در برابر retention هر cohort](chapters/37-blended-retention-vs-cohort-retention.md) | ۲۰۲۴-۰۳-۰۹ |
| ۳۸ | [cohort کاربر را درست بسازید](chapters/38-how-to-build-user-cohort-properly.md) | ۲۰۲۴-۰۳-۱۵ |
| ۳۹ | [cohortهای کاربر را درست رنگ‌آمیزی و بخوانید](chapters/39-how-to-draw-and-read-user-cohorts-properly.md) | ۲۰۲۴-۰۳-۲۱ |
| ۴۰ | [همه‌ی cohortها پرنویزند، ولی بعضی داستانی می‌گویند](chapters/40-all-user-cohorts-are-noisy-but-some-can-tell-you-a-story.md) | ۲۰۲۴-۰۴-۰۱ |
| ۴۱ | [کی باید پیش‌بینی LTV داشت؟](chapters/41-when-do-you-need-to-use-the-ltv-projection.md) | ۲۰۲۴-۰۵-۰۹ |
| ۴۲ | [دوره‌ی بازگشت CAC](chapters/42-cac-payback-period.md) | ۲۰۲۴-۰۶-۰۲ |
| ۴۳ | [بنچمارک دوره‌ی بازگشت CAC](chapters/43-cac-payback-period-benchmarks.md) | ۲۰۲۴-۰۶-۱۰ |
| ۴۴ | [دوره‌ی بازگشت CAC در برابر LTV / CAC](chapters/44-cac-payback-period-vs-ltv-cac.md) | ۲۰۲۴-۰۶-۱۷ |
| ۴۵ | [LTV و سیگنال‌های رفتاری](chapters/45-ltv-and-behavioral-signals.md) | ۲۰۲۴-۰۷-۰۸ |
| ۴۶ | [پیش‌بینی LTV: مقدمه](chapters/46-ltv-forecasting-introduction.md) | ۲۰۲۴-۰۹-۱۶ |
| ۴۷ | [پیش‌بینی LTV: نبرد برای دقت](chapters/47-ltv-forecasting-battle-for-accuracy.md) | ۲۰۲۴-۱۰-۰۱ |
| ۴۸ | [پیش‌بینی LTV: مدل‌های اصلاحی چقدر خوب‌اند](chapters/48-ltv-forecasting-how-good-the-corrective-models-are.md) | ۲۰۲۴-۱۰-۲۲ |
| ۴۹ | [ماتریس RF: مقدمه](chapters/49-rf-matrix-introduction.md) | ۲۰۲۴-۱۲-۲۱ |
| ۵۰ | [ماتریس RF: جادوی Recency](chapters/50-rf-matrix-the-magic-of-recency.md) | ۲۰۲۵-۰۱-۰۷ |
| ۵۱ | [ماتریس RF: بُعد Frequency](chapters/51-rf-matrix-frequency-dimension.md) | ۲۰۲۵-۰۲-۱۰ |
| ۵۲ | [ماتریس‌های RR/FF: مقدمه‌ای بر وضعیت‌های مشتری](chapters/52-rr-ff-matrices-introduction-to-customer-states.md) | ۲۰۲۵-۰۳-۲۸ |
| ۵۳ | [وضعیت مشتری: بلوک سازنده‌ی تحلیل پیشرفته‌ی مشتری](chapters/53-customer-state-a-key-building-block-of-advanced-customer.md) | ۲۰۲۵-۰۴-۲۲ |
| ۵۴ | [دام درخت متریک](chapters/54-the-metric-tree-trap.md) | ۲۰۲۵-۰۶-۰۳ |
| ۵۵ | [قیف جذب کاربر](chapters/55-user-acquisition-funnel.md) | ۲۰۲۵-۰۸-۲۰ |
| ۵۶ | [نمودار گذار بین وضعیت‌های کاربر](chapters/56-user-transition-states-diagram.md) | ۲۰۲۵-۱۱-۱۲ |
| ۵۷ | [وقتی LTV دروغ می‌گوید: «مجانب مرگ»](chapters/57-when-ltv-can-lie-to-you-asymptote-of-death.md) | ۲۰۲۶-۰۲-۱۶ |
| ۵۸ | [چرا مدل LTV در Live-Ops پول را به آتش می‌کشد؟](chapters/58-why-your-live-ops-ltv-model-is-setting-money-on-fire.md) | ۲۰۲۶-۰۲-۲۳ |
| ۵۹ | [paywall روز دوم بهترین مشتریان آینده‌تان را می‌سوزاند](chapters/59-your-day-2-paywall-is-burning-your-best-future-customers.md) | ۲۰۲۶-۰۳-۰۲ |
| ۶۰ | [چهار پرسشی که تحلیل churn باید جواب بدهد](chapters/60-the-four-questions-churn-analysis-should-answer.md) | ۲۰۲۶-۰۳-۲۳ |
| ۶۱ | [D30 ROAS متریک اشتباهی است؛ به‌جایش چه بسنجیم](chapters/61-d30-roas-is-the-wrong-metric-here-is-what-to-use-instead.md) | ۲۰۲۶-۰۴-۰۸ |
| ۶۲ | [درخت متریک را تکه‌تکه نکنید](chapters/62-stop-decomposing-metric-tree.md) | ۲۰۲۶-۰۴-۱۴ |
| ۶۳ | [چرا بهترین سیگنال جذب کاربر از هیچ‌کاری‌نکردن درآمد کمتری می‌سازد؟](chapters/63-best-ua-signal-less-revenue-than-nothing.md) | ۲۰۲۶-۰۴-۱۸ |
| ۶۴ | [وقتی دم بلند مدل LTV را می‌خورد](chapters/64-long-tail-eats-your-ltv-model.md) | ۲۰۲۶-۰۴-۲۶ |
| ۶۵ | [وقتی منحنی retention بیشتر از آنچه نشان می‌دهد پنهان می‌کند](chapters/65-retention-curve-hides-more-than-it-shows.md) | ۲۰۲۶-۰۴-۲۷ |
| ۶۶ | [دو cohort، یک دوره‌ی payback، دو سرمایه‌گذاری کاملاً متفاوت](chapters/66-two-cohorts-same-payback-different-investments.md) | ۲۰۲۶-۰۴-۲۸ |
| ۶۷ | [شرکت Flo Health: «uplift صفر» واقعاً یعنی چه](chapters/67-flo-health-what-zero-uplift-really-means.md) | ۲۰۲۶-۰۵-۲۳ |
| ۶۸ | [چرا streak در Duolingo کار می‌کند، در چهار پرسش](chapters/68-why-duolingo-streaks-work-in-four-questions.md) | ۲۰۲۶-۰۵-۳۰ |
| ۶۹ | [در Duolingo، streak عدد نیست بلکه چرخه‌ی عمر است](chapters/69-a-streak-is-a-lifecycle.md) | ۲۰۲۶-۰۶-۰۵ |
| ۷۰ | [در Duolingo: ورود، ساختن، قفل شدن](chapters/70-getting-in-building-it-locking-in.md) | ۲۰۲۶-۰۶-۱۰ |
| ۷۱ | [چطور جهش churn را به mix و rate بشکنیم: راهنمای قدم‌به‌قدم LMDI](chapters/71-split-a-churn-spike-lmdi.md) | ۲۰۲۶-۰۹-۲۷ |

نوشته‌ها شماره‌ی صفحه ندارند؛ هر یادداشت به عنوان بخش‌های خود نوشته ارجاع می‌دهد، به شکل (بخش «عنوان»).

## مفهوم‌های کلیدی

| مفهوم | تعریف | نوشته‌ها |
|---|---|---|
| دام ترتیب | در drill-down پشت‌سرهم، بُعد اول واریانس بُعدهای زیرش را جذب می‌کند، پس پاسخ به ترتیبی بستگی دارد که انتخاب کرده‌اید. | [۶۲](chapters/62-stop-decomposing-metric-tree.md) · [۷۱](chapters/71-split-a-churn-spike-lmdi.md) |
| IV / WOE | معیار Weight of Evidence به هر دسته امتیاز می‌دهد و Information Value آن را برای هر بُعد جمع می‌زند؛ بُعدها مستقل از هر ترتیبی رتبه می‌گیرند و مخرج کسر تعیین می‌کند پرسش چیست. | [۶۲](chapters/62-stop-decomposing-metric-tree.md) · [۷۱](chapters/71-split-a-churn-spike-lmdi.md) |
| LMDI | روش Logarithmic Mean Divisia Index: تجزیه‌ی دقیق و بدون باقی‌مانده‌ی یک تغییر به اثرهای حجم و mix و rate و ARPU. | [۷۱](chapters/71-split-a-churn-spike-lmdi.md) |
| mix در برابر rate | تغییر یا از این می‌آید که چه کسانی در جمعیت‌اند، یعنی ترکیب، یا از این‌که هر گروه چطور رفتار می‌کند، یعنی ساختار. | [۶۶](chapters/66-two-cohorts-same-payback-different-investments.md) · [۶۷](chapters/67-flo-health-what-zero-uplift-really-means.md) · [۷۱](chapters/71-split-a-churn-spike-lmdi.md) |
| دام دقت | سیگنالی با ROAS درخشان ولی پوشش ناچیز، بودجه‌ی خیلی کمی را به کار می‌اندازد و از هیچ‌کاری‌نکردن کمتر درآمد می‌سازد. | [۶۳](chapters/63-best-ua-signal-less-revenue-than-nothing.md) |
| پرتگاه پوشش | سیگنال‌ها یا به کمتر از ۱۵٪ نصب‌ها می‌رسند یا به بیش از ۳۹٪؛ کمتر سیگنالی وسط این دو می‌نشیند. | [۶۳](chapters/63-best-ua-signal-less-revenue-than-nothing.md) |
| اختلاف مدل‌ها به‌عنوان بلاتکلیفی | مدل‌های معقول retention در جهت‌های مخالف سوگیری دارند؛ پراکندگی‌شان بلاتکلیفی LTV را اندازه می‌گیرد و میانگینشان از هر کدامشان مقاوم‌تر است. | [۶۴](chapters/64-long-tail-eats-your-ltv-model.md) |
| بنیان‌های دوبخشی | از برازش پرتگاه و دم: نرخ بازماندگان، نیمه‌عمر دم، شدت پرتگاه، سهم دم، سقف LTV و فاصله تا سقف. | [۶۵](chapters/65-retention-curve-hides-more-than-it-shows.md) · [۶۶](chapters/66-two-cohorts-same-payback-different-investments.md) |
| فاصله تا سقف | عدد ۱ منهای نسبت CAC به سقف LTV: فاصله‌ی شما تا نقطه‌ای که دیگر payback وجود ندارد. | [۶۵](chapters/65-retention-curve-hides-more-than-it-shows.md) · [۶۶](chapters/66-two-cohorts-same-payback-different-investments.md) |
| holdout | خاموش کردن تصادفی یک feature؛ تنها عدد تمیزِ علّی در یک مقایسه‌ی آشفته‌ی قبل و بعد. | [۶۷](chapters/67-flo-health-what-zero-uplift-really-means.md) |
| نشانه در برابر اهرم | برچسبی که فقط همراه ارزش حرکت می‌کند و بعد از کنترل کردن نیت پیشین محو می‌شود، در برابر ویژگی‌ای که واقعاً می‌توانید بکشیدش. | [۶۷](chapters/67-flo-health-what-zero-uplift-really-means.md) |
| دروازه، جمع، برهم‌کنش | سه شکل ترکیب شدن عامل‌ها: یکی همه چیز را ضرب می‌کند که همان روشنی است، چندتا با هم جمع می‌شوند که ساختن است، و چندتا باید هم‌زمان برقرار باشند که قفل شدن است. | [۶۸](chapters/68-why-duolingo-streaks-work-in-four-questions.md) · [۷۰](chapters/70-getting-in-building-it-locking-in.md) |
| چرخه‌ی عمر streak | شکل‌گیری که یک‌بار رخ می‌دهد، چرخه‌ی روزانه که تکرار می‌شود، و دوره‌ی بلند که رانش می‌کند، هر کدام از دید کاربر و از دید پلتفرم. | [۶۹](chapters/69-a-streak-is-a-lifecycle.md) · [۷۰](chapters/70-getting-in-building-it-locking-in.md) |
| Asymptote of Death | وقتی churn بالا با قیمت پایین روبه‌رو شود، درآمد تجمعی هر کاربر به سقف قیمت ÷ churn می‌رسد؛ اگر آن سقف زیر CAC بماند، payback هرگز رخ نمی‌دهد. | [۵۷](chapters/57-when-ltv-can-lie-to-you-asymptote-of-death.md) · [۴۳](chapters/43-cac-payback-period-benchmarks.md) |
| وضعیت مشتری و ماتریس RF | Recency و Frequency مشتری را در شبکه‌ای از وضعیت‌ها می‌گذارند؛ وضعیت قبلی و فعلی کنار هم مسیر مشتری را نشان می‌دهند: تندشده، کندشده، ماندگار. | [۴۹](chapters/49-rf-matrix-introduction.md) · [۵۲](chapters/52-rr-ff-matrices-introduction-to-customer-states.md) · [۵۳](chapters/53-customer-state-a-key-building-block-of-advanced-customer.md) |
| ماتریس گذار | نمودار وضعیت‌های کاربر با احتمال هر گذار؛ مجموع خروجی هر وضعیت ۱۰۰٪ است و ضرب ماتریس در زمان پیش‌بینی را ممکن می‌کند. | [۵۶](chapters/56-user-transition-states-diagram.md) |
| Direct و Inactive churn | دو شکل رفتن: کاربری که فوراً می‌رود و کاربری که تلاش می‌کند ولی ارزش نمی‌گیرد؛ ریشه و درمانشان فرق دارد. | [۵۵](chapters/55-user-acquisition-funnel.md) |
| Intent در برابر Solvency | رفتار درون محصول نیت را می‌سنجد، نه ظرفیت پرداخت؛ مدل باید این دو را جدا نگه دارد. | [۵۸](chapters/58-why-your-live-ops-ltv-model-is-setting-money-on-fire.md) |
| پیشنهاد متناسب با intent | به‌جای یک paywall برای همه، برای هر تیپ کاربر پیشنهاد و زمان خودش؛ تیپ‌های ارزان‌تر بعداً به تیپ‌های گران‌تر تبدیل می‌شوند. | [۵۹](chapters/59-your-day-2-paywall-is-burning-your-best-future-customers.md) |
| سه سطل churn | کاربر در هر روز یا churn قطعی است، یا safe قطعی، یا نامطمئن؛ اقدام فقط روی قطعی‌ها و منتظر ماندن برای بقیه. | [۶۰](chapters/60-the-four-questions-churn-analysis-should-answer.md) |
| D30 در برابر D180 | ROAS در افق کوتاه ترکیب «چه کسی را جذب کردید» و «آرکتایپش چه‌قدر سریع می‌پردازد» است؛ Churner زود و کم می‌پردازد و Whale دیر. | [۶۱](chapters/61-d30-roas-is-the-wrong-metric-here-is-what-to-use-instead.md) |
| دام درخت متریک | همبستگی‌های درخت ضربی هویت ریاضی‌اند و elasticity و اولویت نمی‌دهند. | [۵۴](chapters/54-the-metric-tree-trap.md) · [۶۲](chapters/62-stop-decomposing-metric-tree.md) |
| سقف رشد | پایه‌ی مشتری به نرخ جذب ماهانه تقسیم بر نرخ churn ماهانه میل می‌کند؛ churn کم‌تر یعنی رسیدن زودتر و نزدیک‌تر به این سقف. | [۱](chapters/01-churn-rate-evolution-at-netflix.md) · [۲۲](chapters/22-plg-growth-retaining-monetizing-users.md) |
| شمردن کاربر به‌جای رویداد | محبوبیت را با شمار و درصد کاربران بسنجید، جدا برای کاربر جدید و قدیمی؛ رویداد را کاربران پرمصرف یا یک باگ بالا می‌برند. | [۳](chapters/03-how-popular-is-this-feature-among-weekly-daily-active.md) · [۴](chapters/04-how-regular-are-users-using-this-feature-per-week.md) |
| خوشه‌بندی صدک ۵۰ و ۸۰ | مرزهای صدک ۵۰ و ۸۰ کاربران یا featureها را بدون مدل به سه گروه casual و power و core تقسیم می‌کنند. | [۶](chapters/06-clustering-users-based-on-weekly-habit-and-daily.md) · [۸](chapters/08-an-enhanced-version-of-the-analysis-of-how-product.md) |
| نُه خوشه‌ی feature | محبوبیت روی یک محور و درصد برگشته‌ها روی محور دیگر، هر کدام با صدک ۵۰ و ۸۰، نُه خوشه می‌سازد تا کیفیت بدون کمیت خوانده نشود. | [۸](chapters/08-an-enhanced-version-of-the-analysis-of-how-product.md) · [۱۵](chapters/15-how-a-successful-product-feature-should-look-like.md) |
| retention محلی و سراسری | کاربر به همان feature برمی‌گردد یا به هر جای محصول؛ تعریف «برگشته» عددها را عوض می‌کند. | [۹](chapters/09-two-types-of-feature-retention.md) · [۲۱](chapters/21-mastering-the-mcc-coefficient.md) |
| Information Gain | اطلاعاتی که استفاده یا عدم استفاده از یک feature درباره‌ی برگشتن می‌دهد، با حساب کردن غیرکاربران؛ جهت اثر را نمی‌گوید. | [۱۰](chapters/10-retention-deep-dive.md) · [۱۱](chapters/11-product-feature-retention-deep-dive-mcc-coefficient.md) |
| MCC | ضریب همبستگی Matthews بین دو متغیر دودویی، مثل استفاده و برگشتن؛ علامت دارد، پس اثر منفی را از مثبت جدا می‌کند، ولی علیت نیست. | [۱۱](chapters/11-product-feature-retention-deep-dive-mcc-coefficient.md) · [۱۳](chapters/13-user-flow.md) · [۲۰](chapters/20-the-mcc-coefficient-or-cohort-analysis.md) · [۲۱](chapters/21-mastering-the-mcc-coefficient.md) |
| Lness | توزیع شمار روزهای فعال کاربر در هفته، از L1 تا L7؛ به‌جای نسبت فشرده‌ی DAU/MAU که شکل این توزیع را پنهان می‌کند. | [۲۳](chapters/23-plg-growth-retaining-users.md) · [۲۵](chapters/25-stickiness-insights-part-2.md) · [۲۷](chapters/27-stickiness-insights-part3.md) |
| retention دوره به دوره | هر دوره را با دوره‌ی قبلش می‌سنجد، نه با ثبت‌نام؛ پنجره‌ی فرصت نگه داشتن کاربر را نشان می‌دهد. | [۲۴](chapters/24-in-the-last-post-i-discussed-how-stickiness-relates-to.md) |
| پنجره‌ی ۲۴ ساعته | دوره‌ها از لحظه‌ی ثبت‌نام هر کاربر شمرده می‌شوند، نه با روز تقویمی که به کاربران فرصت نابرابر می‌دهد. | [۳۰](chapters/30-user-engagement-period-of-analysis.md) · [۳۸](chapters/38-how-to-build-user-cohort-properly.md) |
| تجزیه‌ی D1 | شاخص D1 retention حاصل‌ضرب دو مرحله است: رسیدن به جلسه‌ی دوم در ۲۴ ساعت اول و برگشتن بعد از آن. | [۳۱](chapters/31-user-engagement-first-time-user-experience.md) · [۳۲](chapters/32-user-engagement-d1-retention.md) · [۳۳](chapters/33-d1-retention-a-tricky-metric-to-predict.md) |
| event کلیدی | رویدادی که انجامش با retention بیشترین همبستگی را دارد؛ با MCC و بر پایه‌ی cohort پیدا می‌شود، نه با نمای تقویمی. | [۳۴](chapters/34-user-engagement-key-events.md) · [۳۵](chapters/35-why-does-product-analytics-go-beyond-product-feature.md) |
| سه مرحله‌ی cohort | هر منحنی بقا ریزش دوره‌ی اول، خط میانی و دم بلند دارد، و هر کدام به عامل دیگری حساس است. | [۳۶](chapters/36-user-cohort-retention.md) · [۶۵](chapters/65-retention-curve-hides-more-than-it-shows.md) |
| retention آمیخته | نمای تقویمی cohortهایی با عمر متفاوت را در یک عدد می‌آمیزد و، حتی وقتی همه یک‌جور رفتار می‌کنند، بقای واقعی را بیش از اندازه نشان می‌دهد. | [۳۷](chapters/37-blended-retention-vs-cohort-retention.md) |
| رنگ‌بندی آماری cohort | سلول جدول cohort وقتی رنگ می‌گیرد که بیش از دو انحراف معیار از میانگین ۷ روز قبل فاصله دارد، نه بر پایه‌ی مقدار خامش. | [۳۹](chapters/39-how-to-draw-and-read-user-cohorts-properly.md) · [۴۰](chapters/40-all-user-cohorts-are-noisy-but-some-can-tell-you-a-story.md) |
| CAC payback و LTV به CAC | یکی سرعت برگشت پول جذب را می‌سنجد و دیگری کارایی سرمایه را؛ payback قاعده‌ی سرانگشتی نقدینگی است و جای ROI را نمی‌گیرد. | [۴۲](chapters/42-cac-payback-period.md) · [۴۳](chapters/43-cac-payback-period-benchmarks.md) · [۴۴](chapters/44-cac-payback-period-vs-ltv-cac.md) |
| مدل تصحیحی LTV | مدل دومی که خطای سیستماتیک پیش‌بینی LTV با داده‌ی کم را یاد می‌گیرد و بخش بزرگی از آن را برمی‌دارد. | [۴۶](chapters/46-ltv-forecasting-introduction.md) · [۴۷](chapters/47-ltv-forecasting-battle-for-accuracy.md) · [۴۸](chapters/48-ltv-forecasting-how-good-the-corrective-models-are.md) |
| Recency | زمان از آخرین خرید؛ قوی‌ترین سیگنال خرید بعدی، قوی‌تر از Frequency. | [۵۰](chapters/50-rf-matrix-the-magic-of-recency.md) · [۵۱](chapters/51-rf-matrix-frequency-dimension.md) |

## این یادداشت‌ها چطور نوشته شده‌اند

- هر چیزی که در یادداشت یک نوشته بالای *فراتر از کتاب* است، خود آن نوشته را بازگو می‌کند و به عنوان بخش‌هایش ارجاع می‌دهد؛ بقیه مال vault است.
- عددهای نویسنده از شبیه‌سازی‌های خودش می‌آیند، و برای نوشته‌های Duolingo از گفت‌وگویی در یک پادکست عمومی که خودش اندازه‌اش نگرفته؛ یادداشت‌ها این وضعیت را پیدا نگه می‌دارند.
- نمودارهای داخل نوشته‌ها مال نویسنده‌اند و کپی نشده‌اند؛ شبیه‌سازی‌های vault همان سازوکارها را با کد خودش بازمی‌سازند و هر کدام می‌گویند کدام عددها را از نوشته برداشته‌اند و کدام را فرض کرده‌اند.
- پرسش‌ها و پاسخ‌های *خودتان را بسنجید* مال vault است و از روی همین یادداشت‌ها نوشته شده‌اند.

## منبع

- **منبع اصلی:** پروفایل نویسنده در Medium به نشانی <https://medium.com/@paul.levchuk>، فهرست کامل ۷۱ نوشته از GraphQL خود Medium در ۲۰۲۶-۱۱-۰۹ گرفته شد و متن نوشته‌ها از راه یک آینه‌ی خواننده استخراج شد. هر فصل به نوشته‌ی خودش لینک می‌دهد.
- **ترتیب و تاریخ‌ها:** بر پایه‌ی تاریخ انتشار در فهرست Medium.
- **راستی‌آزمایی‌نشده:** نمودارهای نوشته‌ها به شکل تصویر خوانده شده‌اند؛ عددهایی که فقط در نمودار می‌آیند جایی به کار رفته‌اند که متن هم آن‌ها را گفته یا یادداشتی می‌گوید که نمودار خوانده شده. دنیاهای شبیه‌سازی‌شده‌ی نویسنده، یعنی cohortها و سیگنال‌ها و آزمایش شبیه Flo، همان‌طور که خود نوشته‌ها می‌گویند توضیحی‌اند، نه داده‌ی واقعی production.
