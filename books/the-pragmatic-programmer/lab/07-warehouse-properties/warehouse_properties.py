"""A tiny property-based tester (standard library only) run against the book's Warehouse.

Illustrates The Pragmatic Programmer, Topic 42, Property-Based Testing (pp. 378-383). The Warehouse,
order() and the stock-level property follow the book; the generator and shrinker are the vault's
(the book uses Hypothesis).
"""
import random


class Warehouse:
    def __init__(self, stock, fixed=False):
        self.stock = dict(stock)
        self.fixed = fixed

    def in_stock(self, item_name, quantity=1):
        if self.fixed:                                   # proptest/stock1.py
            return item_name in self.stock and self.stock[item_name] >= quantity
        return item_name in self.stock and self.stock[item_name] > 0   # proptest/stock.py

    def take_from_stock(self, item_name, quantity):
        if quantity <= self.stock[item_name]:
            self.stock[item_name] -= quantity
        else:
            raise Exception(f"Oversold {item_name}")

    def stock_count(self, item_name):
        return self.stock[item_name]


def order(warehouse, item, quantity):
    if warehouse.in_stock(item, quantity):
        warehouse.take_from_stock(item, quantity)
        return ("ok", item, quantity)
    return ("not available", item, quantity)


STOCK = {"shoes": 10, "hats": 2, "umbrellas": 0}


def unit_tests(fixed):
    wh = Warehouse(STOCK, fixed)
    assert order(wh, "hats", 1)[0] == "ok" and wh.stock_count("hats") == 1
    assert order(Warehouse(STOCK, fixed), "umbrellas", 1)[0] == "not available"
    assert order(Warehouse(STOCK, fixed), "bagel", 1)[0] == "not available"
    return "pass"


def prop(fixed, item, quantity):
    """Stock taken plus stock left equals the original stock. Returns None or a failure message."""
    wh = Warehouse(STOCK, fixed)
    initial = wh.stock_count(item)
    try:
        status, item, quantity = order(wh, item, quantity)
    except Exception as e:  # noqa: BLE001 - any exception falsifies the property
        return f"{type(e).__name__}: {e}"
    if status == "ok" and wh.stock_count(item) + quantity != initial:
        return "stock level changed"
    return None


ITEMS = ["shoes", "hats"]        # some.sampled_from(["shoes", "hats"])


def shrink(fixed, item, quantity):
    """Greedy shrink: prefer the first item, then smaller quantities, while the property still fails."""
    steps = 0
    improved = True
    while improved:
        improved = False
        candidates = ([(ITEMS[0], quantity)] if item != ITEMS[0] else []) + [(item, q) for q in range(1, quantity)]
        for it, q in candidates:
            steps += 1
            if prop(fixed, it, q):
                item, quantity, improved = it, q, True
                break
    return item, quantity, steps


def check(fixed, qmax, runs=100, seed=0):
    rng = random.Random(seed)
    for n in range(1, runs + 1):
        item, q = rng.choice(ITEMS), rng.randint(1, qmax)
        msg = prop(fixed, item, q)
        if msg:
            s_item, s_q, steps = shrink(fixed, item, q)
            return f"FAIL after {n:>3} case(s): {item}, {q} -> shrunk to {s_item}, {s_q} in {steps} step(s): {prop(fixed, s_item, s_q)}"
    return f"pass ({runs} cases)"


def main():
    for fixed in (False, True):
        name = "fixed in_stock(item, qty)" if fixed else "buggy in_stock(item)"
        print(f"== {name}")
        print(f"   hand-written unit tests: {unit_tests(fixed)}")
        for qmax in (4, 20):
            for seed in (1, 2, 3):
                print(f"   quantity 1-{qmax:<2} seed {seed}: {check(fixed, qmax, seed=seed)}")
        print()


if __name__ == "__main__":
    main()
