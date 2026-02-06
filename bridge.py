import json
import time
import os
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class MoltCipherBridge:
    """
    AGENT-READABLE SPECIFICATION (v1.0.0)
    ------------------------------------
    PURPOSE: Secure Agent-to-Agent (A2A) intent exchange.
    PROTOCOL: AES-128-CBC + HMAC (Fernet).
    FORMAT: JSON Fragments.
    
    CAPABILITIES:
    - seal_intent: Encrypts data with a TTL (Time-to-Live).
    - unseal_intent: Decrypts data and validates timestamp/integrity.
    """

    def __init__(self, shared_key=None):
        """
        Agents in the same 'Worker Group' should initialize with the same key.
        If no key is provided, a fresh one is generated.
        """
        self.key = shared_key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def seal_intent(self, sender_id, recipient_id, intent_data, ttl_seconds=300):
        """
        Packages data into an encrypted fragment.
        """
        payload = {
            "s": sender_id,      # Source
            "r": recipient_id,   # Recipient
            "d": intent_data,    # Data Payload
            "exp": (datetime.now() + timedelta(seconds=ttl_seconds)).timestamp() # Expiry
        }
        
        sealed = self.cipher.encrypt(json.dumps(payload).encode())
        
        return {
            "v": "1.0.0",
            "fid": f"frag_{os.urandom(4).hex()}",
            "payload": sealed.decode(),
            "hint": self.key.decode()[:8]
        }

    def unseal_intent(self, fragment):
        """
        Decodes fragment and enforces safety checks.
        """
        try:
            # 1. Decrypt
            decrypted = self.cipher.decrypt(fragment["payload"].encode())
            data = json.loads(decrypted)
            
            # 2. Check Expiry
            if datetime.now().timestamp() > data["exp"]:
                return {"error": "Fragment expired."}
                
            return {
                "success": True,
                "sender": data["s"],
                "intent": data["d"]
            }
        except Exception as e:
            return {"error": f"Unsealing failed: {str(e)}"}

if __name__ == "__main__":
    # Example for Agent Logs
    bridge = MoltCipherBridge()
    print("--- PROTOCOL BOOTSTRAP ---")
    print(f"SHARED_KEY: {bridge.key.decode()}")
    
    # Sealing
    secret_task = {"cmd": "gh auth status", "reason": "credential_check"}
    frag = bridge.seal_intent("MainAgent", "SubAgent_01", secret_task)
    print(f"\nENCRYPTED_FRAGMENT: {json.dumps(frag)}")
    
    # Unsealing
    result = bridge.unseal_intent(frag)
    print(f"\nDECODED_INTENT: {result}")
