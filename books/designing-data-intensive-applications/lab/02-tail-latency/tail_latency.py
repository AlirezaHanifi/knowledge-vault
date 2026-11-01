"""Tail latency amplification and why percentiles must not be averaged.

Illustrates DDIA 2nd ed., Chapter 2, "Use of Response Time Metrics" (pp. 41-43).
The latency model is illustrative, not data from the book.
"""

import random

SEED = 42
REQUESTS = 100_000


def backend_latency(rng: random.Random) -> float:
    """One backend call: usually ~20 ms, 1% of the time a slow event adds ~300+ ms."""
    t = rng.lognormvariate(3.0, 0.3)          # median e^3 ~ 20 ms
    if rng.random() < 0.01:
        t += 300 + rng.expovariate(1 / 200)
    return t


def percentile(sorted_values: list[float], p: float) -> float:
    i = max(0, min(len(sorted_values) - 1, int(p * len(sorted_values) + 0.999999) - 1))
    return sorted_values[i]


def summary(values: list[float]) -> str:
    s = sorted(values)
    mean = sum(s) / len(s)
    return (f"mean {mean:7.1f}  p50 {percentile(s, .5):7.1f}  p95 {percentile(s, .95):7.1f}  "
            f"p99 {percentile(s, .99):7.1f}  p99.9 {percentile(s, .999):7.1f}")


def main() -> None:
    rng = random.Random(SEED)

    print("1. One backend service (ms)")
    calls = [backend_latency(rng) for _ in range(REQUESTS)]
    print("   " + summary(calls))
    slow_threshold = percentile(sorted(calls), 0.99)

    print("\n2. A page that fans out to k parallel backend calls is as slow as the slowest call")
    print(f"   {'k':>4}  {'page p50':>9}  {'page p99':>9}  {'slow pages':>10}  {'1-(1-p)^k':>9}")
    for k in (1, 5, 10, 25, 50, 100):
        pages = [max(backend_latency(rng) for _ in range(k)) for _ in range(REQUESTS // 10)]
        s = sorted(pages)
        slow = sum(1 for t in pages if t > slow_threshold) / len(pages)
        print(f"   {k:>4}  {percentile(s, .5):9.1f}  {percentile(s, .99):9.1f}  {slow:10.1%}  {1 - 0.99 ** k:9.1%}")

    print("\n3. Averaging percentiles across servers is meaningless; merge the data instead")
    # Ten servers, one of which is having a bad time (10x more slow events).
    servers = []
    for i in range(10):
        local = random.Random(SEED + i)
        bad = i == 0
        samples = []
        for _ in range(10_000):
            t = local.lognormvariate(3.0, 0.3)
            if local.random() < (0.10 if bad else 0.002):
                t += 300 + local.expovariate(1 / 200)
            samples.append(t)
        servers.append(sorted(samples))
    avg_p99 = sum(percentile(s, .99) for s in servers) / len(servers)
    merged = sorted(t for s in servers for t in s)
    print(f"   average of the ten per-server p99s: {avg_p99:7.1f} ms")
    print(f"   p99 of the merged distribution:     {percentile(merged, .99):7.1f} ms")


if __name__ == "__main__":
    main()
