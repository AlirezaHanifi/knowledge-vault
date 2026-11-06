"""At-most-once, at-least-once, and at-least-once with an idempotence key.

Illustrates Think Distributed Systems, Chapter 4, "Message delivery semantics",
"Exactly-once processing semantics" and "Idempotence" (pp. 57-63). The network's
loss and duplication rates and the retry limit are the vault's (seeded).
"""
import random
import uuid
from collections import Counter

ORDERS = 10_000
P_LOSE_REQUEST = 0.15
P_LOSE_RESPONSE = 0.15
P_DUPLICATE = 0.05  # the network delivers a request twice
MAX_ATTEMPTS = 20


class PaymentService:
    def __init__(self, dedupe):
        self.dedupe = dedupe
        self.charges = Counter()
        self.seen = set()

    def charge(self, order, key):
        if self.dedupe:
            if key in self.seen:      # retry of a request already processed
                return "ok"
            self.seen.add(key)        # recorded together with the side effect
        self.charges[order] += 1
        return "ok"


def send(rng, service, order, key):
    """One attempt: True if the sender sees a response."""
    if rng.random() < P_LOSE_REQUEST:
        return False
    service.charge(order, key)
    if rng.random() < P_DUPLICATE:
        service.charge(order, key)
    return rng.random() >= P_LOSE_RESPONSE


def run(mode, seed):
    rng = random.Random(seed)
    uid = random.Random(seed + 1)
    service = PaymentService(dedupe=(mode == "at-least-once + key"))
    for order in range(ORDERS):
        key = uuid.UUID(int=uid.getrandbits(128))  # one key for the request and all its retries
        attempts = 1 if mode == "at-most-once" else MAX_ATTEMPTS
        for _ in range(attempts):
            if send(rng, service, order, key):
                break
    dist = Counter(service.charges[o] for o in range(ORDERS))
    return dist


def main():
    print(f"{ORDERS:,} orders; request lost {P_LOSE_REQUEST:.0%}, response lost {P_LOSE_RESPONSE:.0%}, "
          f"request duplicated {P_DUPLICATE:.0%}\n")
    print(f"{'mode':<22} {'charged 0x':>11} {'exactly 1x':>11} {'2x or more':>11} {'max':>4}")
    for i, mode in enumerate(["at-most-once", "at-least-once", "at-least-once + key"]):
        d = run(mode, seed=7 + i)
        many = sum(v for k, v in d.items() if k >= 2)
        print(f"{mode:<22} {d[0] / ORDERS:>11.2%} {d[1] / ORDERS:>11.2%} {many / ORDERS:>11.2%} {max(d):>4}")


if __name__ == "__main__":
    main()
