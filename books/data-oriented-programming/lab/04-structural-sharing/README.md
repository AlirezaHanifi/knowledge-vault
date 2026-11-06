# Structural sharing in numbers

How much does an immutable update really copy? A Python port of `setImmutable` sets one book's publication year in libraries of 10 to 10,000 books. The script counts the maps it creates, the slots it copies, and the maps it shares with the previous version, compared with a deep copy. Then it keeps 1,000 versions of a 1,000-book library and counts the maps they hold together.

*Illustrates Data-Oriented Programming, chapter 4, sections 4.2–4.3, pp. 75–81: structural sharing, and Dave's `setImmutable` (listing 4.4, p. 81). The library's shape follows figure 4.2; its size, the authors and the random updates are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 structural_sharing.py
```

## Expected output

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

## What to look for

- Exactly 4 maps are new after one update, one per level of the path (library, catalog, `booksByIsbn`, the book), whatever the library's size. Everything else is shared, including `userManagement` and the sibling books.
- *Slots copied* grows with the collection: the shallow clone of `booksByIsbn` copies every key. That's the slowdown chapter 9 sets out to fix with persistent data structures.
- A deep copy creates as many maps as the library holds. That's 35,308 for 10,000 books, against 4.
- A thousand shared versions hold only about twice the maps of one version. A thousand deep copies would hold a thousand times as many.

## Related

- Chapter note: [4. State management](../../chapters/04-state-management.md) — sections 4.2–4.3, pp. 75–81
