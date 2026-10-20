// Proposed pure helper; not integrated into Woodhouse or deployed.
// Register each event here from GuardedApp.on, beside the existing app.on call.
// Keep one index per Probot/App instance. Do not install an unguarded onAny handler.
function createSubscriptionIndex() {
  const names = new Set();
  return {
    register(events) {
      for (const name of Array.isArray(events) ? events : [events]) names.add(name);
    },
    matches(event, action) {
      return names.has(event) ||
        (typeof action === 'string' && action.length > 0 && names.has(`${event}.${action}`));
    },
  };
}

// Call ONLY after verifyAndReceive resolves, with the JSON-parsed verified body.
// This reports subscription matching, not handler completion or schema validity.
function logUnmatchedVerified(index, payload, metadata, log) {
  const action = payload && typeof payload === 'object' && typeof payload.action === 'string'
    ? payload.action : undefined;
  if (index.matches(metadata.event, action)) return false;
  log.warn({
    deliveryId: metadata.deliveryId,
    app: metadata.app,
    event: metadata.event,
    action: action ?? null,
    outcome: 'unmatched-subscription',
  }, 'Verified webhook has no matching subscription');
  return true;
}
module.exports = { createSubscriptionIndex, logUnmatchedVerified };
