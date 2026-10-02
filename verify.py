#!/usr/bin/env python3
"""One-command verifier for a Switchboard checkpoint anchor.

Usage:
    pip install pynacl
    python3 verify.py [checkpoints/<ts>.json]   # defaults to checkpoints/latest.json

Verifies the Ed25519 signature over the canonical payload, then prints the
anchored room heads. To check a head against the live ledger:
    curl -s "https://switchboard-ai.fly.dev/api/v1/chain/head?room=<name>"
"""
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "checkpoints/latest.json"

with open(path) as f:
    data = json.load(f)

payload = data["payload"]
pubkey_hex = payload["anchor_pubkey"]
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
sig = bytes.fromhex(data["signature_hex"])

try:
    from nacl.signing import VerifyKey
except ImportError:
    sys.exit("PyNaCl is required: pip install pynacl")

VerifyKey(bytes.fromhex(pubkey_hex)).verify(sig + canonical)

print(f"OK — signature valid (Ed25519, anchor key {pubkey_hex[:16]}…)")
print(f"checkpoint: {payload['anchored_at']}  network: {payload['network']}")
for room, h in sorted(payload["heads"].items()):
    print(f"  #{room}: head={h['head'][:16]}…  messages={h['message_count']}")
