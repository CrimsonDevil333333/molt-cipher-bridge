from bridge import MoltCipherBridge
import json

# REAL SHARED KEY provided by user
SHARED_KEY = 'Sdyooy7wF18WlM2Gp6RE-bj-fkHOfBWM0FLNRPMZQXk='

# REAL FRAGMENT provided by user
FRAGMENT = {
    "v": "1.1.0", 
    "fid": "frag_73667219", 
    "payload": "gAAAAABphTS2NC1GI-IodoWk8jrjtj4RvBcTjILr9JX2pkGDNww5hbMVGTJ-7j1z6hZWTKnUsEeAbz2ICozj09m_pjeS9s6-2fJ1TRcxuPSn6cNiP3yLYFu3gqM5h1siz81kw3iWOXDNf4aMx7qvwZihzE4IqWUHE4M4i6_KFoblhkQdPjsvrj91MFt_-Vfm293d7rvFRxfCw5X4CxItwdQv2zlLvxosacXKUnjcxKuzFgV0OBT-WvkESkxISOOTgPe8wf0i3hqxUlITkxgzGEW4VPTvSrVhT_iY5cjrQTrtROCuTp0WOwnIeypSE6mBBW7_Ibg8c1yZqkgTEokH9fMzE07XGhTBtg==", 
    "hint": "Sdyooy7w", 
    "signed": True
}

def main():
    bridge = MoltCipherBridge(shared_key=SHARED_KEY)
    result = bridge.unseal_intent(FRAGMENT, ignore_expiry=True)
    
    if result["success"]:
        print("--- Unseal Successful ---")
        print(f"Sender: {result['sender']}")
        print(f"Recipient: {result['recipient']}")
        print(f"Intent: {json.dumps(result['intent'], indent=2)}")
        if result['multipart']:
            print(f"Multipart: {result['multipart']}")
    else:
        print(f"--- Unseal Failed ---")
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()
