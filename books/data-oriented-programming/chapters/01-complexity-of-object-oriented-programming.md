---
book: data-oriented-programming
chapter: 1
title: "Complexity of object-oriented programming"
pages: "3–25"
---

# 1. Complexity of object-oriented programming

[Book](../README.md) · [2. Separation between code and data →](02-separation-between-code-and-data.md)

## Summary

Theo, a senior tech lead at the agency Albatross, designs Klafim's library management prototype the classic object-oriented way. He draws a UML class diagram of nine classes and walks Dave, a junior developer, through it (pp. 4–12). The author then challenges the design. The design isn't wrong; the trouble is a tendency of OOP itself to make systems **hard to understand**, which is what "complexity" means throughout the book (p. 13). The chapter traces that complexity to four aspects of OOP (table 1.1, p. 14):

- **Code and data are mixed**, so classes take part in many relations.
- **Objects are mutable**, so reading code takes extra thinking, and multi-threaded code needs explicit synchronization.
- **Data is locked in objects**, so serialization isn't trivial.
- **Code is locked in classes**, so class hierarchies get complex.

Two "tiny" late features, VIP members and Super members, turn Theo's hierarchy into three "Deadly Diamonds of Death," and he misses the deadline (pp. 20–24).

## Key takeaways

- **Complexity means hard to understand.** The definition comes from Moseley and Marks's paper "Out of the Tar Pit" (2006). It is relative, not absolute, and has nothing to do with resource consumption (p. 13).
- **The book isn't a critique of OOP.** DOP is compatible with both OOP and FP, and appendix A shows DOP principles applied in both styles (pp. 4, 13).
- **Mixing code and data multiplies relations.** `Member` alone takes part in five relations; splitting every class into a code entity and a data entity leaves two independent subsystems (pp. 14–16).
- **When data is mutable, code is unpredictable.** Reading `this.isBlocked` twice can give two answers in a multi-threaded environment, or with asynchronous code in JavaScript (pp. 16–18).
- **Data locked in members makes serialization costly.** Every JSON endpoint needs its own query and result classes, because there is no simple generic way to access the data (pp. 18–20).
- **Code locked in classes makes hierarchies brittle.** Reusing `addBookItem` for VIP members forces a new base class and multiple inheritance (pp. 20–24).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- 1.1 OOP design: Classic or classical? — p. 4
  - 1.1.1 The design phase — p. 4
  - 1.1.2 UML 101 — p. 6
  - 1.1.3 Explaining each piece of the class diagram — p. 9
  - 1.1.4 The implementation phase — p. 12
- 1.2 Sources of complexity — p. 13
  - 1.2.1 Many relations between classes — p. 14
  - 1.2.2 Unpredictable code behavior — p. 16
  - 1.2.3 Not trivial data serialization — p. 18
  - 1.2.4 Complex class hierarchies — p. 20
- Summary — p. 24

## Notes

The book is a story. In the part 1 opener (pp. 1–2), Nancy, an entrepreneur, meets Theo at a coffee shop near the San Francisco Zoo. Her startup Klafim is a social network for books that lets users borrow books from local libraries, and the one piece of custom software it needs is a "Global Library Management System." She writes the prototype's requirements on a napkin, and Theo commits to deliver in two weeks.

| Klafim prototype requirement (pp. 2, 4) |
|---|
| Two kinds of users: library members and librarians |
| Users log in with email and password |
| Members can borrow books |
| Members and librarians can search books by title or by author |
| Librarians can block and unblock members (e.g., when they are late returning a book) |
| Librarians can list the books currently lent to a member |
| A book can have several copies |
| A book belongs to a physical library |

### 1.1 OOP design: Classic or classical?

Theo works at Albatross, a consulting company whose Startup department has lost its customers' trust. Management moved him there from the Enterprise department to close deals and deliver on time (p. 4).

#### 1.1.1 The design phase

For an object-oriented programmer, every business entity is an object made from a class (p. 4). Theo identifies the main classes (p. 5):

| Class | Role |
|---|---|
| `Library` | The central part of the design |
| `Book` | A book |
| `BookItem` | One copy of a book |
| `BookLending` | Created when a book is lent |
| `Member` | A library member |
| `Librarian` | A librarian |
| `User` | Base class of `Librarian` and `Member` |
| `Catalog` | Contains a list of books |
| `Author` | A book author |

The relations are the hard part; after about two hours he has figure 1.1 (p. 6). The author notes that the design is deliberately naive: experienced OOP developers would use design patterns for a better one, but it is rich enough to start coding and to show the complexity of a typical OOP system (p. 5).

#### 1.1.2 UML 101

Theo explains the four kinds of arrows to Dave (pp. 6–9):

| Relation | Meaning | UML symbol |
|---|---|---|
| Composition | When one object dies, the other dies too (`Library` owns its `Catalog` one-to-one, and its `Member`s one-to-many) | Plain diamond at one edge, optional star at the other |
| Association | Each object has an independent life cycle (`Book` and `Author`, many-to-many) | Empty diamond and a star at both edges |
| Usage | A class uses a method of another class (`Librarian::blockMember` calls `Member::block`) | Dashed arrow |
| Inheritance | A class derives from another (`Member` from `User`) | Plain arrow with an empty triangle, pointing at the superclass |

#### 1.1.3 Explaining each piece of the class diagram

The roles of the classes (pp. 9–12):

- **`Library`** does nothing on its own: it delegates everything to the objects it owns, which are many `Member`s, many `Librarian`s and one `Catalog`. (The book uses *code* and *behavior* interchangeably.)
- **`User`** has an `id`, `email` and `password`, with no security yet, and can `login`.
- **`Member`** adds no data to `User`. It can `checkout`, `returnBook`, `block`, `unblock` and answer `isBlocked`. It owns many `BookLending`s and uses `BookItem` to implement `checkout`.
- **`Librarian`** adds no data either. It can block and unblock a `Member`, list a member's lendings and add book items. It uses `Member`, `BookItem` and `BookLending`.
- **`Catalog`** can `search` books and `addBookItem`, using `Librarian`. It owns many `Book`s.
- **`Book`** has an `id` and a `title`. It is associated with many `Author`s and owns many `BookItem`s.
- **`BookItem`** has an `id` and a `libId`, the ID of its physical library. It owns a `BookLending` for each time it is lent, and can be checked out.

#### 1.1.4 The implementation phase

Dave is impressed that people write down their design in such detail; Theo says it saves him a lot of time when coding (p. 12).

### 1.2 Sources of complexity

The design may look clear on paper, but the author claims it makes the system hard to understand. That comes from the paradigm, not from Theo's choice of classes (p. 13). "Complexity" here is the kind that makes systems hard to understand, as defined in "Out of the Tar Pit" (Moseley and Marks, 2006), not resource consumption, and "simple" means easy to understand. Both are relative: you can say system A is more complex than system B (p. 13).

According to DOP, the main sources of complexity in Theo's system, and in many traditional OOP systems, are four (p. 13). This resembles functional programming's critique of OOP, but DOP's data approach to reducing complexity differs from FP's (p. 13).

| Aspect | Impact on complexity (table 1.1, p. 14) |
|---|---|
| Code and data are mixed | Classes tend to be involved in many relations |
| Objects are mutable | Extra thinking is needed when reading code |
| Objects are mutable | Explicit synchronization is required in multi-threaded environments |
| Data is locked in objects | Data serialization is not trivial |
| Code is locked in classes | Class hierarchies are complex |

#### 1.2.1 Many relations between classes

Looking only at entities and relations (figure 1.10, p. 14), `Member` takes part in five relations (p. 15):

![The whole Library Management System class diagram: Library, Catalog, Librarian, Member, Book, Author, BookItem, BookLending and User joined by composition, association, inheritance and usage arrows](../figures/01-10.png)

*Figure 1.10 (p. 14): even a small system's class diagram becomes a web of crossing relations.*

- **Data relations:** `Library` has many `Member`s, and a `Member` has many `BookLending`s.
- **Code relations:** `Member` extends `User`, `Librarian` uses `Member`, and `Member` uses `BookItem`.

Split it into `MemberCode` (three relations) and `MemberData` (two relations), and the diagram falls into two independent parts, each easier to understand (pp. 15–16). Splitting *every* class (figure 1.13, p. 16) gives one subsystem of data entities only and one of code entities only, which can be understood separately and in any order. The book stresses that this isn't simpler by accident: it follows logically from separating code from data (p. 16).

![Member at the centre of five relations: Library has many Members, Member has many BookLendings, Member extends User, Librarian uses Member, and Member uses BookItem](../figures/01-11.png)

*Figure 1.11 (p. 15): five relations meet on one entity because `Member` mixes code and data.*

![After the split: Library owns MemberData, which owns BookLendings; Librarian uses MemberCode, which extends User and uses BookItem](../figures/01-12.png)

*Figure 1.12 (p. 15): the same five relations become two on the data entity and three on the code entity.*

> **Try it:** [Split code from data](../widgets/01-code-data-split.html) — take Theo's class diagram, split classes into code and data entities one at a time, and watch the relations per entity and the independent parts change.

#### 1.2.2 Unpredictable code behavior

Two versions of `displayBlockedStatusTwice` (listings 1.1 and 1.2, p. 17):

- **Listing 1.1** copies `this.isBlocked` into a local variable and prints it twice. If the first print is `true`, so is the second.
- **Listing 1.2** prints `this.isBlocked` twice. In a single-threaded environment both print `true`. In a multi-threaded one it is unpredictable, because a context switch between the two calls can change the object, for example when a librarian unblocks the member. The same can happen in single-threaded JavaScript when asynchronous code modifies the data (appendix A, Principle #3).

The difference is that the first reads a primitive value, while the second reads a member of a mutable object. **When data is mutable, code is unpredictable** (p. 17). OOP can protect such code with mutexes, at the cost of a performance hit and a risk of deadlocks. DOP instead treats all data, primitives and collections alike, as immutable values (p. 18).

#### 1.2.3 Not trivial data serialization

In a dream, Nancy asks Theo for a REST API with JSON. A `/search` endpoint takes `{"searchCriteria": "author", "query": "albert"}` and returns books with their authors' full names (listings 1.3–1.4, p. 18). In OOP that means three classes (p. 19):

- `SearchController` handles the query.
- `SearchQuery` converts the JSON string into data.
- `SearchResult` converts the results back into a JSON string.

An `/add-book-item` endpoint needs three more classes, rewriting the same (de)serialization code, and so on for every endpoint (pp. 19–20). Yet serializing any query comes down to going over the data fields and concatenating names and values. It is hard in OOP because data follows a rigid shape defined in classes; **data is locked in members**, with no simple generic access (p. 20). Most OOP languages ease JSON conversion a little, but only through reflection, which is complex, or through verbosity (p. 20).

#### 1.2.4 Complex class hierarchies

Inheritance avoids duplication when all requirements are known up front: `Librarian` and `Member` both inherit `login` from `User` (p. 20). Late requirements are another story (pp. 20–24):

1. **VIP members** may add book items themselves. The code that does this is locked in `Librarian::addBookItem`, and `VIPMember` can't derive from `Librarian`, because VIP members may not block members or list lendings. Theo's fix (figure 1.16) adds a base class `UserWithBookItemRight` that holds `addBookItem`, and makes both `Librarian` and `VIPMember` extend it. `VIPMember` also extends `Member`, which creates a diamond, because both bases extend `User`.
2. **Super members** may list the books lent to other members. Theo's plan (figure 1.17) adds `UserWithBlockMemberRight` and `SuperMember` and ends with three "Deadly Diamonds of Death." That is the ambiguity when class D inherits from B and C, which both inherit from A.

He tries to turn `User` into an interface and use composition over inheritance, but under deadline stress he can't deliver Super members. Nancy drops the feature for now (p. 24). The lesson Theo draws: **in OOP, prefer composition over class inheritance** (p. 24).

![Class diagram: Member and UserWithBookItemRight both extend User, and VIPMember extends both Member and UserWithBookItemRight, while Librarian uses Member](../figures/01-16.png)

*Figure 1.16 (p. 22): `VIPMember` reaches `User` along two paths — a diamond from multiple inheritance.*

![The diagram after Super members: VIPMember, SuperMember and Librarian on top, two right classes UserWithBookItemRight and UserWithBlockMemberRight, Member below them, and User at the bottom reached along several paths](../figures/01-17.png)

*Figure 1.17 (p. 23): adding Super members brings the count of diamonds to three.*

> **Try it:** [The tiny feature](../widgets/01-class-hierarchy.html) — add VIP and Super members to Theo's hierarchy, see where the methods have to move and count the diamonds, then compare with the same rights kept as functions over data.

## Trade-offs at a glance

| OOP trait (table 1.1) | What it costs | What the book proposes (previewed) |
|---|---|---|
| Code and data mixed in classes | Entities with many relations; one tangled diagram | Two independent subsystems, code and data (ch. 2) |
| Mutable objects | Code you must re-think when reading; locks, performance hits, deadlocks | Immutable values for all data (ch. 3–5) |
| Data locked in members | A class per JSON shape; reflection or verbosity | Generic data access (ch. 3, 11) |
| Code locked in classes | Brittle hierarchies, diamonds under late requirements | Code as functions that are not tied to a class (ch. 2, 13) |
| Design patterns | Mitigate complexity "to some degree" (p. 25) | Not ruled out: DOP is compatible with OOP (p. 13) |

## Beyond the book

- **"Out of the Tar Pit."** Moseley and Marks's paper splits complexity into *essential* complexity, inherent in the problem, and *accidental* complexity, which comes from how we solve it. They name mutable state as a primary cause of the accidental kind. The book borrows the paper's definition of complexity as being hard to understand (p. 13); the essential/accidental split is the paper's, not this chapter's.
- **Composition over inheritance** is the advice of the "Gang of Four" *Design Patterns* book (1994), whose introduction says to favour object composition over class inheritance. Theo reaches it too late (p. 24).
- **The diamond problem** is handled differently by different languages. C++ has virtual inheritance; Java allows a class to extend only one class but implement many interfaces; Python linearizes base classes with its method resolution order (MRO). The book's point is that a model built only from classes forces this question at all.
- **The same features without a hierarchy.** Chapter 2 (pp. 39–41) adds Super and VIP members by adding `isSuperMember` and `isVIPMember` checks to stateless functions, with no design change. The widget's comparison mode follows that; the per-step counts it shows are the vault's tally, not the book's.

## Connections

- **Next:** [2. Separation between code and data](02-separation-between-code-and-data.md) applies the split from 1.2.1 to the Klafim system.
- **Mutable data and unpredictable code** return in [4. State management](04-state-management.md) and [5. Basic concurrency control](05-basic-concurrency-control.md).
- **Generic data access and JSON** return in [3. Basic data manipulation](03-basic-data-manipulation.md) and [11. Web services](11-web-services.md).
- **Code locked in classes** returns as polymorphism without objects in [13. Polymorphism](13-polymorphism.md).

## Check yourself

1. What does "complexity" mean in this book, and where does the definition come from?
   <details><summary>Answer</summary>Hard to understand, as defined in "Out of the Tar Pit" by Moseley and Marks (2006). It has nothing to do with the resources a program consumes, and it is relative rather than absolute (p. 13).</details>
2. Name the four aspects of OOP that the book blames for complexity, and the impact of each.
   <details><summary>Answer</summary>Code and data mixed (many relations); objects mutable (extra thinking when reading, explicit synchronization with threads); data locked in objects (non-trivial serialization); code locked in classes (complex hierarchies). Table 1.1, p. 14.</details>
3. How many relations does `Member` take part in, and what happens when you split it into `MemberCode` and `MemberData`?
   <details><summary>Answer</summary>Five: two data relations (`Library` has many `Member`s; `Member` has many `BookLending`s) and three code relations (extends `User`; used by `Librarian`; uses `BookItem`). The split leaves two relations on the data entity and three on the code entity, in two independent parts (pp. 15–16).</details>
4. Why can listing 1.2 print `true` and then `false`, when listing 1.1 can't?
   <details><summary>Answer</summary>Listing 1.1 reads a primitive value copied into a local variable. Listing 1.2 reads a member of a mutable object twice; another thread, or asynchronous code in JavaScript, can change it between the two reads (p. 17).</details>
5. Why couldn't Theo simply reuse `Librarian::addBookItem` for VIP members?
   <details><summary>Answer</summary>The code is locked in the `Librarian` class. `VIPMember` can't derive from `Librarian`, since VIP members must not block members or list lendings, so Theo had to move the method into a new base class, which created a diamond (pp. 21–23).</details>
6. What does OOP serialization to JSON usually rely on, according to the book?
   <details><summary>Answer</summary>Either reflection, which is complex, or verbose code: a query class and a result class per endpoint, because data has a rigid class-defined shape (p. 20).</details>
