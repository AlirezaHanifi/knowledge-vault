# Retry strategies vs. failure classes

Which retry strategy fits which kind of failure? This experiment runs 10,000 attempts at a step against three failure models that follow the book's temporal classes. A **transient** failure fails each attempt independently (30%). An **intermittent** one lingers: an outage lasts a random time, about 6 s on average. A **permanent** one never goes away by itself. Each failure meets four strategies: no retry, five immediate retries, eight retries 1 s apart, and capped exponential backoff with jitter. A step gives up after 30 s.

*Illustrates Think Distributed Systems, “Failure classification” and “Failure mitigation”, pp. 47–53: transient failures suit immediate retries, intermittent ones retries with backoff, and permanent ones need repair. The failure probabilities, outage length, strategy parameters and implementation are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 retry_strategies.py
```

## Expected output

```text
10,000 trials per cell; a step gives up after 30 s of retrying

failure       strategy        success  attempts  time to success
transient     no retry          70.5%      1.00           0.00 s
transient     immediate x5      99.8%      1.43           0.00 s
transient     fixed 1 s x8     100.0%      1.43           0.43 s
transient     exp. backoff     100.0%      1.42           0.34 s

intermittent  no retry           0.0%      1.00                —
intermittent  immediate x5       0.7%      4.99           0.03 s
intermittent  fixed 1 s x8      68.1%      5.52           3.36 s
intermittent  exp. backoff      98.8%      4.98           7.86 s

permanent     no retry           0.0%      1.00                —
permanent     immediate x5       0.0%      5.00                —
permanent     fixed 1 s x8       0.0%      8.00                —
permanent     exp. backoff       0.0%     10.14                —
```

## What to look for

- Against **transient** failures, any retry works and immediate retries are fastest: backoff only adds waiting.
- Against **intermittent** failures, immediate retries are used up while the outage lasts (under 1% success). Spreading attempts over time with backoff succeeds about 99% of the time, at the price of several seconds' delay.
- Against **permanent** failures, no strategy succeeds. Retrying only burns attempts, which is why the book's escalation ends with suspend and repair, or compensation.
- The strategies' attempt counts are similar against intermittent failures; what differs is *when* the attempts happen.

## Related

- Chapter note: [3. Failure tolerance](../../chapters/03-failure-tolerance.md) — “Failure mitigation”, pp. 52–53
