# Event-time windows and stragglers

Counts 3,000 events in one-minute tumbling windows. Events normally arrive after ~2 s, 3% come from offline devices minutes later, and the consumer is down for one minute and then catches up. Compares processing-time windows with event-time windows closed after a 5 s or 60 s grace period, dropping stragglers or publishing corrections.

*Illustrates DDIA 2nd ed., “Reasoning About Time”, pp. 518–523. The implementation is the vault’s own.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 windows.py
```

## Expected output

```text
Per-minute counts (3,000 events; 3% from offline devices; consumer down 300-360 s)

minute   true  proc-time  ev-time+5s  ev-time+60s  +corrections
     0    302        278         290          292       302 (+12)
     1    309        301         299          300       309 (+10)
     2    299        295         289          290       299 (+10)
     3    327        323         318          319       327 (+9)
     4    297        305         282          282       297 (+15)
     5    306          0         253          300       306 (+53)
     6    265        572         259          261       265 (+6)
     7    295        297         287          288       295 (+8)
     8    321        321         314          315       321 (+7)
     9    279        308         272          274       279 (+7)

Total absolute error   processing time: 692   event time, 5 s grace: 137 (137 dropped)   60 s grace: 79 (79 dropped)   with corrections: 0
Waiting longer reduces dropped stragglers but delays every result by the grace period.
```

## What to look for

- Processing-time windows show minute 5 as empty and minute 6 as double — an artefact of the outage, not of user behaviour (Figure 12-8).
- A longer grace period drops fewer stragglers but delays every result.
- Publishing corrections converges on the true counts, at the price of results that change after first being emitted.

## Related

- Chapter note: [12. Stream Processing](../../chapters/12-stream-processing.md) — “Reasoning About Time”, pp. 518–523
- Explore in the browser: [Event time and stragglers](../../widgets/12-stream-time.html)
