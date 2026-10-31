# Isolated baseline checks
Node 24.22.1; node r20.ts exited 0. The expected 404 log preceded `2 branch controls passed`. Original resync function; fake KV, exceptions and injected lookup failure. The 429 control injects the exception into the catch branch; it does not simulate a real Discord edit. No fix test, upstream suite or network.

```ts
const RESYNC_PER_RUN=5;class DiscordError extends Error{constructor(status){super();this.status=status}};class GithubError extends Error{constructor(status){super();this.status=status}};const rateLimited=(e)=>e instanceof DiscordError&&e.status===429;let failure;const getIssue=async()=>{throw failure};
export async function resyncStarterIssues(env: Env, cfg: Config): Promise<void> {
  const { keys } = await env.STATE.list({ prefix: "resync:", limit: RESYNC_PER_RUN });
  for (const { name } of keys) {
    const [, repo, number] = /^resync:(.+)#(\d+)$/.exec(name) ?? [];
    // Removed before reading GitHub, so a mark the webhook writes meanwhile stays.
    await env.STATE.delete(name);
    if (!repo || !number) continue;
    try {
      const current = await getIssue(env, cfg, repo, Number(number));
      const issue: StarterIssue = { repo, number: current.number, title: current.title, url: current.html_url, labels: current.labels.map((l) => l.name) };
      const record = await env.STATE.get<FeedRecord>(feedKey(repo, current.number), "json");
      const state = starterState(current, cfg);
      // Like onIssue, only post issues that are free to take right now.
      if (!record && state.kind !== "open") continue;
      await writeFeed(env, record, issue, state);
    } catch (err) {
      if (rateLimited(err)) {
        // The channel is still limited, so the rest wait as well.
        await env.STATE.put(name, "1");
        return;
      }
      console.error("starter issue resync failed", name, err);
    }
  }
}
import assert from 'node:assert/strict';for(const [error,kept] of [[new GithubError(404),false],[new DiscordError(429),true]]){failure=error;const kv=new Map([['resync:r#1','1'],['issue:r#1','open']]);await resyncStarterIssues({STATE:{list:async()=>({keys:[{name:'resync:r#1'}]}),delete:async k=>kv.delete(k),put:async(k,v)=>kv.set(k,v)}},{});assert.equal(kv.has('resync:r#1'),kept);assert.equal(kv.get('issue:r#1'),'open');}console.log('2 branch controls passed');
```
