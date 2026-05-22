You are correct, and thank you for testing this carefully.

We just checked on the public development node:

specVersion: 1002
Contract API (0x40fe3ad401f8959a): version 5
Same result as your local node. Both run the same binary the public node doesn't help in this case.

After testing, i’ve found incompatibility with the public community node:

Node runtime info:
specName: portaldot
specVersion: 1002
contracts API version: 5

Contracts API version 5 only supports ink! 3.x. ink! 4.x requires contracts API version 9+. So my ink! 4.x contract fails with a generic Other dispatch error at the runtime level

Attempt downgrade to ink! 3.x is just dependency nightmare:

The node needs to be upgraded to a modern substrate-contracts-node that supports contracts API version 9+ for ink! 4.x to work


Current state (verified):

All current Portaldot nodes → Contract API v5 → only ink! 3.x
ink! 4.x requires Contract API v9+ → needs a node update from the Portaldot team
ink! 3.x is compatible with v5, but currently has issues on crates.io (toml_datetime bug)
There is no client-side workaround. This requires the Portaldot team to provide a node with a modern runtime environment.

For the hackathon at the moment, the only viable solution is to use native pallets via @polkadot/api  list what's available in the node with Object.keys(api.tx) and build from there.

I will update the PortalFix page to accurately reflect this: portalfix.netlify.app/#/problem/node-rejects-ink4
Thank you for the detailed analysis. Some corrections based on what actually works:

Option 1 helps with the gas format (passing a simple u64 instead of { ref_time, proof_size }), but doesn't solve the main problem. If your WASM was compiled with ink! 4.x, the node's v5 contract API will still reject it regardless of how the transaction is sent.

Option 3 presents the same situation – the UI sends the same extrinsic parameter, the same WASM, and the same rejection occurs.

What actually works at the moment:

Completely ignore the local node. Use the public development node, which runs a modern runtime environment with the v9+ contract API and full ink! 4.x support:

const provider = new WsProvider('wss://drip-backend-production-8d86.up.railway.app/node');

const api = await ApiPromise.create({ provider });

Create with cargo-contract 4.x + ink! 4.x and deploy there. Alice is already pre-funded, no configuration needed.

If you specifically need the local node v2.0.0, the only compatible combination is ink! 3.x + cargo-contract 0.17.x or 1.4.x — but ink! 3.x is currently having issues on crates.io due to a toml_datetime dependency bug, so that path is also blocked.

The definitive solution is what you said, a node update by the team. In the meantime, the public node is the only path that works today.

Must we deploy on ui?
Not necessary, you can just submit the guide in your GitHub and the judge will go through it

