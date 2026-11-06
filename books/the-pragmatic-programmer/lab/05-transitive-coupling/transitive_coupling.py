"""Transitive coupling in random layered dependency graphs.

Illustrates The Pragmatic Programmer, Topic 28, Decoupling (pp. 228-229): coupling is transitive.
The graph model is the vault's.
"""
import random

LAYERS = 6
PER_LAYER = 20
GRAPHS = 200


def graph(deps: int, rng: random.Random) -> dict[int, list[int]]:
    """Modules in layer L depend on `deps` random modules in lower layers (more likely the next one down)."""
    g = {}
    for layer in range(LAYERS):
        for j in range(PER_LAYER):
            m = layer * PER_LAYER + j
            g[m] = []
            if layer == 0:
                continue
            for _ in range(deps):
                below = layer - 1 if rng.random() < 0.7 else rng.randrange(layer)
                g[m].append(below * PER_LAYER + rng.randrange(PER_LAYER))
    return g


def reach(g: dict[int, list[int]], m: int) -> int:
    seen, stack = set(), list(g[m])
    while stack:
        x = stack.pop()
        if x not in seen:
            seen.add(x)
            stack.extend(g[x])
    return len(seen)


def main() -> None:
    rng = random.Random(28)
    n = LAYERS * PER_LAYER
    print(f"{GRAPHS} random graphs per row: {LAYERS} layers x {PER_LAYER} modules = {n} modules\n")
    print(f"{'direct deps':>11}  {'top layer: coupled to':>22}  {'all modules: mean':>18}  {'share of lower modules':>23}")
    for deps in (1, 2, 3, 4, 6):
        top = allm = 0.0
        for _ in range(GRAPHS):
            g = graph(deps, rng)
            tops = [reach(g, m) for m in range((LAYERS - 1) * PER_LAYER, n)]
            top += sum(tops) / len(tops)
            allm += sum(reach(g, m) for m in g) / n
        top /= GRAPHS
        allm /= GRAPHS
        lower = (LAYERS - 1) * PER_LAYER
        print(f"{deps:>11}  {top:>22.1f}  {allm:>18.1f}  {top / lower:>23.0%}")
    print("\nA top-layer module has at most", (LAYERS - 1) * PER_LAYER, "modules below it.")


if __name__ == "__main__":
    main()
