import json
import time
import os
import hashlib
import subprocess
import base64
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class MoltCipherBridge:
    """
    🦞 MOLT-CIPHER-BRIDGE | v1.4.0 (Enhanced)
    -------------------------------------------
    Agent-to-Agent (A2A) cryptographic protocol for passing 'Sealed Intents'.
    Ensures zero-log context by encrypting sensitive task data at source.
    """

    def __init__(self, shared_key=None):
        if isinstance(shared_key, str):
            shared_key = shared_key.encode()
        self.key = shared_key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def seal_intent(self, sender_id, recipient_id, intent_data, ttl_seconds=300, multipart=None, binary=False):
        """
        Seal data. If binary is True, intent_data should be bytes or base64 string.
        """
        is_raw_bytes = False
        if binary:
            if isinstance(intent_data, bytes):
                intent_data = base64.b64encode(intent_data).decode()
                is_raw_bytes = True
            elif isinstance(intent_data, str):
                # Assume already b64 or just treat as string
                pass

        payload = {
            "s": sender_id,
            "r": recipient_id,
            "d": intent_data,
            "exp": (datetime.now() + timedelta(seconds=ttl_seconds)).timestamp(),
            "sig": hashlib.sha256(f"{sender_id}:{recipient_id}".encode()).hexdigest()[:16],
            "bin": binary,
            "raw": is_raw_bytes
        }
        if multipart: payload["part"] = multipart
        sealed = self.cipher.encrypt(json.dumps(payload).encode())
        return {
            "v": "1.4.0",
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
            
            intent = data["d"]
            if data.get("bin") and data.get("raw"):
                intent = base64.b64decode(intent)

            return {
                "success": True,
                "sender": data["s"],
                "recipient": data["r"],
                "intent": intent,
                "multipart": data.get("part", None),
                "is_binary": data.get("bin", False)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def execute_sealed_command(self, fragment, command_template, ignore_expiry=False, pick=None):
        result = self.unseal_intent(fragment, ignore_expiry=ignore_expiry)
        if not result["success"]:
            return result

        intent = result["intent"]
        env = os.environ.copy()
        
        extracted_secrets = {}

        # If it's a dict, extract secrets
        if isinstance(intent, dict):
            extracted_secrets = intent.get("secrets", intent)
        
        # If it's a string and looks like env file, parse it
        elif isinstance(intent, str) and "=" in intent:
            for line in intent.splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    extracted_secrets[k.strip()] = v.strip().strip("'\"")
        
        # Filtering logic
        pick_list = [p.strip() for p in pick.split(",")] if pick else None
        
        for k, v in extracted_secrets.items():
            if pick_list is None or k in pick_list:
                env[str(k)] = str(v)

        try:
            # Command template replacement logic
            final_command = command_template
            for k, v in env.items():
                placeholder = f"{{{k}}}"
                if placeholder in final_command:
                    final_command = final_command.replace(placeholder, str(v))

            process = subprocess.run(
                final_command,
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
    parser = argparse.ArgumentParser(description="🦞 Molt-Cipher-Bridge CLI (v1.4.0)")
    subparsers = parser.add_subparsers(dest="command")

    # Seal
    seal_p = subparsers.add_parser("seal")
    seal_p.add_argument("--key", required=True)
    seal_p.add_argument("--sender", required=True)
    seal_p.add_argument("--to", required=True)
    seal_p.add_argument("--data", help="Plain text or JSON string")
    seal_p.add_argument("--file", help="Path to any file (JSON, .env, binary, etc.)")
    seal_p.add_argument("--ttl", type=int, default=300)
    seal_p.add_argument("--binary", action="store_true", help="Treat file as binary data")

    # Unseal
    unseal_p = subparsers.add_parser("unseal")
    unseal_p.add_argument("--key", required=True)
    unseal_p.add_argument("--fragment", required=True)
    unseal_p.add_argument("--ignore-expiry", action="store_true")
    unseal_p.add_argument("--out", help="Write unsealed intent to this file")

    # Run
    run_p = subparsers.add_parser("run")
    run_p.add_argument("--key", required=True)
    run_p.add_argument("--fragment", required=True)
    run_p.add_argument("--cmd", required=True)
    run_p.add_argument("--ignore-expiry", action="store_true")
    run_p.add_argument("--pick", help="Comma-separated list of keys to inject (default: all)")

    # Sample
    sample_p = subparsers.add_parser("sample")
    sample_p.add_argument("--type", choices=["json", "env"], default="json")
    sample_p.add_argument("--out", default="secrets.sample")

    args = parser.parse_args()

    if args.command == "seal":
        bridge = MoltCipherBridge(shared_key=args.key)
        intent_data = None
        is_binary = args.binary
        
        if args.file:
            if not os.path.exists(args.file):
                print(json.dumps({"success": False, "error": f"File not found: {args.file}"}))
                return
            
            mode = 'rb' if is_binary else 'r'
            with open(args.file, mode) as f:
                if is_binary:
                    intent_data = f.read()
                else:
                    content = f.read()
                    try:
                        intent_data = json.loads(content)
                    except:
                        intent_data = content
        elif args.data:
            try: intent_data = json.loads(args.data)
            except: intent_data = args.data
        else:
            print(json.dumps({"success": False, "error": "Must provide --data or --file"}))
            return
            
        print(json.dumps(bridge.seal_intent(args.sender, args.to, intent_data, ttl_seconds=args.ttl, binary=is_binary)))

    elif args.command == "unseal":
        bridge = MoltCipherBridge(shared_key=args.key)
        try:
            frag = json.loads(args.fragment)
        except:
            if os.path.exists(args.fragment):
                with open(args.fragment, 'r') as f:
                    frag = json.load(f)
            else:
                raise
        
        result = bridge.unseal_intent(frag, ignore_expiry=args.ignore_expiry)
        
        if args.out and result["success"]:
            mode = 'wb' if isinstance(result["intent"], bytes) else 'w'
            with open(args.out, mode) as f:
                if isinstance(result["intent"], (dict, list)):
                    f.write(json.dumps(result["intent"], indent=2))
                else:
                    f.write(result["intent"])
            result["saved_to"] = args.out
            
        # For JSON output, if intent is bytes, b64 encode it
        if result["success"] and isinstance(result["intent"], bytes):
            result["intent"] = base64.b64encode(result["intent"]).decode()
            
        print(json.dumps(result))

    elif args.command == "run":
        bridge = MoltCipherBridge(shared_key=args.key)
        try:
            frag = json.loads(args.fragment)
        except:
            if os.path.exists(args.fragment):
                with open(args.fragment, 'r') as f:
                    frag = json.load(f)
            else:
                raise
        print(json.dumps(bridge.execute_sealed_command(frag, args.cmd, ignore_expiry=args.ignore_expiry, pick=args.pick)))

    elif args.command == "sample":
        if args.type == "json":
            content = json.dumps({"API_KEY": "your_key_here", "DB_PASSWORD": "secret_password"}, indent=2)
        else:
            content = "API_KEY=your_key_here\nDB_PASSWORD=secret_password\n"
        
        with open(args.out, 'w') as f:
            f.write(content)
        print(json.dumps({"success": True, "file": args.out, "type": args.type}))

if __name__ == "__main__":
    cli()
