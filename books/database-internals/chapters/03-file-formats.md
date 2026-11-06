---
book: database-internals
chapter: 3
title: "File Formats"
pages: "45–60"
---

# 3. File Formats

[← 2. B-Tree Basics](02-b-tree-basics.md) · [Book](../README.md) · [4. Implementing B-Trees →](04-implementing-b-trees.md)

## Summary

Memory access is mostly transparent to a developer, thanks to virtual memory. A disk, by contrast, is accessed with system calls: you name an offset in a file and translate the bytes you get back into an in-memory form (p. 45). This chapter covers the general principles for designing on-disk structures, not only B-Trees. The book's framing is to treat an on-disk B-Tree as a **page management mechanism**, where algorithms compose and navigate pages (p. 45).

It builds up from the bottom:

- **Primitive types** and byte order, then **strings** and variable-size data, then **bit-packed** booleans, enums and flags (pp. 47–50).
- **General principles:** fixed-size pages plus a file header and trailer, fixed fields placed before variable fields (pp. 50–51).
- **Slotted pages:** a pointer array grows from one end of the page and cells from the other. Records can be inserted in any order, keys stay sorted by reordering pointers, and records are referenced by slot ID (pp. 52–57).
- **Free-space management:** an availability list with first-fit or best-fit placement, then defragmentation, then overflow pages (pp. 57–58).
- **Versioning** of file formats and **checksumming** pages to catch corruption (pp. 58–59).

## Key takeaways

- **On disk, you manage fragmentation and garbage collection yourself.** There is no `malloc` or `free`, only `read` and `write` (pp. 46–47).
- **Byte order must match on encode and decode.** Big-endian puts the most significant byte first; little-endian puts the least significant first (p. 47).
- **Length-prefixed (Pascal) strings beat null-terminated ones.** The length is known in constant time, and the bytes can be sliced directly (p. 49).
- **Flags are bit masks with power-of-two values.** Set a flag with `|`, clear it with `& ~`, test it with `& … != 0` (p. 50).
- **Group fixed-size fields first.** They then have static offsets, and only variable-size fields need offset calculations (pp. 51, 54).
- **Slotted pages solve three problems at once:** minimal overhead (just the pointer array), space reclamation (defragmenting the page) and a dynamic layout (cells are referenced by ID from outside the page) (p. 54).
- **Checksum per page, not per file.** If one page is corrupt, only that page has to be discarded. CRCs detect burst errors, but noncryptographic hashes are not a tamper check (p. 59).

## Section outline

*From the book’s own table of contents (PDF bookmarks); printed page numbers.*

- Motivation — p. 46
- Binary Encoding — p. 47
  - Primitive Types — p. 47
  - Strings and Variable-Size Data — p. 49
  - Bit-Packed Data: Booleans, Enums, and Flags — p. 49
- General Principles — p. 50
- Page Structure — p. 52
- Slotted Pages — p. 52
- Cell Layout — p. 54
- Combining Cells into Slotted Pages — p. 56
- Managing Variable-Size Data — p. 57
- Versioning — p. 58
- Checksumming — p. 59
- Summary — p. 60

## Notes

Splits and merges are necessary to implement B-Trees but not enough, because pointer management on disk works differently than in memory (p. 45). Most of a B-Tree's complexity comes from mutability, so this chapter and the next focus on page layouts, splits and relocations. The LSM chapter instead focuses on sorting and maintenance (p. 46).

### Motivation

Designing a file format is like working with data structures in a language without managed memory: you allocate a block and slice it into fixed-size primitives and structures, and you use pointers for larger or variable-size pieces (p. 46). Unlike memory, though, the disk gives you no free allocation, so you have to deal with fragmentation and garbage collection yourself. Layout matters far more on disk than in memory, where special layouts are mostly a CPU-cache optimization (p. 46).

### Binary encoding

Data must be encoded compactly and be easy to serialize and deserialize (p. 47). The same principles apply to file formats, serialization formats and network protocols.

#### Primitive types

Most numbers are fixed-size. The **endianness** of a multibyte value must match on write and read (p. 47):

| Byte order | First byte | `0xAABBCCDD` in memory, lowest address first |
|---|---|---|
| **Big-endian** | Most significant byte (MSB) | `AA BB CC DD` |
| **Little-endian** | Least significant byte (LSB) | `DD CC BB AA` |

*The memory column restates Figure 3-1 (p. 47).*

RocksDB detects the platform's byte order. If it doesn't match the value's order, it reverses the bytes (`EncodeFixed64WithEndian`, `EndianTransform`) (p. 48).

| Type | Size (p. 48) |
|---|---|
| `byte` | 8 bits |
| `short` | 2 bytes |
| `int` | 4 bytes |
| `long` | 8 bytes |
| `float` (IEEE 754 single precision) | 32 bits: 23 fraction bits, 8 exponent bits, 1 sign bit |
| `double` | Double precision |

Floating-point values are approximations. Figure 3-2 encodes 0.15652 (p. 48).

#### Strings and variable-size data

Complex values are composed like a C `struct`, out of primitives, fixed-size arrays and pointers. Compilers may add architecture-dependent padding, which breaks assumptions about offsets (p. 49, note 2). Variable-size data is a length followed by that many bytes, as in a **Pascal (UCSD) string** (p. 49):

```text
String
{
    size    uint_16
    data    byte[size]
}
```

Compared with **null-terminated strings**, the length is known in constant time, and a string can be built by slicing `size` bytes (p. 49).

#### Bit-packed data: booleans, enums and flags

- **Booleans:** a whole byte per boolean is wasteful, so they're often packed eight per byte. A 1 bit is *set*; a 0 bit is *unset* (p. 49).
- **Enums:** low-cardinality, often-repeated values encoded as integers, such as a node type `ROOT = 0x00`, `INTERNAL = 0x01`, `LEAF = 0x02` (p. 49).
- **Flags:** non-mutually-exclusive named booleans, for example "is leaf", "variable-size values", "has overflow pages". Each mask is a power of two, so it has a single set bit (p. 50).

| Operation | Expression (p. 50) |
|---|---|
| Set | `flags \|= MASK` or `flags \|= (1 << n)` |
| Unset | `flags &= ~MASK` |
| Test | `(flags & MASK) != 0` |

### General principles

The first decision is how to do **addressing**: whether to split the file into same-sized pages, each one block or several contiguous blocks (p. 50). In-place update structures mostly use fixed-size pages because that simplifies access. Append-only structures often write page-wise too, flushing a page once it fills up in memory (p. 50). A file usually has a fixed-size **header**, optionally a fixed-size **trailer** for metadata needed for fast access or decoding, and pages in between (Figure 3-3, pp. 50–51).

With a **fixed schema**, fields are identified by position rather than by name (p. 51). The book's employee-directory example puts fixed-size fields first, followed by the variable-size ones:

```text
Fixed-size:    employee_id (4) | tax_number (4) | date (3) | gender (1)
               | first_name_length (2) | last_name_length (2)
Variable-size: first_name (first_name_length) | last_name (last_name_length)
```

Reading `last_name` this way means adding up the sizes of the variable fields before it. Storing an **offset and length** for each variable field in the fixed area makes every field directly addressable (p. 51). Formats are usually hierarchies: fields → cells → pages → sections → regions. A lookup table, kept in the header, the trailer or a separate file, points to where each part starts (p. 51).

### Page structure

Data and index files are divided into fixed-size **pages**, often several filesystem blocks each and usually 4–16 KB (p. 52). Leaves hold key/record pairs; nonleaf nodes hold keys and pointers. Bayer's original layout is a simple concatenation of triplets: key, value and child pointer (Figure 3-4) (p. 52). Its drawbacks (p. 52):

- inserting anywhere but on the right relocates elements;
- it works only for fixed-size records.

### Slotted pages

The core problem with variable-size records is **free-space management** (pp. 52–53):

- A record of size *n* reuses a gap of size *m* only if *m* = *n* or another record of size *m* − *n* exists.
- Fixed-size segments, say 64 bytes, waste `64 − (n mod 64)` bytes per record.
- Moving records to reclaim space must preserve the offsets that out-of-page pointers refer to.

The page format therefore has to store variable-size records with minimal overhead, reclaim deleted space and reference records regardless of their exact location (p. 53). The answer is the **slotted page**, also called a **slot directory**, used by PostgreSQL among others (p. 53). Pointers and cells live in two independent regions on opposite sides of the page:

- order is preserved by reorganizing only the pointers;
- a delete nullifies or removes a pointer;
- a fixed-size header holds page metadata (Figure 3-5).

| Requirement | How slotted pages meet it (p. 54) |
|---|---|
| Minimal overhead | Only the pointer array of cell offsets |
| Space reclamation | Defragment and rewrite the page |
| Dynamic layout | Outside the page, cells are referenced only by slot ID |

### Cell layout

Cells come in two kinds (p. 54):

- **Key cells** hold a separator key and a child page ID.
- **Key-value cells** hold a key and a data record.

All cells in a page are assumed to be uniform (all key cells or all key-value cells, all fixed-size or all variable-size), so cell metadata is stored once per page (p. 54).

A **key cell** needs a type (inferred from the page), a key size, a child page ID and the key bytes (p. 54):

```text
0                4               8
+----------------+---------------+-------------+
| [int] key_size | [int] page_id | [bytes] key |
+----------------+---------------+-------------+
```

A **key-value cell** has flags, a key size, a value size, the key bytes and the record bytes (p. 55):

```text
0              1                5                  9
+--------------+----------------+------------------+-------------+----------------------+
| [byte] flags | [int] key_size | [int] value_size | [bytes] key | [bytes] data_record  |
+--------------+----------------+------------------+-------------+----------------------+
```

*Both layouts are from p. 55; the book splits the second over two lines.*

Fixed fields come first, so their offsets are static. Cells store a **page ID**, not a file offset: the page cache translates IDs through a lookup table. Cell offsets are page-local, so smaller integers are enough (p. 55).

**Variable-size data** (p. 55): to read the key, skip the header and read `key_size` bytes. To read the value, skip the header plus `key_size` bytes and read `value_size` bytes. Storing a total size and deriving the value size works too. The point is to have enough information to slice the cell.

### Combining cells into slotted pages

Cells are appended toward the end of the page and offsets are kept at the start, so the two grow toward each other (Figure 3-6) (p. 56). Keys can arrive in any order. Logical order is kept by **sorting the offsets**, which enables binary search, and cells never move on insert, update or delete (p. 56).

The book's example (Figures 3-7 and 3-8, pp. 56–57):

| Step | Cells, physical (insertion) order | Offsets, logical order |
|---|---|---|
| Insert Tom, Leslie | Tom, Leslie | Leslie, Tom |
| Insert Ron | Tom, Leslie, Ron | Leslie, **Ron**, Tom: pointers after the insertion point shift right |

> **Try it:** [Slotted page](../widgets/03-slotted-page.html) — insert and delete variable-size records, watch offsets stay sorted while cells stay in insertion order, and compare first fit and best fit before forcing a defragmentation.

### Managing variable-size data

A delete doesn't have to shift the remaining cells. The cell is marked deleted, and an in-memory **availability list** records the offset and size of the freed segment. Inserts check this list first (Figure 3-9) (p. 57). SQLite calls the free segments **freeblocks**: it keeps a pointer to the first one in the page header, plus the total number of free bytes, so it can tell quickly whether a cell would fit after defragmentation (p. 57).

| Fit strategy | Behaviour (pp. 57–58) |
|---|---|
| **First fit** | Uses the first suitable segment. The remainder may be too small for any cell and is effectively wasted |
| **Best fit** | Picks the segment that leaves the smallest remainder |

If no contiguous space is big enough but the fragmented space is, the page is **defragmented**: live cells are read and rewritten. If even that isn't enough, an **overflow page** is created (Ch. 4, p. 65) (p. 58). Some engines store leaf keys and values separately to improve key locality during search, at the cost of an extra value-cell pointer for variable-size keys (p. 58).

The simplified model for the rest of the book: one node per page, made of a fixed header, a cell pointer block and cells. Page IDs locate child nodes in the file, and cell offsets locate cells within a page (p. 58).

### Versioning

Storage engines usually have to read more than one format version, so the version has to be discoverable (pp. 58–59):

| Where | Example |
|---|---|
| Filename prefix | Cassandra 4.0 writes `na-1-big-Data.db`; 3.0 files use the `ma` prefix |
| Separate file | PostgreSQL's `PG_VERSION` |
| File header | Part of the header uses a format that never changes; a version-specific reader then takes over. Magic numbers (Ch. 4, p. 62) |

### Checksumming

Bugs and hardware failures corrupt files. **Checksums** and **CRCs** detect corruption before it spreads to other subsystems or nodes (p. 59).

| Mechanism | Detects (p. 59) |
|---|---|
| Checksum (XOR with parity, summation) | Weakest; can't detect multibit corruption |
| CRC (lookup tables, polynomial division) | Burst errors, i.e. consecutive corrupted bits, common on networks and storage |
| Cryptographic hash | Tampering; CRCs and noncryptographic hashes are not designed for this |

On write, compute the checksum and store it with the data. On read, recompute and compare, and never use mismatching data (p. 59). Checksums are usually stored per page in the **page header**: whole-file checksums are impractical because files are rarely read in full, and a corrupt page doesn't invalidate the whole file (p. 59).

### Summary

The chapter covered serializing primitives, composing cells, building slotted pages and handling variable-size data. The same principles work for on-disk structures and for network protocols (p. 60).

## Trade-offs at a glance

| Layout | Pros | Cons |
|---|---|---|
| Fixed-size triplets (Bayer) | Simple | Fixed-size records only; inserts relocate elements |
| Fixed-size segments | Simple space management | Waste up to a segment per record |
| Slotted page | Variable-size records; stable slot IDs; no cell movement | Pointer array overhead; fragmentation needs an availability list and defragmentation |

| | First fit | Best fit |
|---|---|---|
| Search | Stops at the first match | Scans all free segments |
| Waste | Can leave unusable remainders | Smallest remainder |

## Beyond the book

- **Endianness in practice.** x86-64 and most ARM configurations are little-endian; network protocols traditionally use big-endian ("network byte order"). Python's `struct` module makes the choice explicit with `<` and `>`.
- **PostgreSQL's page layout** matches the book's model closely. A 24-byte page header is followed by an array of 4-byte *line pointers* growing forward, while tuples grow backward from the end of the page. An index entry addresses a row by page number and line-pointer index (a TID), so tuples can move within a page without changing any index.
- **CRC32C** (Castagnoli) is the checksum used by many storage systems, including RocksDB and ext4 metadata. Modern CPUs compute it in hardware.

## Connections

- **Related chapters:** [2. B-Tree Basics](02-b-tree-basics.md) (nodes = pages), [4. Implementing B-Trees](04-implementing-b-trees.md) (page headers, magic numbers, overflow pages, binary search over offsets), [5. Transaction Processing and Recovery](05-transaction-processing-and-recovery.md) (the page cache), [7. Log-Structured Storage](07-log-structured-storage.md) (SSTable layouts).

## Check yourself

*Questions and answers are the vault's, written from the notes above; answers cite the book's pages.*

1. **How is the 32-bit value `0xAABBCCDD` laid out in little-endian order?**
   - [ ] `AA BB CC DD`
   - [x] `DD CC BB AA`
   - [ ] `BB AA DD CC`

   *Answer:* Little-endian starts with the least significant byte (p. 47).

2. **Why prefer Pascal strings to null-terminated strings in a file format?**

   *Answer:* The length is available in constant time without scanning, and the string can be built by slicing `size` bytes (p. 49).

3. **How do you test whether the flag `HAS_OVERFLOW_PAGES` is set?**

   *Answer:* `(flags & HAS_OVERFLOW_PAGES) != 0`. Masks are powers of two, so each has a single set bit (p. 50).

4. **In a slotted page, what moves when a key is inserted between two existing keys?**
   - [ ] The cells after the insertion point
   - [x] Only the offset pointers after the insertion point
   - [ ] Nothing; the page is re-sorted on read

   *Answer:* Cells are appended in insertion order. The offset array is kept sorted, so pointers after the insertion point shift (pp. 56–57).

5. **What happens when a new cell doesn't fit in any free segment but the page has enough free bytes in total?**

   *Answer:* The page is defragmented: live cells are read and rewritten to reclaim the space. If there still isn't enough room, an overflow page is created (p. 58).

6. **Why are checksums stored per page rather than per file?**

   *Answer:* Files are rarely read in full, so per-file checksums are impractical. Per-page checksums are more robust, and a single corrupt page doesn't invalidate the whole file (p. 59).
