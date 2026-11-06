"""A tiny log-based durable-execution runtime, crashed after every step.

Illustrates Think Distributed Systems, Chapter 11, Listings 11.2 and 11.6-11.7
(pp. 149-155): a process is a generator that yields steps; the runtime records
each step's result in a durable log and, on recovery, replays logged results
instead of re-executing. The crash model (crash after a step ran, before its
result was logged), the restart comparison and the clock-reading variant are
the vault's.
"""


class Crash(Exception):
    pass


def letter(x, trace):
    def step():
        trace.append(x)       # the observable side effect
        return x
    step.name = x
    return step


def alphabet(trace, clock):
    for x in "abc":
        yield letter(x, trace)
    # Deterministic: always 'd'. Nondeterministic: decided by the clock, outside any step.
    yield letter("d" if clock is None or clock() % 2 == 0 else "D", trace)
    for x in "ef":
        yield letter(x, trace)


def execute(make, log, crash_at, trace):
    """Run with replay. Raises Crash after step `crash_at` runs, before it is logged."""
    gen = make()
    i, result = 0, None
    try:
        step = gen.send(None)
        while True:
            i += 1
            if i <= len(log):
                name, result = log[i - 1]
                if step.name != name:
                    raise RuntimeError(f"replay diverged: log has step {i} = {name}, code yielded {step.name}")
            else:
                result = step()
                if i == crash_at:
                    raise Crash
                log.append((step.name, result))
            step = gen.send(result)
    except StopIteration:
        return


def durable(crash_at, clock_values=None):
    trace, log, runs = [], [], iter(clock_values or [])
    def make():
        c = next(runs, None)
        return alphabet(trace, None if c is None else (lambda: c))
    try:
        execute(make, log, crash_at, trace)
    except Crash:
        trace.append("💥")
        try:
            execute(make, log, None, trace)
        except RuntimeError as e:
            return "•".join(trace) + "  ✗ " + str(e)
    return "•".join(trace) + "•✓"


def restart(crash_at, clock_values=None):
    trace, runs = [], iter(clock_values or [])
    for attempt in range(2):
        c = next(runs, None)
        for i, step in enumerate(alphabet(trace, None if c is None else (lambda: c)), 1):
            step()
            if attempt == 0 and i == crash_at:
                trace.append("💥")
                break
        else:
            break
    return "•".join(trace) + "•✓"


def main():
    print("Failure-free:", durable(None))
    print("\nDeterministic alphabet(), crash after step k ran but before it was logged")
    print(f"{'k':>2}  {'log-based replay':<32} restart")
    for k in range(1, 7):
        print(f"{k:>2}  {durable(k):<32} {restart(k)}")
    print("\nThe clock reads 0 on the first run and 1 on recovery (branch outside a step)")
    print(f"{'k':>2}  {'log-based replay':<70} restart")
    for k in range(1, 7):
        print(f"{k:>2}  {durable(k, [0, 1]):<70} {restart(k, [0, 1])}")


if __name__ == "__main__":
    main()
