from bridge import MoltCipherBridge
import json

# Setup the bridge
key = MoltCipherBridge.generate_shared_key()
bridge = MoltCipherBridge(shared_key=key.encode())

print(f"--- 🔑 Secure Handoff Example ---")
print(f"Shared Key (Whisper this to the sub-agent once): {key}\n")

# Intent: Database Migration Secret
secret_task = {
    "action": "DB_MIGRATE",
    "params": {
        "db_host": "10.0.0.5",
        "db_pass": "P@ssw0rd123_DONT_LOG_THIS"
    }
}

print(f"[MainAgent] Sealing sensitive DB migration task...")
fragment = bridge.seal_intent("MainAgent", "MigrationBot", secret_task)

print("\n--- 📝 CHAT LOG OUTPUT (Opaque) ---")
print(json.dumps(fragment, indent=2))
print("----------------------------------\n")

print(f"[MigrationBot] Receiving fragment and unsealing in isolated session...")
unsealed = bridge.unseal_intent(fragment)

if unsealed["success"]:
    print(f"Decrypted Content: {json.dumps(unsealed['intent'], indent=2)}")
    print(f"Origin Verified: {unsealed['sender']}")
