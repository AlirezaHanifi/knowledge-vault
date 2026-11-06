# Custom data tools

`update`, `flatMap`, `countByBoolField` and `unwind` in Python, run on the chapter's data: the income map, the two books with their book items, and Joe's cart. The script then runs `update` and `unwind` again with a `set` that mutates in place, as default Lodash's `_.set` does.

*Illustrates Data-Oriented Programming, chapter 14, pp. 296–309 (listings 14.3–14.19). The duplicated author in step 1 is the vault's example; the mutating-set comparison illustrates the vault note in the lesson.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 custom_data_tools.py
```

## Expected output

```text
update (listings 14.2-14.4)
  update(m, 'income', x * 2): {'position': 'manager', 'income': 200000} | m is unchanged: {'position': 'manager', 'income': 100000}
  removeAuthorDuplicates: ['Alan Moore', 'Dave Gibbons']

flatMap (listings 14.5-14.9)
  map:     [["alan-moore", "dave-gibbons"], ["sean-covey", "stephen-covey"]]
  flatMap: ["alan-moore", "dave-gibbons", "sean-covey", "stephen-covey"]

countByBoolField (listings 14.13-14.15)
  test of listing 14.14: {'aTrue': 3, 'aFalse': 1}
  book items: {'lent': 2, 'notLent': 1} -> lendingRatio = 0.6667

unwind (listings 14.17-14.19)
   {"customer-id": "joe", "items": {"item": "phone", "quantity": 1}}
   {"customer-id": "joe", "items": {"item": "pencil", "quantity": 10}}
  cart is unchanged: [{"item": "phone", "quantity": 1}, {"item": "pencil", "quantity": 10}]
  books grouped by library:
    nyc-central-lib: Watchmen (book-item-1), 7 Habits of Highly Effective People (book-item-17)
    hudson-park-lib: 7 Habits of Highly Effective People (book-item-123)

The same with a mutating set (the vault note in the lesson)
   {"customer-id": "joe", "items": {"item": "pencil", "quantity": 10}}
   {"customer-id": "joe", "items": {"item": "pencil", "quantity": 10}}
  both results are the same object: True | the cart itself was changed: {"item": "pencil", "quantity": 10}
  update with a mutating set changes its input: m = {'income': 200000} | same object: True
  books grouped by library: {'nyc-central-lib': ['book-item-1', 'book-item-17', 'book-item-17']}
```

## What to look for

- `update` returns a new map and leaves its input alone; `countByBoolField` passes listing 14.14's test, and the lending ratio of the sample is 2/3.
- `unwind` turns the cart into two maps with one item each, and the cart is unchanged.
- Grouping the unwound books by `bookItems.libId` puts Watchmen and one copy of 7 Habits at nyc-central-lib, and the other copy at hudson-park-lib.
- With a mutating set, `unwind` returns the same object twice, each showing the last item, and changes the cart. `update` changes its input. The grouping then collapses into one library with a duplicated item.

## Related

- Chapter note: [14. Advanced data manipulation](../../chapters/14-advanced-data-manipulation.md) — sections 14.1–14.4, pp. 296–309
