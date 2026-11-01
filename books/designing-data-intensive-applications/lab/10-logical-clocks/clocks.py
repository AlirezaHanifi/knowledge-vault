"""Physical timestamps vs Lamport clocks vs hybrid logical clocks (HLC).

Three nodes with skewed time-of-day clocks exchange chat messages. A reply is
causally after the message it answers, so its timestamp must be greater.
Physical timestamps break this when the replier's clock is behind; Lamport
clocks and HLCs never do, and HLC timestamps stay close to physical time.

Illustrates DDIA 2nd ed., Chapter 10, "Logical Clocks" (pp. 420-423). The HLC
here follows the algorithm of Kulkarni et al. (the book's reference [57]);
the code is the vault's own.
"""

from __future__ import annotations

import random

SKEW_MS = {"Aaliyah": +40, "Bryce": -35, "Caleb": 0}   # clock error relative to true time


class Node:
    def __init__(self, name: str):
        self.name = name
        self.lamport = 0
        self.hlc = (0, 0)                               # (physical part l, counter c)

    def physical(self, true_ms: int) -> int:
        return true_ms + SKEW_MS[self.name]

    def tick_lamport(self, received: int | None = None) -> tuple[int, str]:
        self.lamport = max(self.lamport, received or 0) + 1
        return (self.lamport, self.name)              # node name breaks ties -> total order

    def tick_hlc(self, true_ms: int, received: tuple[int, int] | None = None) -> tuple[int, int, str]:
        pt = self.physical(true_ms)
        l, c = self.hlc
        if received is None:
            new_l = max(l, pt)
            new_c = c + 1 if new_l == l else 0
        else:
            rl, rc = received
            new_l = max(l, rl, pt)
            if new_l == l == rl:
                new_c = max(c, rc) + 1
            elif new_l == l:
                new_c = c + 1
            elif new_l == rl:
                new_c = rc + 1
            else:
                new_c = 0
        self.hlc = (new_l, new_c)
        return (new_l, new_c, self.name)


def main() -> None:
    rng = random.Random(3)
    nodes = {n: Node(n) for n in SKEW_MS}
    names = list(nodes)
    events = []                                       # (kind, true time, stamps, parent index)
    true_ms = 1_000
    for i in range(300):
        true_ms += rng.randint(1, 30)
        sender = nodes[rng.choice(names)]
        parent = None
        if events and rng.random() < 0.6:             # a reply to a recent message
            parent = rng.randrange(max(0, len(events) - 5), len(events))
        recv = events[parent][2] if parent is not None else None
        stamps = {
            "physical": (sender.physical(true_ms), sender.name),
            "lamport": sender.tick_lamport(recv["lamport"][0] if recv else None),
            "hlc": sender.tick_hlc(true_ms, recv["hlc"][:2] if recv else None),
        }
        events.append((sender.name, true_ms, stamps, parent))

    replies = [(i, p) for i, (_, _, _, p) in enumerate(events) if p is not None]
    print(f"{len(events)} messages, {len(replies)} of them replies; clock skew {SKEW_MS}\n")
    print(f"{'timestamp scheme':<18}{'replies ordered before their parent':>38}{'max |ts - true time|':>24}")
    for scheme in ("physical", "lamport", "hlc"):
        bad = sum(events[i][2][scheme] <= events[p][2][scheme] for i, p in replies)
        if scheme == "lamport":
            drift = "n/a (a counter)"
        else:
            drift = f"{max(abs(e[2][scheme][0] - e[1]) for e in events)} ms"
        print(f"{scheme:<18}{bad:>38}{drift:>24}")

    i, p = next((i, p) for i, p in replies if events[i][2]["physical"] <= events[p][2]["physical"])
    print("\nExample violation with physical clocks:")
    for label, idx in (("message", p), ("reply", i)):
        name, t, s, _ = events[idx]
        print(f"  {label:<7} by {name:<8} true time {t}  physical {s['physical'][0]}  "
              f"lamport {s['lamport'][0]}  hlc {s['hlc'][0]}.{s['hlc'][1]}")


if __name__ == "__main__":
    main()
