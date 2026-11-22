# R38 isolated evidence

Date: 2026-11-22. Six assertions passed with Python3. This is an abstract schedule model, not source extraction, upstream Go execution, or proof of a shipped fix.

## Assumptions grounded in pinned source
Commit 612177bc37bf2cfc3a9ee729bd48810076c45232: server_test.go sends q1 with ReturnImmediately=true; tasks.go launches Receive in a goroutine; fake.go uses a shared FIFO; mapping.go maps Unknown to Working and Accepted inform to Completed; tasks.go defers leaveWait until SendMessage returns.
S queues the scripted result, Q is q1 injection, E acquires hang's wait slot, H is hang injection, F is its potential terminal return, W attempts the second wait. Q's task creation happened before S but Q injection may happen later. W requires the scripted Entered signal. Each abstract event is atomic; this is not an exhaustive model of Go scheduling, failures, locks, SDK or networking. Counts are model schedules, not observed CI frequencies.

## Actual output
```text
PASS: 6 model assertions
baseline valid modeled schedules: 15
baseline second wait admitted: 3
fixed valid modeled schedules: 2
fixed second wait admitted: 0
No upstream Go, HTTP, race detector or CI execution.
```

## Executed script
```python
from itertools import permutations
# Abstract event model only; not upstream Go or SDK execution.
# S queues Unknown+Entered. Q/H consume FIFO at Inject.
def simulate(order):
    queue = []
    signaled = False
    waiting = 0
    h_state = None
    consumer = None
    result = None
    for event in order:
        if event == "S":
            queue.append("unknown")
        elif event in ("Q", "H"):
            state = queue.pop(0) if queue else "accepted"
            if state == "unknown":
                signaled = True
                consumer = event
            if event == "H":
                h_state = state
        elif event == "E":
            waiting += 1
        elif event == "F":
            if h_state == "accepted":
                waiting -= 1
        elif event == "W":
            if not signaled:
                return None
            result = waiting >= 1
    return consumer, result

def legal(order, fixed=False):
    pos = {x: order.index(x) for x in order}
    if not (pos["S"] < pos["E"] < pos["H"] < pos["F"]):
        return False
    if not pos["S"] < pos["W"]:
        return False
    if fixed and not pos["Q"] < pos["S"]:
        return False
    return True

base = [(p, simulate(p)) for p in permutations("SQEHFW") if legal(p)]
base = [(p, r) for p, r in base if r is not None]
fixed = [(p, simulate(p)) for p in permutations("SQEHFW") if legal(p, True)]
fixed = [(p, r) for p, r in fixed if r is not None]
assert simulate(tuple("SQEHFW")) == ("Q", False)
assert simulate(tuple("SEHFWQ")) == ("H", True)
assert any(r == ("Q", False) for _, r in base)
assert all(r[0] == "Q" for _, r in base if not r[1])
assert fixed and all(r == ("H", True) for _, r in fixed)
assert simulate(tuple("QSEHFW")) == ("H", True)
print("PASS: 6 model assertions")
print("baseline valid modeled schedules:", len(base))
print("baseline second wait admitted:", sum(not r[1] for _,r in base))
print("fixed valid modeled schedules:", len(fixed))
print("fixed second wait admitted:", sum(not r[1] for _,r in fixed))
print("No upstream Go, HTTP, race detector or CI execution.")
```

## Native validation still required
Use the existing beforeReceive hook to force q1 to reach the shared fake only after ScriptInject has queued the outcome. Track the message that consumes it; do not rely on a sleep. In the proposed test, waitState(q1, Working) precedes the queue. Keep MaxOpenAsks and size assertions; verify too_many_waits, correct Entered ownership, cancel/release, bounded channel waits and goroutine cleanup. Run TestAdmission and the deterministic case under -race on Linux/macOS. No compiler/runtime was installed in this round and no workflow was dispatched. Command go version returned "Go: Unknown option: version"; expected Go locations absent. This is an environment limitation, not a test failure in CrossTalk.
