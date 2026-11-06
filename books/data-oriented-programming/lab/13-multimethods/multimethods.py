"""Multimethods from scratch: DOP chapter 13 (pp. 277-293).

A tiny multi/method in the spirit of the arrows/multimethod library: a dispatch
function plus a hash map from dispatch values to methods, with an optional default.
Replays single dispatch (greet), multiple dispatch (greetLang), dynamic dispatch
(dysGreet) and Author.myName's prolificity boundaries.
Standard library only; no randomness.
"""


class NoMethodError(Exception):
    pass


def _key(v):
    return tuple(v) if isinstance(v, list) else v


def multi(dispatch):
    table, default = {}, []

    def call(*args):
        v = dispatch(*args)
        if _key(v) in table:
            return table[_key(v)](*args)
        if default:
            return default[0](*args)
        raise NoMethodError(f"no method for dispatch value {v!r}")
    call.table, call.default = table, default
    return call


def method(*args):
    """method(value, fn) adds a method; method(fn) sets the default. Returns a function of the multimethod."""
    def add(mm):
        if len(args) == 1:
            mm.default[:] = [args[0]]
        else:
            mm.table[_key(args[0])] = args[1]
        return mm
    return add


my_dog, my_cat, my_cow = {"type": "dog", "name": "Fido"}, {"type": "cat", "name": "Milo"}, {"type": "cow", "name": "Clarabelle"}
my_horse = {"type": "horse", "name": "Horace"}
french, english = {"type": "fr", "name": "Français"}, {"type": "en", "name": "English"}

# Single dispatch (listings 13.6-13.12)
greet = multi(lambda animal: animal["type"])
greet = method("dog", lambda a: "Woof woof! My name is " + a["name"])(greet)
greet = method("cat", lambda a: "Meow! I am " + a["name"])(greet)
greet = method("cow", lambda a: "Moo! Call me " + a["name"])(greet)
print("Single dispatch on the animal's type")
for a in (my_dog, my_cat, my_cow):
    print("  greet:", greet(a))
try:
    greet(my_horse)
except NoMethodError as e:
    print("  greet(Horace) before a default:", "NoMethodError,", e)
greet = method(lambda a: "My name is " + a["name"])(greet)     # added elsewhere, nothing else edited
print("  greet(Horace) after method(greetDefault):", greet(my_horse))
print()

# Multiple dispatch (listings 13.15-13.17)
greet_lang = multi(lambda animal, language: [animal["type"], language["type"]])
EN = {"dog": "Woof woof! My name is ", "cat": "Meow! I am ", "cow": "Moo! Call me "}
FR = {"dog": "Ouaf Ouaf! Je m'appelle ", "cat": "Miaou! Je m'appelle ", "cow": "Meuh! Appelle moi "}
for t in EN:
    greet_lang = method([t, "en"], lambda a, l, t=t: EN[t] + a["name"] + " and I speak " + l["name"])(greet_lang)
    greet_lang = method([t, "fr"], lambda a, l, t=t: FR[t] + a["name"] + " et je parle " + l["name"])(greet_lang)
print("Multiple dispatch on [animal type, language type]: 6 methods")
for a in (my_dog, my_cat, my_cow):
    for lang in (french, english):
        print("  greetLang:", greet_lang(a, lang))
print()

# Dynamic dispatch (listings 13.18-13.20)
dys_greet = multi(lambda animal: [animal["type"], len(animal["name"]) > 5])
SHORT = {"dog": "Woof woof!", "cat": "Meow!", "cow": "Moo!"}
for t in EN:
    dys_greet = method([t, True], lambda a, t=t: EN[t] + a["name"])(dys_greet)
    dys_greet = method([t, False], lambda a, t=t: SHORT[t])(dys_greet)
print("Dynamic dispatch on [animal type, name longer than 5 letters]")
for a in (my_dog, my_cow, my_cat, {"type": "dog", "name": "Fidelio"}, {"type": "cat", "name": "Milou"}):
    print(f"  dysGreet({a['name']!r}, {len(a['name'])} letters):", dys_greet(a))
print()


# Author.myName (listings 13.23-13.29)
def prolificity_level(author):
    books = len(author["bookIsbns"])
    if books <= 10:
        return "low"
    if books >= 51:
        return "high"
    return "medium"


def author_name_dispatch(author, fmt):
    if fmt not in ("markdown", "html"):          # the enum of authorNameArgsSchema
        raise ValueError("Author.myName called with invalid arguments: data/1 must be equal to one of the allowed values")
    return [prolificity_level(author), fmt]


my_name = multi(author_name_dispatch)
WRAP = {("low", "html"): ("<i>", "</i>"), ("medium", "html"): ("<b>", "</b>"), ("high", "html"): ("<b><i>", "</i></b>"),
        ("low", "markdown"): ("*", "*"), ("medium", "markdown"): ("**", "**"), ("high", "markdown"): ("***", "***")}
for (lv, fmt), (o, c) in WRAP.items():
    my_name = method([lv, fmt], lambda a, f, o=o, c=c: o + a["name"] + c)(my_name)
print("Author.myName across the boundaries of table 13.1")
print(f"  {'books':>5}  {'level':<7} {'html':<34} markdown")
for n in (1, 10, 11, 50, 51, 80):
    author = {"name": "Yehonathan Sharvit", "bookIsbns": ["9781617298578"] * n}
    print(f"  {n:>5}  {prolificity_level(author):<7} {my_name(author, 'html'):<34} {my_name(author, 'markdown')}")
try:
    my_name({"name": "Yehonathan Sharvit", "bookIsbns": []}, "pdf")
except ValueError as e:
    print("  format 'pdf':", e)
