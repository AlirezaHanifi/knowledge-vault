# Tail latency amplification

Simulates a backend whose calls are occasionally slow, then pages that fan out to *k* parallel calls. Shows that page latency is governed by the slowest call (tail latency amplification, Figure 2-6) and that averaging per-server percentiles gives a meaningless number, while merging the distributions gives the real one.

*Illustrates DDIA 2nd ed., “Use of Response Time Metrics”, pp. 41–43. The implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 tail_latency.py
```

## Expected output

```text
1. One backend service (ms)
   mean    26.2  p50    20.1  p95    33.9  p99   329.3  p99.9   795.9

2. A page that fans out to k parallel backend calls is as slow as the slowest call
      k   page p50   page p99  slow pages  1-(1-p)^k
      1       20.1       49.3        0.9%       1.0%
      5       28.5      621.3        4.5%       4.9%
     10       32.2      766.1        9.1%       9.6%
     25       37.6     1002.7       20.6%      22.2%
     50       44.8     1069.9       37.9%      39.5%
    100      390.7     1227.9       61.6%      63.4%

3. Averaging percentiles across servers is meaningless; merge the data instead
   average of the ten per-server p99s:   114.5 ms
   p99 of the merged distribution:       352.9 ms
```

## What to look for

- The backend p99 (~330 ms) is 16× its median; the mean (~26 ms) hides this entirely.
- At *k* = 100, the *median* page already contains a slow call — the backend’s p99 has become the user’s p50.
- The measured share of slow pages tracks the analytic 1 − (1 − p)<sup>k</sup>.
- One unhealthy server out of ten: the average of p99s (≈115 ms) understates the fleet’s true p99 (≈350 ms) by 3×.

## Related

- Chapter note: [2. Defining Nonfunctional Requirements](../../chapters/02-defining-nonfunctional-requirements.md) — “Use of Response Time Metrics”, pp. 41–43
- Explore in the browser: [Percentiles and tail latency](../../widgets/02-tail-latency.html)
