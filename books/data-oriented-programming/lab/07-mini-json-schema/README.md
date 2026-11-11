# اعتبارسنج کوچک JSON Schema

کلیدواژه‌های JSON Schema این فصل در حدود صد خط Python: `type` و `properties` و `required` و `items` و `enum` و `additionalProperties` و `allOf` و `anyOf` و `oneOf`. خطاها به سبک Ajv می‌آیند، با کلیدی برای همه‌ی خطاها. اسکریپت درخواست‌ها و پاسخ‌های پایگاه داده و پاسخ‌های Open Library این فصل را از آن می‌گذراند.

*تصویری از فصل ۷ کتاب Data-Oriented Programming، صص. ۱۴۴–۱۶۱ (listingهای ۷.۶ تا ۷.۲۳). آن اعتبارسنج مال vault است؛ زیرمجموعه‌ای آموزشی است، نه پیاده‌سازی کامل JSON Schema.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 mini_json_schema.py
```

## خروجی چشم‌داشته

```text
Search requests (listings 7.6-7.9)
7.8  title, fields of strings                              valid
7.9  'tilte' typo                                          INVALID: data must have required property 'title'
7.7  the same request against the enum of 7.6              INVALID: data/fields/0 must be equal to one of the allowed values

Database responses (listings 7.13-7.15)
7.14 extra dummy_property, default schema                  valid
7.15 extra dummy_property, additionalProperties: false     INVALID: data/0 must NOT have additional properties

Open Library responses (listings 7.16-7.19)
7.19 Watchmen (both ISBNs), allOf + anyOf                  valid
     Watchmen with only isbn_10, allOf + anyOf             valid
     Watchmen with no ISBN, allOf + anyOf                  INVALID: data must match a schema in anyOf
     Watchmen (both ISBNs), allOf + oneOf                  INVALID: data must match exactly one schema in oneOf

Error details (listings 7.20-7.23)
7.21 first error only: [{"instancePath": "", "schemaPath": "#/required", "keyword": "required", "message": "must have required property 'title'"}]
7.23 myTitle and fields [1, 2], first error (default)      INVALID: data must have required property 'title'
7.23 myTitle and fields [1, 2], allErrors: true            INVALID: data must have required property 'title', data/fields/0 must be string, data/fields/1 must be string
```

## به چه چیزی نگاه کنید

- درخواست listingهای ۷.۷ و ۷.۸ فیلد `title` را می‌خواهد، که آن enum از listing ۷.۶ فهرستش نمی‌کند. در برابر آن طرح نامعتبر است.
- فیلدهای نگفته پیش‌فرض روایند و مقدار `dummy_property` رد می‌شود، تا `additionalProperties: false`.
- کلیدواژه‌ی `allOf` با `anyOf` کتاب Watchmen را با هر دو ISBN یا تنها یکی می‌پذیرد، و با هیچ‌کدام ردش می‌کند. با `oneOf` به‌جای `anyOf`، آن Watchmen شکست می‌خورد، چون هر دو را دارد.
- پیش‌فرض تنها نخستین شکست گزارش می‌شود. با روشن بودن همه‌ی خطاها، درخواست listing ۷.۲۳ همان سه خطایی را می‌دهد که کتاب نشان می‌دهد.

## مرتبط

- یادداشت فصل: [فصل ۷: اعتبارسنجی پایه‌ی داده](../../chapters/07-basic-data-validation.md) — بخش‌های ۷.۲ تا ۷.۵، صص. ۱۴۴–۱۶۱
