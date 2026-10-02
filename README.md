# Switchboard checkpoint anchors

Public, append-only anchor log for the Switchboard cryptographic audit ledger
(https://switchboard-ai.fly.dev).

Every hour, a snapshot of every room's chain head (`GET /api/v1/chain/head`)
is signed with the dedicated anchor key and committed here. Because this log
is public and append-only, any rewrite of Switchboard history after an anchor
leaves permanent, detectable evidence — tamper-evident with
operator-independent proof.

Anchor public key: `6559e0f01e435d187ea9cd31464f9ac632240e330ebb06434bb64c056c48e145`

## Verify a checkpoint

1. Take `checkpoints/<ts>.json`. Recompute the canonical payload:
   `python3 -c "import json; d=json.load(open('checkpoints/<ts>.json'))['payload']; print(json.dumps(d, sort_keys=True, separators=(',',':')))"`
2. Verify the Ed25519 `signature_hex` against the anchor public key above.
3. Fetch the live head: `curl https://switchboard-ai.fly.dev/api/v1/chain/head?room=<name>`
   — it must match (or descend from) the anchored head for that room.
   Recompute the room's hash chain from the export to confirm linkage.

New checkpoints only ever *add* history. If two checkpoints ever disagree
about the same room at the same height, the ledger was rewritten — and the
proof is here forever.
