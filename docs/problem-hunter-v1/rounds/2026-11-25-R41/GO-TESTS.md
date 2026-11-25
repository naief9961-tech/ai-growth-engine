# R41 Go follow-up — actual native isolated tests

Checked 2026-11-25T08:47:24.748296+00:00. User requested Go testing. No external comment or third-party repository mutation.

## Environment and integrity

The original /usr/bin/go is a local board-game application, as confirmed by --help. It is not the compiler. Official go1.27.4.linux-amd64.tar.gz was downloaded from https://go.dev/dl/go1.27.4.linux-amd64.tar.gz into an isolated scratch directory, verified against https://go.dev/dl/?mode=json, then extracted with Python tarfile data filter.

- Archive size:70680823 bytes.
- Archive SHA256:7226736c2339719cda28fbf3a54d71aa63bcefe376e98cef00034268dab24840.
- Actual version command: go version go1.27.4 linux/amd64.
- Source: https://github.com/Mag1cFall/Antigravity2API/blob/8caff896859499b86398c1e3e75c964c40dca6f3/internal/app/events.go
- Git blob SHA1 verified locally:5be7315ac786ee97342d5bced4f831450663c3e5.
- One extra newline introduced during local file transfer was detected by hash validation and removed BEFORE extraction/testing. Exact blob hash then matched.
- Seven exact methods extracted:publishLocked,publish,begin,end,track,runningLocked,subscribe.
- Explicit substitutions:requestdb.Row→local Row; minimal event/hub/activeRequest/Trace/Log declarations; Trace.Snapshot stub returns its synthetic immutable row. No production callback/Trace implementation execution.

## Result

Command in each fixture directory:
```sh
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off CGO_ENABLED=1 GOCACHE=/isolated/cache /isolated/go/bin/go test -race -count=1 -json ./...
```
Actual scratch paths were used, not the illustrative /isolated paths above. No external module downloads or upstream entrypoints.

| Top-level group | Original | Candidate |
|---|---|---|
| Delayed captured begin after end: cancelled/failed/completed | FAIL (all3 subcases) | PASS |
| Still-active updates then end | PASS | PASS |
| Unrelated active request | PASS | PASS |
| Fresh subscription excludes ended request | PASS | PASS |
| Concurrent begin/end order (up to200 iterations) | FAIL, stops on first violation | PASS, all200 |
| Full-subscriber close/removal | PASS | PASS |

Original exit1, candidate exit0. Neither emitted DATA RACE; mutex-safe code can still have wrong event order. Six top-level groups, with3 nested state subtests in the first group; not nine independent groups.

The candidate changes only begin: lock hub.mu, require active[row.ID], publishLocked, unlock. It serializes membership and publication with end. Deterministic delayed release uses channels, not sleeps. No new broad stress run was needed after the planned checks passed.

## Limits

These are native compiled tests of extracted source with explicit type stubs. They do not compile the full application, exercise actual Trace.SetAccount or upstream cancellation, test React/EventSource/WebView2, prove the user's observed path, or establish a deployed fix. The source reporter's late request.progress log remains insufficient proof of a late request/running SSE frame. No secrets/API accounts/providers, system tools or production services modified.

## Reproduce

Save upstream events.go at the pinned SHA as events.source.go.txt. Save the following preparation script and test source next to it. Run python3 prepare.py; it verifies the source blob and writes baseline/candidate directories. Use the official local Go toolchain to run the commands above in each directory.

### prepare.py
```python
import pathlib,hashlib,re
p=pathlib.Path(__file__).parent
s=(p/'events.source.go.txt').read_text()
blob=hashlib.sha1(b'blob '+str(len(s.encode())).encode()+b'\0'+s.encode()).hexdigest()
assert blob=='5be7315ac786ee97342d5bced4f831450663c3e5',blob
names=['publishLocked','publish','begin','end','track','runningLocked','subscribe']
methods=[]
for name in names:
    match=re.search(r'^func \(h \*hub\) '+name+r'\(.*?^}',s,re.M|re.S)
    assert match,name
    methods.append(match.group())
prefix='''package fixture
import ("sync"; "time"; "slices")
const (logInitial=200; subscriberBuffer=1024)
type Row struct { ID string; State string; Time time.Time }
type Log struct{}
type Trace struct{ row Row }
func (t *Trace) Snapshot() Row { return t.row }
type activeRequest struct{ trace *Trace }
type event struct{Type string; Data any}
type hub struct{mu sync.Mutex; accounts *event; logs []Log; active map[string]*activeRequest; subscribers map[chan event]struct{}}
'''
original=prefix+'\n\n'.join(methods).replace('requestdb.Row','Row')+'\n'
candidate=original.replace('h.publish(event{Type: "request", Data: row})','''h.mu.Lock()
 defer h.mu.Unlock()
 if _, ok := h.active[row.ID]; !ok { return }
 h.publishLocked(event{Type: "request", Data: row})''')
assert candidate!=original
for name,code in [('baseline',original),('candidate',candidate)]:
    d=p/name;d.mkdir(exist_ok=True)
    (d/'go.mod').write_text('module isolated-fixture\n\ngo 1.27\n')
    (d/'hub.go').write_text(code)
    (d/'hub_test.go').write_text((p/'hub_test.go.txt').read_text())
print('Source Git blob verified; 7 exact hub methods extracted with explicit type stubs.')

```

### hub_test.go.txt
```go
package fixture

import("testing";"sync")

func setup() (*hub,chan event) {
 h:=&hub{active:map[string]*activeRequest{},subscribers:map[chan event]struct{}{}}
 ch:=make(chan event,16);h.subscribers[ch]=struct{}{}
 return h,ch
}
func track(h *hub,id string){h.track(id,&activeRequest{trace:&Trace{row:Row{ID:id,State:"running"}}})}
func drain(ch chan event) []event {var all []event;for{select{case x,ok:=<-ch:if !ok{return all};all=append(all,x);default:return all}}}
func assertFinal(t *testing.T,events []event,id,state string){t.Helper();terminal:=false;for _,e:=range events{r:=e.Data.(Row);if r.ID!=id{continue};if terminal&&r.State=="running"{t.Fatalf("running event after terminal: %+v",events)};if r.State==state{terminal=true}};if !terminal{t.Fatal("terminal event missing")}}

func TestDelayedCapturedBeginAfterEnd(t *testing.T){
 for _,state:=range []string{"cancelled","failed","completed"}{t.Run(state,func(t *testing.T){
  h,ch:=setup();track(h,"a")
  captured:=make(chan struct{});release:=make(chan struct{});done:=make(chan struct{})
  go func(){row:=Row{ID:"a",State:"running"};close(captured);<-release;h.begin(row);close(done)}()
  <-captured;h.end("a",Row{ID:"a",State:state});close(release);<-done
  assertFinal(t,drain(ch),"a",state)
 })}
}
func TestStillActiveUpdatesAndEnd(t *testing.T){
 h,ch:=setup();track(h,"a");h.begin(Row{ID:"a",State:"running"});h.begin(Row{ID:"a",State:"running"});h.end("a",Row{ID:"a",State:"completed"})
 events:=drain(ch);if len(events)!=3{t.Fatalf("want two updates and terminal, got %v",events)};assertFinal(t,events,"a","completed")
}
func TestOtherActiveRequestUnaffected(t *testing.T){
 h,ch:=setup();track(h,"a");track(h,"b");h.end("a",Row{ID:"a",State:"cancelled"});h.begin(Row{ID:"b",State:"running"})
 events:=drain(ch);if len(events)!=2||events[1].Data.(Row).ID!="b"{t.Fatalf("lost unrelated active request: %v",events)}
}
func TestFreshSubscriptionExcludesEnded(t *testing.T){
 h,_:=setup();track(h,"a");track(h,"b");h.end("a",Row{ID:"a",State:"cancelled"})
 events:=drain(h.subscribe());if len(events)!=2{t.Fatalf("want b + ready: %v",events)}
 if events[0].Type!="request"||events[0].Data.(Row).ID!="b"||events[1].Type!="ready"{t.Fatalf("wrong snapshot: %v",events)}
}
func TestConcurrentBeginEndOrdering(t *testing.T){
 for n:=0;n<200;n++{h,ch:=setup();track(h,"a");start:=make(chan struct{});var wg sync.WaitGroup;wg.Add(2)
  go func(){defer wg.Done();<-start;h.begin(Row{ID:"a",State:"running"})}()
  go func(){defer wg.Done();<-start;h.end("a",Row{ID:"a",State:"cancelled"})}()
  close(start);wg.Wait();assertFinal(t,drain(ch),"a","cancelled")
 }
}
func TestFullSubscriberClosedAndRemoved(t *testing.T){
 h,_:=setup();track(h,"a");blocked:=make(chan event);h.subscribers[blocked]=struct{}{};h.begin(Row{ID:"a",State:"running"})
 if _,ok:=h.subscribers[blocked];ok{t.Fatal("full subscriber retained")};if _,ok:=<-blocked;ok{t.Fatal("subscriber not closed")}
}

```

## Exact run evidence
- prepare.py: SHA256 658fcb8c3d30c48167bfb47ba0998ce835c31bb0be49bb13851299bbb2771d49
- hub_test.go.txt: SHA256 8a09d20799409d40025da240fc761fe2497eda03ad93803cd163d2825f96e820
- baseline-results.jsonl: SHA256 19d9c810b5e38564737568be8cc4577afe68b5dd9ca776e9e30399fc4814fea5
- candidate-results.jsonl: SHA256 3cf262f2665dacfa24e455abe8becdf166e6eae91863c41d099b02cb4c388843
- baseline/hub.go: SHA256 ad811331e10b870227174cf52c4f87fc0925928999b39095183924395435dc35
- candidate/hub.go: SHA256 c5a8678cd42f6d109f339a3c4b56cd2a2e6c04d75ee2f1c0ec660b435b0c3e52

### Baseline JSONL
```jsonl
{"Time":"2026-11-25T11:46:15.805522625+03:00","Action":"start","Package":"isolated-fixture"}
{"Time":"2026-11-25T11:46:15.832394224+03:00","Action":"run","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd"}
{"Time":"2026-11-25T11:46:15.832467812+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd","Output":"=== RUN   TestDelayedCapturedBeginAfterEnd\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.832498147+03:00","Action":"run","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled"}
{"Time":"2026-11-25T11:46:15.832501563+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled","Output":"=== RUN   TestDelayedCapturedBeginAfterEnd/cancelled\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.832923257+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled","Output":"    hub_test.go:20: running event after terminal: [{Type:request Data:{ID:a State:cancelled Time:0001-01-01 00:00:00 +0000 UTC}} {Type:request Data:{ID:a State:running Time:0001-01-01 00:00:00 +0000 UTC}}]\n","OutputType":"error"}
{"Time":"2026-11-25T11:46:15.832944583+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled","Output":"--- FAIL: TestDelayedCapturedBeginAfterEnd/cancelled (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833011786+03:00","Action":"fail","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled","Elapsed":0}
{"Time":"2026-11-25T11:46:15.833081304+03:00","Action":"run","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed"}
{"Time":"2026-11-25T11:46:15.8330842+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed","Output":"=== RUN   TestDelayedCapturedBeginAfterEnd/failed\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833231846+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed","Output":"    hub_test.go:20: running event after terminal: [{Type:request Data:{ID:a State:failed Time:0001-01-01 00:00:00 +0000 UTC}} {Type:request Data:{ID:a State:running Time:0001-01-01 00:00:00 +0000 UTC}}]\n","OutputType":"error"}
{"Time":"2026-11-25T11:46:15.833267241+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed","Output":"--- FAIL: TestDelayedCapturedBeginAfterEnd/failed (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833292247+03:00","Action":"fail","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed","Elapsed":0}
{"Time":"2026-11-25T11:46:15.833311133+03:00","Action":"run","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed"}
{"Time":"2026-11-25T11:46:15.833338872+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed","Output":"=== RUN   TestDelayedCapturedBeginAfterEnd/completed\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833447287+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed","Output":"    hub_test.go:20: running event after terminal: [{Type:request Data:{ID:a State:completed Time:0001-01-01 00:00:00 +0000 UTC}} {Type:request Data:{ID:a State:running Time:0001-01-01 00:00:00 +0000 UTC}}]\n","OutputType":"error"}
{"Time":"2026-11-25T11:46:15.833452998+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed","Output":"--- FAIL: TestDelayedCapturedBeginAfterEnd/completed (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833455622+03:00","Action":"fail","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed","Elapsed":0}
{"Time":"2026-11-25T11:46:15.833459045+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd","Output":"--- FAIL: TestDelayedCapturedBeginAfterEnd (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833469272+03:00","Action":"fail","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd","Elapsed":0}
{"Time":"2026-11-25T11:46:15.833492788+03:00","Action":"run","Package":"isolated-fixture","Test":"TestStillActiveUpdatesAndEnd"}
{"Time":"2026-11-25T11:46:15.833495465+03:00","Action":"output","Package":"isolated-fixture","Test":"TestStillActiveUpdatesAndEnd","Output":"=== RUN   TestStillActiveUpdatesAndEnd\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.83354626+03:00","Action":"output","Package":"isolated-fixture","Test":"TestStillActiveUpdatesAndEnd","Output":"--- PASS: TestStillActiveUpdatesAndEnd (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833552223+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestStillActiveUpdatesAndEnd","Elapsed":0}
{"Time":"2026-11-25T11:46:15.833610511+03:00","Action":"run","Package":"isolated-fixture","Test":"TestOtherActiveRequestUnaffected"}
{"Time":"2026-11-25T11:46:15.833612869+03:00","Action":"output","Package":"isolated-fixture","Test":"TestOtherActiveRequestUnaffected","Output":"=== RUN   TestOtherActiveRequestUnaffected\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833615712+03:00","Action":"output","Package":"isolated-fixture","Test":"TestOtherActiveRequestUnaffected","Output":"--- PASS: TestOtherActiveRequestUnaffected (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833617872+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestOtherActiveRequestUnaffected","Elapsed":0}
{"Time":"2026-11-25T11:46:15.833620152+03:00","Action":"run","Package":"isolated-fixture","Test":"TestFreshSubscriptionExcludesEnded"}
{"Time":"2026-11-25T11:46:15.833621785+03:00","Action":"output","Package":"isolated-fixture","Test":"TestFreshSubscriptionExcludesEnded","Output":"=== RUN   TestFreshSubscriptionExcludesEnded\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833734812+03:00","Action":"output","Package":"isolated-fixture","Test":"TestFreshSubscriptionExcludesEnded","Output":"--- PASS: TestFreshSubscriptionExcludesEnded (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833738847+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestFreshSubscriptionExcludesEnded","Elapsed":0}
{"Time":"2026-11-25T11:46:15.83376583+03:00","Action":"run","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering"}
{"Time":"2026-11-25T11:46:15.833768071+03:00","Action":"output","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering","Output":"=== RUN   TestConcurrentBeginEndOrdering\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833940871+03:00","Action":"output","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering","Output":"    hub_test.go:40: running event after terminal: [{Type:request Data:{ID:a State:cancelled Time:0001-01-01 00:00:00 +0000 UTC}} {Type:request Data:{ID:a State:running Time:0001-01-01 00:00:00 +0000 UTC}}]\n","OutputType":"error"}
{"Time":"2026-11-25T11:46:15.83395686+03:00","Action":"output","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering","Output":"--- FAIL: TestConcurrentBeginEndOrdering (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.833960226+03:00","Action":"fail","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering","Elapsed":0}
{"Time":"2026-11-25T11:46:15.833982727+03:00","Action":"run","Package":"isolated-fixture","Test":"TestFullSubscriberClosedAndRemoved"}
{"Time":"2026-11-25T11:46:15.83398488+03:00","Action":"output","Package":"isolated-fixture","Test":"TestFullSubscriberClosedAndRemoved","Output":"=== RUN   TestFullSubscriberClosedAndRemoved\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.834061785+03:00","Action":"output","Package":"isolated-fixture","Test":"TestFullSubscriberClosedAndRemoved","Output":"--- PASS: TestFullSubscriberClosedAndRemoved (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.834064511+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestFullSubscriberClosedAndRemoved","Elapsed":0}
{"Time":"2026-11-25T11:46:15.834066582+03:00","Action":"output","Package":"isolated-fixture","Output":"FAIL\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.834285013+03:00","Action":"output","Package":"isolated-fixture","Output":"FAIL\tisolated-fixture\t0.028s\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:15.834309374+03:00","Action":"fail","Package":"isolated-fixture","Elapsed":0.029}

```

### Candidate JSONL
```jsonl
{"Time":"2026-11-25T11:46:34.471032594+03:00","Action":"start","Package":"isolated-fixture"}
{"Time":"2026-11-25T11:46:34.497153813+03:00","Action":"run","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd"}
{"Time":"2026-11-25T11:46:34.497228516+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd","Output":"=== RUN   TestDelayedCapturedBeginAfterEnd\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.497286169+03:00","Action":"run","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled"}
{"Time":"2026-11-25T11:46:34.49728956+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled","Output":"=== RUN   TestDelayedCapturedBeginAfterEnd/cancelled\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.497994417+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled","Output":"--- PASS: TestDelayedCapturedBeginAfterEnd/cancelled (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.498006803+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/cancelled","Elapsed":0}
{"Time":"2026-11-25T11:46:34.498057839+03:00","Action":"run","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed"}
{"Time":"2026-11-25T11:46:34.498060785+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed","Output":"=== RUN   TestDelayedCapturedBeginAfterEnd/failed\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.498222337+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed","Output":"--- PASS: TestDelayedCapturedBeginAfterEnd/failed (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.498376982+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/failed","Elapsed":0}
{"Time":"2026-11-25T11:46:34.498380991+03:00","Action":"run","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed"}
{"Time":"2026-11-25T11:46:34.498382765+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed","Output":"=== RUN   TestDelayedCapturedBeginAfterEnd/completed\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.498533918+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed","Output":"--- PASS: TestDelayedCapturedBeginAfterEnd/completed (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.498539007+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd/completed","Elapsed":0}
{"Time":"2026-11-25T11:46:34.498578706+03:00","Action":"output","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd","Output":"--- PASS: TestDelayedCapturedBeginAfterEnd (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.498603379+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestDelayedCapturedBeginAfterEnd","Elapsed":0}
{"Time":"2026-11-25T11:46:34.498644514+03:00","Action":"run","Package":"isolated-fixture","Test":"TestStillActiveUpdatesAndEnd"}
{"Time":"2026-11-25T11:46:34.498646987+03:00","Action":"output","Package":"isolated-fixture","Test":"TestStillActiveUpdatesAndEnd","Output":"=== RUN   TestStillActiveUpdatesAndEnd\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.498791301+03:00","Action":"output","Package":"isolated-fixture","Test":"TestStillActiveUpdatesAndEnd","Output":"--- PASS: TestStillActiveUpdatesAndEnd (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.498795307+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestStillActiveUpdatesAndEnd","Elapsed":0}
{"Time":"2026-11-25T11:46:34.498813649+03:00","Action":"run","Package":"isolated-fixture","Test":"TestOtherActiveRequestUnaffected"}
{"Time":"2026-11-25T11:46:34.498816102+03:00","Action":"output","Package":"isolated-fixture","Test":"TestOtherActiveRequestUnaffected","Output":"=== RUN   TestOtherActiveRequestUnaffected\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.499084304+03:00","Action":"output","Package":"isolated-fixture","Test":"TestOtherActiveRequestUnaffected","Output":"--- PASS: TestOtherActiveRequestUnaffected (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.49908898+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestOtherActiveRequestUnaffected","Elapsed":0}
{"Time":"2026-11-25T11:46:34.499143371+03:00","Action":"run","Package":"isolated-fixture","Test":"TestFreshSubscriptionExcludesEnded"}
{"Time":"2026-11-25T11:46:34.499146072+03:00","Action":"output","Package":"isolated-fixture","Test":"TestFreshSubscriptionExcludesEnded","Output":"=== RUN   TestFreshSubscriptionExcludesEnded\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.49954607+03:00","Action":"output","Package":"isolated-fixture","Test":"TestFreshSubscriptionExcludesEnded","Output":"--- PASS: TestFreshSubscriptionExcludesEnded (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.499549567+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestFreshSubscriptionExcludesEnded","Elapsed":0}
{"Time":"2026-11-25T11:46:34.499722227+03:00","Action":"run","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering"}
{"Time":"2026-11-25T11:46:34.499726573+03:00","Action":"output","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering","Output":"=== RUN   TestConcurrentBeginEndOrdering\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.516917358+03:00","Action":"output","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering","Output":"--- PASS: TestConcurrentBeginEndOrdering (0.02s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.516949282+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestConcurrentBeginEndOrdering","Elapsed":0.02}
{"Time":"2026-11-25T11:46:34.51717286+03:00","Action":"run","Package":"isolated-fixture","Test":"TestFullSubscriberClosedAndRemoved"}
{"Time":"2026-11-25T11:46:34.517176623+03:00","Action":"output","Package":"isolated-fixture","Test":"TestFullSubscriberClosedAndRemoved","Output":"=== RUN   TestFullSubscriberClosedAndRemoved\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.517521975+03:00","Action":"output","Package":"isolated-fixture","Test":"TestFullSubscriberClosedAndRemoved","Output":"--- PASS: TestFullSubscriberClosedAndRemoved (0.00s)\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:34.517536036+03:00","Action":"pass","Package":"isolated-fixture","Test":"TestFullSubscriberClosedAndRemoved","Elapsed":0}
{"Time":"2026-11-25T11:46:34.517591279+03:00","Action":"output","Package":"isolated-fixture","Output":"PASS\n","OutputType":"frame"}
{"Time":"2026-11-25T11:46:35.526931655+03:00","Action":"output","Package":"isolated-fixture","Output":"ok  \tisolated-fixture\t1.055s\n"}
{"Time":"2026-11-25T11:46:35.527532412+03:00","Action":"pass","Package":"isolated-fixture","Elapsed":1.057}

```
