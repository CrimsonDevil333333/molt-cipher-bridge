from bridge import MoltCipherBridge
import json

# Split a large secret into 2 parts for 2 different agents
bridge = MoltCipherBridge() # Fresh key for this session

master_intent = "THE_FULL_API_KEY_IS_12345-ABCDE-67890"
parts = [master_intent[:18], master_intent[18:]]

print("--- 🧩 Multipart Distributed Secret Example ---")
print("Scenario: Splitting a secret so no single agent log contains the full key.\n")

fragments = []
for i, part in enumerate(parts):
    frag = bridge.seal_intent("Director", f"Agent_{i+1}", {"fragment": part}, multipart={"current": i+1, "total": 2})
    fragments.append(frag)
    print(f"Sealed Part {i+1}: {frag['fid']}")

print("\n--- 🛠️ Reconstruction ---")
reconstructed = ""
for frag in fragments:
    result = bridge.unseal_intent(frag)
    print(f"Decoded Part {result['multipart']['current']}: {result['intent']['fragment']}")
    reconstructed += result['intent']['fragment']

print(f"\nFinal Secret: {reconstructed}")
