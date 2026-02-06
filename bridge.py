import json
import time
import os
import hashlib
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class MoltCipherBridge:
    """
    🦞 MOLT-CIPHER-BRIDGE | v1.1.0 (Production)
    -------------------------------------------
    An Agent-to-Agent (A2A) cryptographic protocol for passing 'Sealed Intents'.
    Ensures least-privilege context by encrypting sensitive task data.
    """

    def __init__(self, shared_key=None):
        self.key = shared_key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def seal_intent(self, sender_id, recipient_id, intent_data, ttl_seconds=300, multipart=None):
        """
        Seal a task. Supports multipart indexing for complex distributed tasks.
        """
        payload = {
            "s": sender_id,
            "r": recipient_id,
            "d": intent_data,
            "exp": (datetime.now() + timedelta(seconds=ttl_seconds)).timestamp(),
            "sig": hashlib.sha256(f"{sender_id}:{recipient_id}".encode()).hexdigest()[:16]
        }
        
        if multipart:
            payload["part"] = multipart # e.g. {"current": 1, "total": 3}

        sealed = self.cipher.encrypt(json.dumps(payload).encode())
        
        return {
            "v": "1.1.0",
            "fid": f"frag_{os.urandom(4).hex()}",
            "payload": sealed.decode(),
            "hint": self.key.decode()[:8],
            "signed": True
        }

    def unseal_intent(self, fragment, ignore_expiry=False):
        try:
            decrypted = self.cipher.decrypt(fragment["payload"].encode())
            data = json.loads(decrypted)
            
            # Expiry Check
            if not ignore_expiry and datetime.now().timestamp() > data["exp"]:
                return {"success": False, "error": "FRAGMENT_EXPIRED"}
                
            return {
                "success": True,
                "sender": data["s"],
                "recipient": data["r"],
                "intent": data["d"],
                "multipart": data.get("part", None),
                "expires_at": datetime.fromtimestamp(data["exp"]).isoformat() if "exp" in data else None
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def generate_shared_key():
        return Fernet.generate_key().decode()

