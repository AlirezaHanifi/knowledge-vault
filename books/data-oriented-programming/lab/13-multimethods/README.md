# Multimethods from scratch

A tiny `multi` and `method` in Python: a dispatch function plus a hash map from dispatch values to methods, with an optional default. The script replays single dispatch with `greet`, multiple dispatch with `greetLang` and dynamic dispatch with `dysGreet`. Then it runs `Author.myName` across the prolificity boundaries of table 13.1.

*Illustrates Data-Oriented Programming, chapter 13, pp. 277–293 (listings 13.6–13.29). The implementation stands in for the arrows/multimethod library. Fidelio, Milou, the book counts and the `pdf` format are the vault's test inputs.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 multimethods.py
```

## Expected output

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

## What to look for

- Horace has no method until `greetDefault` is registered. Adding it doesn't edit any other method: that's the extensibility the chapter is after.
- The six `greetLang` lines match listing 13.17's outputs.
- `dysGreet` dispatches on whether the name has more than five letters: Milou (5) is short, Fidelio (7) is long.
- 10 books is still low, 11 is medium, 50 is still medium, and 51 is high. The format enum rejects anything but HTML and Markdown.

## Related

- Chapter note: [13. Polymorphism](../../chapters/13-polymorphism.md) — sections 13.2–13.5, pp. 277–293
