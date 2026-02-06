import json
import time
import os
import hashlib
import subprocess
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class MoltCipherBridge:
    """
    🦞 MOLT-CIPHER-BRIDGE | v1.3.0 (Production)
    -------------------------------------------
    Agent-to-Agent (A2A) cryptographic protocol for passing 'Sealed Intents'.
    Ensures zero-log context by encrypting sensitive task data at source.
    """

    def __init__(self, shared_key=None):
        if isinstance(shared_key, str):
            shared_key = shared_key.encode()
        self.key = shared_key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def seal_intent(self, sender_id, recipient_id, intent_data, ttl_seconds=300, multipart=None):
        payload = {
            "s": sender_id,
            "r": recipient_id,
            "d": intent_data,
            "exp": (datetime.now() + timedelta(seconds=ttl_seconds)).timestamp(),
            "sig": hashlib.sha256(f"{sender_id}:{recipient_id}".encode()).hexdigest()[:16]
        }
        if multipart: payload["part"] = multipart
        sealed = self.cipher.encrypt(json.dumps(payload).encode())
        return {
            "v": "1.3.0",
            "fid": f"frag_{os.urandom(4).hex()}",
            "payload": sealed.decode(),
            "hint": self.key.decode()[:8],
            "signed": True
        }

    def unseal_intent(self, fragment, ignore_expiry=False):
        try:
            decrypted = self.cipher.decrypt(fragment["payload"].encode())
            data = json.loads(decrypted)
            if not ignore_expiry and datetime.now().timestamp() > data["exp"]:
                return {"success": False, "error": "FRAGMENT_EXPIRED"}
            return {
                "success": True,
                "sender": data["s"],
                "recipient": data["r"],
                "intent": data["d"],
                "multipart": data.get("part", None)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def execute_sealed_command(self, fragment, command_template, ignore_expiry=False):
        result = self.unseal_intent(fragment, ignore_expiry=ignore_expiry)
        if not result["success"]:
            return result

        intent = result["intent"]
        secrets = intent.get("secrets", {})
        
        env = os.environ.copy()
        for k, v in secrets.items():
            env[k] = str(v)

        try:
            process = subprocess.run(
                command_template,
                shell=True,
                env=env,
                capture_output=True,
                text=True
            )
            return {
                "success": True,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "exit_code": process.returncode
            }
        except Exception as e:
            return {"success": False, "error": f"Execution failed: {str(e)}"}

    @staticmethod
    def generate_shared_key():
        return Fernet.generate_key().decode()

def cli():
    import argparse
    parser = argparse.ArgumentParser(description="🦞 Molt-Cipher-Bridge CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Seal
    seal_p = subparsers.add_parser("seal")
    seal_p.add_argument("--key", required=True)
    seal_p.add_argument("--sender", required=True)
    seal_p.add_argument("--to", required=True)
    seal_p.add_argument("--data", help="JSON string data (LEAKS IN LOGS)")
    seal_p.add_argument("--file", help="Path to a JSON file containing secrets (LOG-SAFE)")
    seal_p.add_argument("--ttl", type=int, default=300)

    # Unseal
    unseal_p = subparsers.add_parser("unseal")
    unseal_p.add_argument("--key", required=True)
    unseal_p.add_argument("--fragment", required=True)
    unseal_p.add_argument("--ignore-expiry", action="store_true")

    # Run
    run_p = subparsers.add_parser("run")
    run_p.add_argument("--key", required=True)
    run_p.add_argument("--fragment", required=True)
    run_p.add_argument("--cmd", required=True)
    run_p.add_argument("--ignore-expiry", action="store_true")

    args = parser.parse_args()

    if args.command == "seal":
        bridge = MoltCipherBridge(shared_key=args.key)
        intent_data = None
        
        if args.file:
            if not os.path.exists(args.file):
                print(json.dumps({"success": False, "error": f"File not found: {args.file}"}))
                return
            with open(args.file, 'r') as f:
                try:
                    intent_data = json.load(f)
                except:
                    f.seek(0)
                    intent_data = f.read().strip()
        elif args.data:
            try: intent_data = json.loads(args.data)
            except: intent_data = args.data
        else:
            print(json.dumps({"success": False, "error": "Must provide --data or --file"}))
            return
            
        print(json.dumps(bridge.seal_intent(args.sender, args.to, intent_data, ttl_seconds=args.ttl)))

    elif args.command == "unseal":
        bridge = MoltCipherBridge(shared_key=args.key)
        print(json.dumps(bridge.unseal_intent(json.loads(args.fragment), ignore_expiry=args.ignore_expiry)))

    elif args.command == "run":
        bridge = MoltCipherBridge(shared_key=args.key)
        print(json.dumps(bridge.execute_sealed_command(json.loads(args.fragment), args.cmd, ignore_expiry=args.ignore_expiry)))

if __name__ == "__main__":
    cli()
