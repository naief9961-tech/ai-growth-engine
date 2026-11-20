# R36 isolated evidence
Executed successfully on 2026-11-20 with Git2.56.1: 11 assertion groups pass. Python GitPython import failed (module unavailable); the harness below invokes the Git CLI directly, not extracted server code. No network, secrets, remote fetch, wallet, provider or live deployment.

Checks: baseline "* main" fails rev-parse; clean local name resolves; linked-worktree "+" marker; forced colors; remote symbolic HEAD; both ref namespaces; contains; not_contains; combined filters; detached HEAD pseudo-entry from branch --format; branch/tag collision resolved using a qualified ref.

The candidate enumeration passes tested cases. This does not mean every returned short name is safe for every downstream operation; branch/tag collision and remote checkout semantics remain explicit integration requirements. No full MCP/GitPython/macOS test ran.

Official command semantics: https://git-scm.com/docs/git-for-each-ref (read2026-11-20).

## Exact executed harness
```python
import os, subprocess, tempfile, json
from pathlib import Path
env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
 GIT_AUTHOR_NAME="Synthetic Test", GIT_AUTHOR_EMAIL="test@example.invalid",
 GIT_COMMITTER_NAME="Synthetic Test", GIT_COMMITTER_EMAIL="test@example.invalid")
results=[]
with tempfile.TemporaryDirectory(prefix="naif-r36-") as temp:
 root=Path(temp); repo=root/"repo"; repo.mkdir()
 def git(*args,check=True):
  return subprocess.run(["git","-C",str(repo),*args],env=env,text=True,capture_output=True,check=check)
 def out(*args): return git(*args).stdout.strip()
 def refs(kind="local",*filters):
  roots={"local":["refs/heads"],"remote":["refs/remotes"],"all":["refs/heads","refs/remotes"]}[kind]
  return out("for-each-ref","--format=%(refname:lstrip=2)",*filters,*roots).splitlines()
 def check(name,condition,evidence):
  assert condition, (name,evidence)
  results.append({"name":name,"pass":True,"evidence":evidence})
 git("init","-b","main");git("commit","--allow-empty","-m","synthetic initial")
 first=out("rev-parse","HEAD")
 raw=out("branch")
 check("baseline current marker",raw=="* main" and git("rev-parse","--verify",raw+"^{commit}",check=False).returncode!=0,raw)
 check("candidate local name resolves",refs()==["main"] and out("rev-parse","--verify",refs()[0]+"^{commit}")==first,refs())
 git("branch","work");git("worktree","add",str(root/"work"),"work")
 raw=out("branch")
 check("linked worktree marker", "+ work" in raw and refs()==["main","work"],{"baseline":raw,"candidate":refs()})
 git("config","color.branch","always")
 raw=out("branch")
 check("color independent enumeration","\x1b" in raw and all("\x1b" not in x for x in refs()),{"baseline":repr(raw),"candidate":refs()})
 git("update-ref","refs/remotes/origin/main",first);git("symbolic-ref","refs/remotes/origin/HEAD","refs/remotes/origin/main")
 check("remote alias no presentation arrow",refs("remote")==["origin/HEAD","origin/main"] and all(out("rev-parse","--verify",x+"^{commit}")==first for x in refs("remote")),refs("remote"))
 check("all roots",refs("all")==["main","work","origin/HEAD","origin/main"],refs("all"))
 git("commit","--allow-empty","-m","synthetic second")
 second=out("rev-parse","HEAD")
 check("contains retained",refs("local","--contains",second)==["main"],refs("local","--contains",second))
 check("not contains retained",refs("local","--no-contains",second)==["work"],refs("local","--no-contains",second))
 check("combined filters retained",refs("all","--contains",first,"--no-contains",second)==["work","origin/HEAD","origin/main"],refs("all","--contains",first,"--no-contains",second))
 git("checkout","--detach",first)
 formatted=out("branch","--no-color","--format=%(refname:short)")
 check("format only detached pseudo entry","HEAD detached" in formatted and refs()==["main","work"],{"format_only":formatted,"candidate":refs()})
 git("tag","main",first)
 # Fully-qualified refs disambiguate a branch/tag collision; short-name output alone cannot.
 check("full ref resolves branch despite tag collision",out("rev-parse","--verify","refs/heads/main^{commit}")==second,{"branch":second,"tag":first})
 print(json.dumps({"git_version":out("--version"),"passed":len(results),"results":results,"limits":"Real Git CLI only, no GitPython, MCP server, downstream tool integration or full upstream suite."},indent=2))
```
