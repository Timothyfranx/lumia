import subprocess
import time
import urllib.request
import json
import os
import sys

def test_endpoints():
    print("🚀 Starting Lumia FastAPI Backend in a background process...")
    # Add project root to python path
    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/replytim/Desktop/portaldot"
    
    server_process = subprocess.Popen(
        ["venv/bin/python", "-m", "backend.app"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to boot up
    time.sleep(3)
    
    success = True
    try:
        # Test 1: Health check
        print("\n🔍 Test 1: GET /health")
        req = urllib.request.Request("http://127.0.0.1:8000/health")
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"✅ Response: {res_data}")
            assert res_data["status"] == "online"

        # Test 2: Scan address (Using Bob's valid address)
        print("\n🔍 Test 2: POST /scan (Bob's address)")
        post_data = json.dumps({
            "sender": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", # Alice
            "recipient": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty", # Bob
            "amount": 25.5,
            "token": "POT"
        }).encode('utf-8')
        
        req = urllib.request.Request(
            "http://127.0.0.1:8000/scan",
            data=post_data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print("✅ Scan Successful!")
            print(f"Risk Score: {res_data['risk_score']}")
            print(f"Risk Level: {res_data['risk_level']}")
            print(f"AI Briefing: {res_data['ai_briefing'][:120]}...")
            assert "risk_score" in res_data
            assert "ai_briefing" in res_data

        # Test 3: Register Receipt on Smart Contract
        print("\n🔍 Test 3: POST /register")
        tx_hash = "0x" + "a" * 64
        register_data = json.dumps({
            "tx_hash": tx_hash,
            "risk_score": res_data["risk_score"]
        }).encode('utf-8')
        
        req = urllib.request.Request(
            "http://127.0.0.1:8000/register",
            data=register_data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"✅ Register Successful: {res_data}")
            assert res_data["success"] is True

        # Test 4: Get Receipt from Smart Contract
        print("\n🔍 Test 4: GET /receipt/{tx_hash}")
        req = urllib.request.Request(f"http://127.0.0.1:8000/receipt/{tx_hash}")
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"✅ Query Successful: {res_data}")
            assert res_data["success"] is True
            assert res_data["receipt"]["risk_score"] is not None

    except Exception as e:
        print(f"❌ Verification Test Failed: {e}")
        success = False
        # Print server stdout and stderr for debugging
        print("\n--- SERVER STDOUT ---")
        try:
            out, err = server_process.communicate(timeout=2)
            print(out)
            print("\n--- SERVER STDERR ---")
            print(err)
        except Exception as ce:
            print(f"Failed to read server logs: {ce}")
    finally:
        print("\n🛑 Stopping background server process...")
        server_process.terminate()
        try:
            server_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("Server stopped.")
        
    if success:
        print("\n🟢 ALL BACKEND REST API ENDPOINTS FULLY VERIFIED!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    test_endpoints()
