# Majority-voted redundancy

When does triple redundancy beat a single component? Each trial evaluates one gate, and three gates whose outputs a majority gate combines. Every component is right with probability p, independently. The script compares a single gate, three gates with a perfect voter (which should match the formula 3p² − 2p³), three gates with one unreliable voter, and three gates with three unreliable voters whose outputs are combined by majority, for p from 0.4 to 0.999.

*Illustrates Think Distributed Systems, “Redundancy”, pp. 107–108 and Figure 8.1: redundancy is duplication plus coordination, and the majority gate is replicated too. The independent-failure model, the formula and the trial counts are the vault's.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 majority_redundancy.py
```

## Expected output

```text
200,000 trials per row; a component is right with probability p

     p    single   3p²−2p³  TMR, perfect voter  TMR, 1 voter  TMR, 3 voters
   0.4    0.3991    0.3520              0.3499        0.5310         0.5453
   0.5    0.5008    0.5000              0.4992        0.4991         0.4999
   0.7    0.6976    0.7840              0.7831        0.6121         0.6611
   0.9    0.9008    0.9720              0.9728        0.8782         0.9464
  0.95    0.9499    0.9927              0.9929        0.9431         0.9859
  0.99    0.9902    0.9997              0.9997        0.9896         0.9994
 0.999    0.9990    1.0000              1.0000        0.9990         1.0000
```

## What to look for

- With a perfect voter, the measured reliability matches 3p² − 2p³ to three decimals.
- Redundancy only pays off when components are good: at p = 0.4 three gates do worse than one (0.35 against 0.40), at p = 0.5 they're equal, and above that they win.
- One unreliable voter throws the gain away. It is a new single point of failure and caps the system at about p.
- Replicating the voter recovers most of the gain: at p = 0.99, 0.9994 against 0.9896 with one voter. (At p = 0.4 wrong voters flip wrong majorities back, a quirk of this simple model.)

## Related

- Chapter note: [8. Replication](../../chapters/08-replication.md) — “Redundancy”, pp. 107–108
