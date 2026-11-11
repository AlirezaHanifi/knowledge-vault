# پیاده‌سازی multimethodها از صفر

یک `multi` و `method` ناچیز به Python: تابعی توزیع‌کننده به‌علاوه‌ی hash mapی از مقدارهای توزیعی به متدها، با پیش‌فرضی اختیاری. اسکریپت توزیع یگانه را با `greet` و توزیع چندگانه را با `greetLang` و توزیع پویا را با `dysGreet` replay می‌کند. بعد `Author.myName` را از مرزهای پرکاری جدول ۱۳.۱ می‌گذراند.

*تصویری از فصل ۱۳ کتاب Data-Oriented Programming، صص. ۲۷۷–۲۹۳ (listingهای ۱۳.۶ تا ۱۳.۲۹). آن پیاده‌سازی جای کتابخانه‌ی arrows/multimethod می‌نشیند. نام‌های Fidelio و Milou و شمار کتاب‌ها و قالب `pdf` ورودی‌های تست vault است.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 multimethods.py
```

## خروجی چشم‌داشته

```text
Single dispatch on the animal's type
  greet: Woof woof! My name is Fido
  greet: Meow! I am Milo
  greet: Moo! Call me Clarabelle
  greet(Horace) before a default: NoMethodError, no method for dispatch value 'horse'
  greet(Horace) after method(greetDefault): My name is Horace

Multiple dispatch on [animal type, language type]: 6 methods
  greetLang: Ouaf Ouaf! Je m'appelle Fido et je parle Français
  greetLang: Woof woof! My name is Fido and I speak English
  greetLang: Miaou! Je m'appelle Milo et je parle Français
  greetLang: Meow! I am Milo and I speak English
  greetLang: Meuh! Appelle moi Clarabelle et je parle Français
  greetLang: Moo! Call me Clarabelle and I speak English

Dynamic dispatch on [animal type, name longer than 5 letters]
  dysGreet('Fido', 4 letters): Woof woof!
  dysGreet('Clarabelle', 10 letters): Moo! Call me Clarabelle
  dysGreet('Milo', 4 letters): Meow!
  dysGreet('Fidelio', 7 letters): Woof woof! My name is Fidelio
  dysGreet('Milou', 5 letters): Meow!

Author.myName across the boundaries of table 13.1
  books  level   html                               markdown
      1  low     <i>Yehonathan Sharvit</i>          *Yehonathan Sharvit*
     10  low     <i>Yehonathan Sharvit</i>          *Yehonathan Sharvit*
     11  medium  <b>Yehonathan Sharvit</b>          **Yehonathan Sharvit**
     50  medium  <b>Yehonathan Sharvit</b>          **Yehonathan Sharvit**
     51  high    <b><i>Yehonathan Sharvit</i></b>   ***Yehonathan Sharvit***
     80  high    <b><i>Yehonathan Sharvit</i></b>   ***Yehonathan Sharvit***
  format 'pdf': Author.myName called with invalid arguments: data/1 must be equal to one of the allowed values
```

## به چه چیزی نگاه کنید

- اسب Horace تا ثبت شدن `greetDefault` هیچ متدی ندارد. افزودنش هیچ متد دیگری را ویرایش نمی‌کند: همان گسترش‌پذیری است که فصل در پی‌اش است.
- آن شش خط `greetLang` با خروجی‌های listing ۱۳.۱۷ می‌خوانند.
- تابع `dysGreet` بر پایه‌ی اینکه آن نام بیش از پنج حرف دارد یا نه توزیع می‌کند: نام Milou با ۵ حرف کوتاه است و Fidelio با ۷ حرف دراز.
- شمار ۱۰ کتاب هنوز low است، ۱۱ همان medium، ۵۰ هنوز medium، و ۵۱ همان high. آن enum قالب هر چیزی جز HTML و Markdown را رد می‌کند.

## مرتبط

- یادداشت فصل: [فصل ۱۳: polymorphism](../../chapters/13-polymorphism.md) — بخش‌های ۱۳.۲ تا ۱۳.۵، صص. ۲۷۷–۲۹۳
