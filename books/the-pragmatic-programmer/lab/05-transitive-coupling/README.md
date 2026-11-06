# Transitive coupling

If A is coupled to B and C, and they are coupled to others, A is coupled to all of them. How fast does that spread? The script builds 200 random layered dependency graphs per row: 6 layers of 20 modules, where each module depends on a few modules in lower layers, usually the layer just below. It then counts how many modules each one reaches transitively, as the number of direct dependencies per module grows from 1 to 6.

*Illustrates The Pragmatic Programmer, Topic 28, Decoupling, pp. 228–229: coupling is transitive, and decoupled code is easier to change. The layered-graph model and its parameters are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 transitive_coupling.py
```

## Expected output

```text
200 random graphs per row: 6 layers x 20 modules = 120 modules

direct deps   top layer: coupled to   all modules: mean   share of lower modules
          1                     3.7                 2.1                       4%
          2                    23.2                 9.3                      23%
          3                    48.0                18.6                      48%
          4                    62.4                25.2                      62%
          6                    75.4                32.4                      75%

A top-layer module has at most 100 modules below it.
```

## What to look for

- With one direct dependency, a top-layer module is coupled to about 4 modules, roughly one per layer below it.
- Three direct dependencies already couple a top module to about half of everything below it; six reach three quarters.
- The growth is far faster than the number of direct dependencies, because every dependency brings its own dependencies along. That's why the book wants shy code that talks only to what it knows directly.

## Related

- Chapter note: [5. Bend, or Break](../../chapters/05-bend-or-break.md) — Topic 28, Decoupling, pp. 228–229
