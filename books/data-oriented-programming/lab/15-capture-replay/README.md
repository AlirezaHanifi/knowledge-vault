# Capture and replay

Dumps a function context, its arguments, to a JSON file named by context and UUID, then reads it back synchronously and replays the call. It runs the eight test queries against the three versions of the search, on the captured catalog. Last, it shows what an asynchronous dump records when the caller goes on and changes the data.

*Illustrates Data-Oriented Programming, chapter 15, pp. 314–328 (listings 15.5–15.26). Files are written to a temporary directory and removed. The UUIDs are seeded and the race is ordered with events, so the output is deterministic. The withdrawal of Watchmen is the vault's scenario.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 capture_replay.py
```

## Expected output

```text
1. Capture: console.log versus JSON.stringify (listings 15.5-15.6)
   console.log:    I like the word "reproducibility"
   JSON.stringify: "I like the word \"reproducibility\""
   pasting the console.log output back: fails (Expecting value)
   pasting the JSON output back: OK

2. Dump the context of searchBooksByTitle(catalog, 'Watch'), then replay it
   wrote test-data/searchBooksByTitle-85750621-02fb-4d4f-b57f-bc5af71a1bfc.json (990 bytes)
   original: [{"title": "Watchmen", "isbn": "978-1779501127", "authorNames": ["Alan Moore", "Dave Gibbons"]}]
   replayed: [{"title": "Watchmen", "isbn": "978-1779501127", "authorNames": ["Alan Moore", "Dave Gibbons"]}] | identical: True

3. The eight queries of listings 15.25-15.26 on the captured catalog
   query       expected 15.8 lowercase startsWith   15.12 word startsWith       15.24 lowercase \b regex
   "Habit"     book     FAIL none                   ok   found                  ok   found
   "habit"     book     FAIL none                   FAIL none                   ok   found
   "7 Habit"   book     ok   found                  FAIL none                   ok   found
   "habits of" book     FAIL none                   FAIL none                   ok   found
   "abit"      nothing  ok   none                   ok   none                   ok   none
   "bit"       nothing  ok   none                   ok   none                   ok   none
   "7 abit"    nothing  ok   none                   ok   none                   ok   none
   "habit of"  nothing  ok   none                   ok   none                   ok   none
   passing:            5 / 8                       5 / 8                       8 / 8

4. An asynchronous dump while the caller goes on and withdraws Watchmen
   mutable   data: the function saw 1 book(s); the replay finds 0 -> NOT reproduced
   immutable data: the function saw 1 book(s); the replay finds 1 -> reproduced
```

## What to look for

- `console.log` output loses the quotes and backslashes, so it can't be pasted back. JSON can.
- The file name includes the UUID; as printed, listing 15.15 never concatenates it (see the vault note in the lesson). The replayed result equals the original.
- Listing 15.8's lowercase `startsWith` and listing 15.12's word prefix each pass 5 of 8 queries, failing different ones. Listing 15.24's lowercase `\b` regular expression passes all 8.
- With mutable data, the asynchronous dump writes a catalog the function never saw, and the replay finds nothing. With immutable data, the caller makes a new version, and the dump records exactly what the function received (p. 326).

## Related

- Chapter note: [15. Debugging](../../chapters/15-debugging.md) — sections 15.2–15.4, pp. 314–328
