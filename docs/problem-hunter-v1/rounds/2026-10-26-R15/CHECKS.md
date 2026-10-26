# R15 checks — NOT EXECUTED

This is a regression plan, not a test-results claim. No Qt development environment/pkg-config is available in the local isolated environment. No upstream build, dump executable, client or hardware was run.

1. Build the corrected MCP plugin and tools-dump helper in the maintainers' supported Qt environment.
2. Read live tools/list without invoking tune_gain. Find tune_gain by name, not by array index or a fixed catalog size.
3. Assert values.type == array and values.items.type == number. Compare the rest of that inputSchema to the baseline; values must not become globally required.
4. Generate server/tools.json through the existing build target; run the same assertions against the generated catalog.
5. Check discovery through the bridge both before SDRangel starts (bundled catalog) and while it is running (live catalog).
6. Add a client-specific array-items compatibility assertion; generic JSON Schema meta-schema validation cannot enforce the reported Copilot restriction.
7. Reverting the property change should fail that targeted catalog assertion. Keep scan.frequencies' numeric items and the other definitions unchanged.

No additional minimum length, range, uniqueness or device policy is proposed. Numeric item schemas describe client input; they do not establish new runtime validation in tuneGain. Full Copilot acceptance remains to be verified.
