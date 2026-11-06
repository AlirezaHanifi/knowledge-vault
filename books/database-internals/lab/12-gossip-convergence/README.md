# Gossip convergence

How quickly does gossip reach a whole cluster, and how many messages does it waste? Starting from one node, every node that knows the information pushes it to `fanout` random peers each round. The experiment counts rounds until everyone knows, messages per node, and the share of messages that reach nodes that already knew. It covers 100, 1,000 and 10,000 nodes, averaged over 20 seeded runs.

*Illustrates Database Internals, “Gossip Dissemination”, pp. 250–253: information spreads in a logarithmic number of rounds, with redundant messages to nodes that are already infected. The vault simplifies by having every infected node keep pushing until all are infected, with no interest loss. The cluster sizes, fanouts and implementation are the vault's.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 gossip.py
```

## Expected output

```text
Push gossip from one node, averaged over 20 seeded runs

 nodes fanout  rounds  log2 N  messages/node  redundant
   100      1    12.2     6.6            5.6        82%
   100      2     7.5     6.6            6.2        84%
   100      3     5.7     6.6            6.5        85%
  1000      1    18.1    10.0            8.0        87%
  1000      2    10.7    10.0            8.5        88%
  1000      3     8.2    10.0            9.0        89%
 10000      1    23.8    13.3           10.4        90%
 10000      2    13.9    13.3           10.7        91%
 10000      3    10.6    13.3           11.1        91%
```

## What to look for

- Rounds grow with log N: going from 100 to 10,000 nodes, 100 times more, adds only about 10 rounds at fanout 1.
- A larger fanout cuts rounds and pushes them below log₂ N, but each node then sends more messages per round.
- Most messages are redundant, 80–90% here, because nodes keep pushing after almost everyone knows. That is why real systems stop after a node has hit too many peers that already knew (interest loss).
- Messages per node grow only slowly with cluster size, which is why gossip scales.

## Related

- Chapter note: [12. Anti-Entropy and Dissemination](../../chapters/12-anti-entropy-and-dissemination.md) — “Gossip Dissemination”, pp. 250–253
