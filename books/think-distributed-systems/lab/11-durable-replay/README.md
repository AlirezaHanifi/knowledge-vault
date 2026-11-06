# Log-based durable execution

How does log-based durable execution recover a process, and what breaks it? The script implements a tiny runtime. A process is a generator that yields steps; the runtime runs each step, records its result in a durable log, and sends the result back into the generator. After a crash, it starts the generator again and replays: steps already in the log are not re-executed, and their logged results are fed back instead. The book's `alphabet()` process is crashed after every step, just before the step's result is logged. The run is repeated with a version that branches on the clock outside a step.

*Illustrates Think Distributed Systems, Listings 11.2 and 11.6–11.7, pp. 149–155: log-based recovery replays from the log and requires deterministic execution. The crash model, the restart comparison and the clock-reading variant are the vault's.*

## Run

Python 3.10+, standard library only, deterministic (seeded):

```sh
python3 durable_replay.py
```

## Expected output

```text
Failure-free: a•b•c•d•e•f•✓

Deterministic alphabet(), crash after step k ran but before it was logged
 k  log-based replay                 restart
 1  a•💥•a•b•c•d•e•f•✓                a•💥•a•b•c•d•e•f•✓
 2  a•b•💥•b•c•d•e•f•✓                a•b•💥•a•b•c•d•e•f•✓
 3  a•b•c•💥•c•d•e•f•✓                a•b•c•💥•a•b•c•d•e•f•✓
 4  a•b•c•d•💥•d•e•f•✓                a•b•c•d•💥•a•b•c•d•e•f•✓
 5  a•b•c•d•e•💥•e•f•✓                a•b•c•d•e•💥•a•b•c•d•e•f•✓
 6  a•b•c•d•e•f•💥•f•✓                a•b•c•d•e•f•💥•a•b•c•d•e•f•✓

The clock reads 0 on the first run and 1 on recovery (branch outside a step)
 k  log-based replay                                                       restart
 1  a•💥•a•b•c•D•e•f•✓                                                      a•💥•a•b•c•D•e•f•✓
 2  a•b•💥•b•c•D•e•f•✓                                                      a•b•💥•a•b•c•D•e•f•✓
 3  a•b•c•💥•c•D•e•f•✓                                                      a•b•c•💥•a•b•c•D•e•f•✓
 4  a•b•c•d•💥•D•e•f•✓                                                      a•b•c•d•💥•a•b•c•D•e•f•✓
 5  a•b•c•d•e•💥  ✗ replay diverged: log has step 4 = d, code yielded D     a•b•c•d•e•💥•a•b•c•D•e•f•✓
 6  a•b•c•d•e•f•💥  ✗ replay diverged: log has step 4 = d, code yielded D   a•b•c•d•e•f•💥•a•b•c•D•e•f•✓
```

## What to look for

- Replay repeats exactly one event, the step that ran but wasn't logged: “valid to duplicate the last event”. Restart repeats everything done so far.
- Crashing after step k ran but before it was logged repeats step k. Had the crash come after logging, replay would repeat nothing.
- With a clock read outside a step, the rerun takes the other branch. If the crash came after step 4 was logged, replay notices that the code no longer matches the log and stops.
- If the crash came earlier, replay doesn't notice, and the trace contains a step from each branch (d before the crash, D after) or the new branch only. Restart's traces mix branches the same way. Determinism is the programmer's job.

## Related

- Chapter note: [11. Durable executions](../../chapters/11-durable-executions.md) — “Durable execution”, pp. 153–155
