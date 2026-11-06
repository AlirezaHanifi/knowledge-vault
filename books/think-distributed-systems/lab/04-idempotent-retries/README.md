# Exactly-once by idempotence

What does it take to charge every order exactly once over an unreliable network? This experiment sends 10,000 payment requests over a network that loses 15% of requests and 15% of responses and duplicates 5% of requests. Under **at-most-once**, the sender tries once. Under **at-least-once**, it retries until it sees a response. Under **at-least-once with an idempotence key**, it also sends one UUID with the request and every retry, and the payment service deduplicates on it.

*Illustrates Think Distributed Systems, “Message delivery semantics”, “Exactly-once processing semantics” and “Idempotence”, pp. 57–63: at-least-once processing plus an idempotent step gives exactly-once processing semantics. The loss and duplication rates, the retry limit and the implementation are the vault's (seeded).*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 idempotent_retries.py
```

## Expected output

```text
10,000 orders; request lost 15%, response lost 15%, request duplicated 5%

mode                    charged 0x  exactly 1x  2x or more  max
at-most-once                15.30%      80.49%       4.21%    2
at-least-once                0.00%      80.81%      19.19%    6
at-least-once + key          0.00%     100.00%       0.00%    1
```

## What to look for

- At-most-once leaves orders uncharged whenever the request is lost, and the network's own duplicates still charge some orders twice.
- At-least-once charges every order, but a lost response looks the same as a lost request to the sender, so about one order in five is charged two or more times.
- With an idempotence key, every order is charged exactly once: the retries still arrive, but the service recognizes them.
- The service records the key together with the charge. Recording it in a separate step would bring back the crash windows of the book's two failed deduplication attempts.

## Related

- Chapter note: [4. Message delivery and processing](../../chapters/04-message-delivery-and-processing.md) — “Idempotence”, pp. 62–63
